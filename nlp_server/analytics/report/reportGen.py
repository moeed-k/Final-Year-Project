import nltk
import shutil
import glob
import os
import json
import time
from collections import Counter


####################################################################  HELPER FUNCTIONS #######################################################################

# returns a list of filler words/phrases
def getFillers(transcription):
    word_lexicon = ['well', 'okay', 'ok', 'so', 'like', 'basically', 'actually', 'literally', 'totally', 'seriously',
                    'hopefully', 'probably', 'mean', 'know', 'relatively']
    phrase_lexicon = ['well so', 'i think', 'think that', 'you know', 'i know', 'to say', 'you see', 'so you', 'i mean',
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
    wordTuples = wordCounts.most_common(10)

    filler_words = []

    for wordTuple in wordTuples:
        if wordTuple[0] in word_lexicon:
            filler_words.append(wordTuple[0])

    # checking filler phrases
    bigrams = []
    for words in nltk.bigrams(tokens):
        bigrams.append(" ".join(words))

    phraseCounts = Counter(bigrams)
    phraseTuples = phraseCounts.most_common(10)

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


# returns a count of all filler words used in a speaking session
def getFillerWordCount(transcriptions):
    sentence = ""

    for transcription in transcriptions:
        tmp = ""
        tmp = tmp.join(transcription)
        sentence += " " + tmp

    filler_words = getFillers(sentence)

    return getFillerFrequency(filler_words, sentence)


# returns a count of the filler words occuring in a sentence
def getFillerFrequency(fillers, sentence):
    count = 0

    for filler in fillers:
        count += sentence.count(filler)

    return count

def createReport(metrics,metrics_path):
    json_obj = json.dumps(metrics)
    with open(f'{metrics_path}report.json', "w") as outfile:
        outfile.write(json_obj)


####################################################################  DRIVER CODE #######################################################################


def getReport(audio_path, metrics_path,wait):
    metrics = {
        "average_clarity": 0,
        "total_filler_sounds_count": 0,
        "pitch": 0,
        "total_pause_count": 0,
        "average_wpm": 0,
        "total_filler_word_count": 0,
        "total_pause_time": 0,
        "total_bad_pause_count": 0,
        "total_word_count": 0,
        "total_time": 0
    }

    totalWaitTime = 0

    if(wait == '1'):
        total_audios = len(os.listdir(audio_path))
        total_metrics = len(os.listdir(metrics_path))
        while (total_metrics != total_audios and totalWaitTime < 30):
            print("Waiting for results to process at ", metrics_path)
            time.sleep(5)
            totalWaitTime += 5
            total_audios = len(os.listdir(audio_path))
            total_metrics = len(os.listdir(metrics_path))

    json_files = glob.glob(f'{metrics_path}*.json')
    totalFiles = len(json_files)

    if (totalFiles == 0):
        print("No JSON files found. Waiting 15 seconds...")
        time.sleep(15)
        json_files = glob.glob(f'{metrics_path}*.json')
        totalFiles = len(json_files)
        if (totalFiles == 0):
            print("Could not get report. No JSON files found. Returning empty metrics.")
            createReport(metrics,metrics_path)
            return totalFiles, metrics

    data_points = []
    for json_file in json_files:
        with open(json_file) as file:
            data_points.append(json.load(file))

    total_clarity = 0
    total_filler_sounds = 0
    total_pauses = 0
    total_wpm = 0
    total_pause_time = 0
    total_bad_pause_count=0
    total_time = 0
    total_word_count = 0
    transcriptions = []

    for data_point in data_points:
        total_clarity += int(data_point["clarity"])
        total_filler_sounds += int(data_point["filler_sounds"])
        total_pauses += int(data_point["pauses"])
        total_wpm += int(data_point["wpm"])
        total_pause_time += float(data_point["total_pause_time"])
        total_bad_pause_count += int(data_point["bad_pause_count"])
        total_time += int(data_point["total time"])
        total_word_count += int(data_point["word_count"])
        transcriptions.append(data_point["transcription"])


    total_filler_word_count = getFillerWordCount(transcriptions)


    metrics["average_clarity"] = total_clarity/totalFiles
    metrics["total_filler_sounds_count"] = total_filler_sounds
    metrics["total_pause_count"] = total_pauses
    metrics["average_wpm"] = total_wpm/totalFiles
    metrics["total_filler_word_count"] = total_filler_word_count
    metrics["total_pause_time"] = total_pause_time
    metrics["total_bad_pause_count"] = total_bad_pause_count
    metrics["total_word_count"] = total_word_count
    metrics["total_time"] = total_time


    createReport(metrics,metrics_path)
    return totalFiles, metrics



