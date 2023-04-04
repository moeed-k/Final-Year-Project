from huggingsound import SpeechRecognitionModel
from pyannote.audio import Pipeline
from pydub import AudioSegment
from scipy.io import wavfile
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from collections import Counter
from multiprocessing.connection import Listener
from multiprocessing.pool import ThreadPool
import crepe
import soundfile as sf
import librosa
import wordsegment
import nltk
import shutil
import torch
import glob
import os
import json
import threading as td

import tracemalloc

####################################################################  HELPER FUNCTIONS #######################################################################

def trimAudio(audioPath):
    audio = AudioSegment.from_wav(audioPath)
    if audio.duration_seconds > 30:
        trim = audio[0:30*1000]
        os.remove(audioPath)
        trim.export(audioPath,format="wav")


# returns 2 parallel arrays that contain the start and stop times of every speech interval in an audio file
def getSpeechTimes(audioPath):
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token="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")
    output = pipeline(audioPath)

    start_times = []
    end_times = []

    for speech in output.get_timeline().support():
        start_times.append(speech.start)
        end_times.append(speech.end)

    return start_times, end_times


# takes the speech start and stop times of an audio file and saves them as snippets
def saveSnippets(start_times,end_times, audioPath, saveDir):
    folderName = (audioPath.split("/")[-1]).rstrip(".wav")

    directory = saveDir+"/"+folderName

    if not os.path.exists(directory):
        os.makedirs(directory)

    audio = AudioSegment.from_wav(audioPath)

    for i in range(len(start_times)):
        start = int(start_times[i] * 1000)
        end = int(end_times[i] * 1000)
        snippet = audio[start:end]

        snippetName = directory + "/" + str(i) + ".wav"
        snippet.export(snippetName, format = "wav")


#  takes a transcription model and audio name and returns the WPM
#  requires:
#           snippets of audio name in ./snippets/AUDIONAME/0.wav,1.wav...n.wav
#           list of transcription of each snippet
def getWPM(transcriptions, audioName,SNIPPET_SAVE_DIR):
    folderName = audioName.rstrip(".wav")
    path = f'{SNIPPET_SAVE_DIR}{folderName}/'

    if not os.path.exists(path):
        print("ERROR: Audio snippets do not exist. Please create snippets first.")
        return 0

    snippets = glob.glob(path+"*.wav")

    if not snippets or not transcriptions:
        print("ERROR. Either no snippets found or transcriptions do not exist.")
        return 0



    totalSeconds = 0
    totalWords = 0

    i = 0



    for snippetPath in snippets:
        transcription = transcriptions[i]
        audio = AudioSegment.from_wav(snippetPath)

        totalWords += len(transcription.split(" "))
        totalSeconds += audio.duration_seconds

        i += 1

    if totalSeconds == 0:
        print("ERROR. Total time of snippets is 0 seconds.")
        return 0

    WPM = totalWords/(totalSeconds/60)

    return WPM


#  takes a transcription object (dictionary) and an error threshold, and returns the clarity score
def getSpeechClarity(transcription, errorThreshold):
    transcribedText = transcription['transcription']
    startings = transcription["start_timestamps"]
    endings = transcription["end_timestamps"]
    probs = transcription['probabilities']

    length = len(transcription['transcription'])
    ambiguities = 0

    for i in range(length):
        currProb = transcription['probabilities'][i]

        # Show probability of every transcribed letter
        # print(transcriptions[0]['transcription'][i], " : ", transcriptions[0]['probabilities'][i])

        if currProb < errorThreshold:
            ambiguities += 1

    return 1 - (ambiguities / length)


# returns a list of pause durations
def getPauses(start_times,end_times,audio_end_time):
    length = len(start_times)
    if length == 0:
        print("ERROR. No start times, hence no voice detected.")
        return [],0,0
    pauses = []
    # first pause. Necessary when batch processing 30 second clips in succession. If audio clip#2 of a speech has a
    # long first pause, it means the speaker had paused speaking since the end of audio clip#1
    pauses.append(start_times[0])

    totalTime = 0
    badPauseCount = 0
    badPauseThreshold = 2

    for i in range(length):
        if i != 0:
            pause = start_times[i] - end_times[i-1]
            pause = round(pause,2)
            pauses.append(pause)
            totalTime += pause
            if pause > badPauseThreshold:
                badPauseCount += 1

    # last pause
    pauses.append(audio_end_time- end_times[length-1])

    return pauses, totalTime, badPauseCount


# returns the transcription of the audio name as a single string. Also returns the transcription dictionary object containing probabilities. Uses xlsr
def getTranscrptionString(stt_model, audio_path):
    if not (os.path.exists(audio_path)):
        print("ERROR. Audio does not exist. Cannot transcribe.")
        return [],""

    transcriptions = stt_model.transcribe([audio_path])

    return transcriptions[0], " ".join(wordsegment.segment(transcriptions[0]['transcription']))


# returns the transcription of the audio snippets as a list of strings. Also returns a list of probability lists. Uses xlsr
def getTranscrptionStrings(stt_model, audioName,SNIPPET_SAVE_DIR):
    if not os.path.exists(f'{SNIPPET_SAVE_DIR}{audioName.rstrip(".wav")}'):
        print("ERROR: Audio snippets do not exist. Please create snippets first.")
        return 0

    snippets = glob.glob(f'{SNIPPET_SAVE_DIR}/{audioName.rstrip(".wav")}/' + "*.wav")

    transcriptions = []
    snippetProbabilities = []
    for snippetPath in snippets:
        transcription = stt_model.transcribe([snippetPath])

        transcriptionText = transcription[0]['transcription']
        # segmenting words without spaces in between
        transcriptionText = " ".join(wordsegment.segment(transcriptionText))

        transcriptions.append(transcriptionText)
        snippetProbabilities.append(transcription[0]['probabilities'])

    return snippetProbabilities, transcriptions



# return the phoneme transcription of the audio name as a single strings. Uses wav2vec2
def getPhonemeTranscriptionString(processor, phoneme_model, audio_path):
    audioArray, samplerate = sf.read(audio_path)

    if samplerate != 16000:
        audioArray = librosa.resample(audioArray,samplerate,16000)

    input_values = processor(audioArray, return_tensors="pt", padding="longest").input_values  # Batch size 1


    # retrieve logits
    logits = phoneme_model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)

    return transcription


# return the phoneme transcription of the audio snippets as a list of strings. Uses wav2vec2
def getPhonemeTranscriptionStrings(processor, phoneme_model, audioName,SNIPPET_SAVE_DIR):
    if not os.path.exists(f'{SNIPPET_SAVE_DIR}{audioName.rstrip(".wav")}'):
        print("ERROR: Audio snippets do not exist. Please create snippets first.")
        return 0

    snippets = glob.glob(f'{SNIPPET_SAVE_DIR}{audioName.rstrip(".wav")}/' + "*.wav")

    transcriptions = []

    for snippetPath in snippets:
        audioArray, samplerate = sf.read(snippetPath)

        if samplerate != 16000:
            audioArray = librosa.resample(audioArray, samplerate, 16000)

        input_values = processor(audioArray, return_tensors="pt", padding="longest").input_values  # Batch size 1

        # retrieve logits
        logits = phoneme_model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)

        transcriptions.append(transcription)

    return transcriptions

# returns count of filler sounds 'uh' and 'um'. Requires phoneme snippet transcriptions and normal snippet transcriptions
def getFillerSounds(phonemeSnippets, normalSnippets):
    lexicon = ['uh','e','um','ah','af','om','o']

    phonemeSentence = ""

    for snippet in phonemeSnippets:
        tmp = ""
        tmp = tmp.join(snippet)
        phonemeSentence += " " + tmp

    phonemeSentence = phonemeSentence.lower()
    phonemeTokens = phonemeSentence.split(" ")

    normalSentence = ""

    for snippet in normalSnippets:
        tmp = ""
        tmp = tmp.join(snippet)
        phonemeSentence += tmp
        normalSentence += " " + snippet

    normalSentence = normalSentence.lower()
    normalTokens = normalSentence.split(" ")

    if not phonemeTokens or not normalTokens:
        print("ERORR. Either phoneme transcription or regular transcription returned empty.")
        return 0

    # The following is a list of words that are actual english words, but the phoneme transcription also maps them onto filler sounds.
    # for example, the sound 'um' is sometimes mapped as 'am'
    normal_a_count = 0
    normal_of_count = 0
    normal_am_count= 0
    normal_oh_count = 0
    phoneme_a_count = 0
    phoneme_of_count = 0
    phoneme_am_count = 0
    phoneme_oh_count = 0

    otherFillerCount = 0

    for token in phonemeTokens:
        if token == 'a':
            phoneme_a_count += 1
        elif token == 'of':
            phoneme_of_count += 1
        elif token == 'am':
            phoneme_am_count += 1
        elif token == 'oh':
            phoneme_oh_count += 1
        elif token in lexicon:
            otherFillerCount += 1

    for token in normalTokens:
        if token == 'a':
            normal_a_count += 1
        elif token == 'of':
            normal_of_count += 1
        elif token == 'am':
            normal_am_count += 1
        elif token == 'oh':
            normal_oh_count += 1


    if phoneme_a_count >= normal_a_count:
        phoneme_a_count = phoneme_a_count - normal_a_count
    else:
        phoneme_a_count = 0

    if phoneme_of_count >= normal_of_count:
        phoneme_of_count = phoneme_of_count - normal_of_count
    else:
        phoneme_of_count = 0

    if phoneme_am_count >= normal_am_count:
        phoneme_am_count = phoneme_am_count - normal_am_count
    else:
        phoneme_am_count = 0

    if phoneme_oh_count >= normal_oh_count:
        phoneme_oh_count = phoneme_oh_count - normal_oh_count
    else:
        phoneme_oh_count = 0

    return otherFillerCount + phoneme_a_count + phoneme_of_count + phoneme_am_count + phoneme_oh_count


# returns speech clarity score from a list of snippet probabilitiy lists
def getSpeechClarityFromSnippets(snippetProbabilities, errorThreshold):
    ambiguities = 0
    totalLength = 0

    for snippetProbability in snippetProbabilities:
        if not snippetProbability:
            continue

        length = len(snippetProbability)
        totalLength += length

        for probability in snippetProbability:
            if probability < errorThreshold:
                ambiguities += 1

    if totalLength == 0:
        print("ERROR. Cannot get clarity as length of transcribed audio probability is 0.")
        return 0

    return 1 - (ambiguities/totalLength)


# returns a list of filler words/phrases
def getFillers(transcription):
    word_lexicon = ['well', 'okay', 'ok', 'so', 'like', 'basically', 'actually', 'literally', 'totally', 'seriously',
                    'hopefully', 'probably', 'mean', 'know', 'relatively']
    phrase_lexicon = ['well so', 'i think', 'think that', 'you know', 'i know','to say', 'you see', 'so you', 'i mean',
                      'you mean', 'what i', 'i guess', 'i suppose', 'or something', 'something like', 'sort of',
                      'kind of', 'stuff like']

    if not transcription:
        print("ERROR. Length of transcribed audio is 0.")
        return []

    tokens = transcription.split(" ")

    # not enough words to accurately find filler words
    if len(tokens) < 5:
        return []

    wordCounts = Counter(tokens)

    # checking filler words
    wordTuples = wordCounts.most_common(5)

    filler_words = []

    for wordTuple in wordTuples:
        if wordTuple[0] in word_lexicon:
            filler_words.append(wordTuple[0])


    # checking filler phrases
    bigrams = []
    for words in nltk.bigrams(tokens):
        bigrams.append(" ".join(words))

    phraseCounts = Counter(bigrams)
    phraseTuples = phraseCounts.most_common(5)

    filler_phrases = []
    for phraseTuple in phraseTuples:
        if phraseTuple[0] in phrase_lexicon:
            filler_phrases.append(phraseTuple[0])

    # filtering filler words and phrases into a single list to remove overlaps
    # for example, filler phrase 'i mean' already contains filler word 'mean'
    filteredFillers = []

    filler_phrases_as_sentence = " ".join(filler_phrases)


    for filler in filler_words:
        if filler not in filler_phrases_as_sentence:
            filteredFillers.append(filler)


    for filler in filler_phrases:
        filteredFillers.append(filler)


    return filteredFillers


# returns a list of filler words from snippets
def getFillersFromSnippets(snippetTranscriptions):
    sentence = ""

    for snippet in snippetTranscriptions:
        tmp = ""
        tmp = tmp.join(snippet)
        sentence += " " + tmp

    return getFillers(sentence)


# concatenates snippetTranscriptions into a single sentence
def makeSentence(snippetTranscriptions):
    sentence = ""

    for snippet in snippetTranscriptions:
        tmp = ""
        tmp = tmp.join(snippet)
        sentence += " " + tmp

    return sentence




def getPitch(audioFile):
    sr, audio = wavfile.read(audioFile)
    #Step size defined here
    time, frequency, confidence, activation = crepe.predict(audio, sr, step_size=35, viterbi=True)
    frequency_mean = frequency.mean()
    frequency_range = frequency.max(), frequency.min()
    return frequency_mean, time.tolist(), frequency.tolist()

def getWordCount(transcription):
    tokens = transcription.split(" ")
    return len(tokens)

def getSnippetWordCount(snippetTranscriptions):
    word_count = 0

    for snippet in snippetTranscriptions:
        word_count += getWordCount(snippet)

    return word_count




####################################################################  DRIVER CODE #######################################################################


def getStats(audioPath,snippetPath):
    SNIPPET_SAVE_DIR = snippetPath#f'./session{sessionID}/snippets'
    audio_path = audioPath#f'./session{sessionID}/audio/{audio_name}'
    audio_name = audio_path.split('/')[-1]

    AUDIO_END_TIME = AudioSegment.from_wav(audio_path).duration_seconds


    start_times, end_times = getSpeechTimes(audio_path)

    # creating snippets for the audio file if they don't exist. Only checks for presence of the audio name in the snippets directory
    if not os.path.exists(f'{SNIPPET_SAVE_DIR}{audio_name.rstrip(".wav")}'):
        print("Snippet folder not found. Creating snippets...")
        saveSnippets(start_times, end_times, audio_path, SNIPPET_SAVE_DIR)



    # #############################################################################################
    pool = ThreadPool(processes=4)
    #transcriptionFunc = pool.apply_async(getTranscrptionString, (stt_model, audio_path))
    snippetFunc = pool.apply_async(getTranscrptionStrings, (stt_model, audio_name,SNIPPET_SAVE_DIR))
    phonemeFunc = pool.apply_async(getPhonemeTranscriptionStrings, (processor, phoneme_model, audio_name,SNIPPET_SAVE_DIR))
    pitchFunc = pool.apply_async(getPitch, ([audio_path]))

    ##################################################################################################
    #transcriptionDict, transcription = transcriptionFunc.get()
    snippetProbabilities, snippetTranscriptions = snippetFunc.get()
    phonemeSnippets = phonemeFunc.get()
    mean_pitch, pitch_time, pitch_freq = pitchFunc.get()

    #transcriptionFunc.wait()
    snippetFunc.wait()
    phonemeFunc.wait()

    fillerSoundCount = getFillerSounds(phonemeSnippets, snippetTranscriptions)
    filler_words = getFillersFromSnippets(snippetTranscriptions)
    clarity = getSpeechClarityFromSnippets(snippetProbabilities, 0.9)
    pauses, totalPauseTime, badPauseCount  =  getPauses(start_times, end_times, AUDIO_END_TIME)
    word_count = getSnippetWordCount(snippetTranscriptions)
    speechrate = getWPM(snippetTranscriptions, audio_name,SNIPPET_SAVE_DIR)

    pitchFunc.wait()

    clarity = int(clarity * 100)
    mean_pitch = int(mean_pitch)
    speechrate = int(speechrate)
    AUDIO_END_TIME = int(AUDIO_END_TIME)
	
    print("Transcription", snippetTranscriptions)
    print("Phoneme transcription: ", phonemeSnippets)
    print("Filler words: ", filler_words)
  
    metrics = {
        "clarity": clarity,
        "filler_sounds": fillerSoundCount,
        "pitch": mean_pitch,
        "pauses": max(len(pauses)-2,0),
        "wpm":speechrate,
        "filler words":len(filler_words),
        "total_pause_time":totalPauseTime,
	     "bad_pause_count": badPauseCount,
        "word_count": word_count,
        "total time": AUDIO_END_TIME,
	    "pitch_time": json.dumps(pitch_time),
	    "pitch_freq": json.dumps(pitch_freq),
	    "transcription":makeSentence(snippetTranscriptions)
    }

    return metrics


MODEL_NAME = "jonatasgrosman/wav2vec2-large-xlsr-53-english"
stt_model = SpeechRecognitionModel(MODEL_NAME)
phoneme_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
print("Models loaded.")


def threadedProcessor(audioPath,snippetPath,metricsPath):
    print("Data Processing beginning for audio clip at " + audioPath)
    stats = getStats(audioPath,snippetPath)
    json_obj = json.dumps(stats)
    with open(metricsPath, "w") as outfile:
        outfile.write(json_obj)
    print("Data Processing complete for audio clip "+ audioPath)



address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')


# word segmenter is used on transcription as a post process to give better results
wordsegment.load()

while 1:

    print("Waiting for client...")
    conn = listener.accept()
    print('connection accepted from', listener.last_accepted)
    msg = conn.recv()
    conn.close()
    tokens = msg.split(',')
    audioPath = tokens[0]
    snippetPath = tokens[2]
    metricsPath = tokens[1]
    print("Received data. Beginning processing...")

    worker = td.Thread(target=threadedProcessor, args=(audioPath,snippetPath,metricsPath))
    worker.start()

    print("Data processing assigned to worker thread.")
