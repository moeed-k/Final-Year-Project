import React from 'react';
import {useState, useRef,useEffect} from 'react'
import "../Stylings/taketest.css";
// import  MediaRecorder from "./MediaRecorder"
import { useReactMediaRecorder } from "react-media-recorder";

import {

    Link
  } from "react-router-dom";

export default function Test() {
    const [isPlaying, setIsPlaying] = useState(false);
    const videoRef = useRef(null);
    const [Number, setNumber] = useState(0);
    const [QuestionPath, setQuestionPath] = useState(["http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4","b.mp4"]);
    const [currentVideo, setCurrentVideo] = useState(QuestionPath[Number]);
    const { status, startRecording, stopRecording, mediaBlobUrl } =useReactMediaRecorder({ video: true });




    useEffect(() => {
        setCurrentVideo(QuestionPath[Number]);
        console.log("Number is "+Number);
        videoRef.current.load();
        startRecording();
        stopRecording();
      }, [Number]);
      

    async function convertMediaBlobUrlToBlob(url) {// Converting the blob url to blob
        const response = await fetch(url)
        .then(response => response.blob())
        .then(response => {
            const file=new File([response], "video.webm", {type: "video/webm"});
            console.log("File is "+file);
            const videoElement = document.createElement('video');
            videoElement.controls = true;
            videoElement.src = URL.createObjectURL(file);
            document.body.appendChild(videoElement);
            return file;
        })
    }

    const SendVideotoServer=(File)=>{// File is the blob file Making API call to the server
        const form = new FormData();
        form.append('file', File);
        console.log("Form is "+form);
        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: form
        })
        .then(response => response.json())
        .then(response => {
            console.log("Response is "+response);
        }
        )
    }

    const togglePlay = () => {
        startRecording();

          if (isPlaying) {
            videoRef.current.pause();
          } else {
            videoRef.current.play();
          }
            setIsPlaying(!isPlaying);
      };
      const ProcessRecording = () => {
        videoRef.current.pause();
        stopRecording();
        console.log("Stop Recording");
        
        console.log("Media Blob URL is "+mediaBlobUrl);

        // Way to convert the blob url to blob
        convertMediaBlobUrlToBlob(mediaBlobUrl);
          
        
    
      };
 
    const changeQuestion=()=>{
        if(Number===0)
        {
          setNumber(1);
        }
        else
        {
          setNumber(0);
        }
        console.log("Clicked the change Question ");
    }

    
   



  return (
<div>
<nav className="NavigationBar">
    <div id="logo">
        <a href="#">
            <img src="./SpeakEasy1.png" alt="Pic not found " width="100px" height="100px"/>
        </a>
    </div>
    <ul className="ButtonList">
        <li className="buttonBlock">
            <div className="dropdown">
                <button className="dropbtn"> 
                    <div id="accountDetails">
                        <img src="./SpeakEasy1.png" alt="none" width="20px" height="15px"/> 
                        Wasay Rizwani 
                        <span className="material-symbols-outlined">
                            arrow_drop_down
                        </span>
                </div>

                </button>
                <div className="dropdown-content">
                    <a href="#">Account Details</a>
                    <a href="#">About us</a>
                    <a href="#">Help</a>
                </div>
            </div>
        </li>

    </ul>

</nav>

<div className="container">

    <div className="sidebar">
        <ul className="sideButtonList">
            <li className="sidebuttonBlock">
                <Link
 to="/home"> <span className="material-symbols-outlined">
                    home
                    </span>Home</Link>
            </li>
            <li className="sidebuttonBlock">
                <Link to="/test"><span className="material-symbols-outlined">
                    quiz
                    </span>Take a Test</Link>
            </li>
            <li className="sidebuttonBlock">
                <Link to="/analytic">
                    <span className="material-symbols-outlined">
                        rule
                        </span>Analytics</Link>
            </li>
            <li className="sidebuttonBlock">
                <Link to="/recommendation">
                    <span className="material-symbols-outlined">
                        recommend
                        </span> Recommend Exercises
                </Link>
            </li>
        </ul>
    </div>
    <div className="contents">
        <div className='testHeading'>

            <div className='testHeadingText1'>
                Video Test
            </div>
            <div className='testHeadingText2'>
                Please answer the following questions
            </div>
        </div>
        <div className='vidflexouter'>
            <div className='vidflex'>
            {/* height="90%" width="100%" */}
            {/* <video>
                <source src={video1} type='video/mp4' />
                    Sorry, your browser doesn't support videos.
            </video> */}
            <video ref={videoRef} width="100%">
                <source id = "videosource" src={currentVideo} type="video/mp4" />
            </video>

            <div className='buttons'>

                <button type="button" className='start' onClick={togglePlay}>
                    <span className="material-symbols-outlined">
                        play_circle
                    </span>
           
                    <span className = 'start_text'>Start Recording</span>
                </button>

                <button type="button" onClick={ProcessRecording} className='stop'>
                    <span className="material-symbols-outlined">
                        stop_circle
                    </span>
                    <span className = 'stop_text'>End Recording</span>
                </button>

                <button type="button"  className='stop'>
                    <span className="material-symbols-outlined">
                        delete_forever
                    </span>
                    <span className = 'stop_text'>Cancel</span>
                </button>


                <button type="button" className='next' onClick={changeQuestion}>
                    <span className="material-symbols-outlined">
                        skip_next
                    </span>
                    <span className = 'next_text'>Next</span>
                </button>

            </div>
        </div>

        </div>
    </div>
</div>

</div>
)}
