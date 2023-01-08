import React from 'react'
import "../Stylings/taketest.css"
import {

    Link
  } from "react-router-dom";

export default function Test() {
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
                <Link a="/recommendation">
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
                <video src="vid1.mp4" controls className='video1' height="90%" width="100%"></video>
                <div className='buttons'>
                    <button type="button" className='next'>
            <span className = 'next_text'>Previous</span>
            <span className="material-symbols-outlined">
                skip_previous
            </span>
        </button>
                    <button type="button" className='next'>
            <span className="material-symbols-outlined">
                skip_next
            </span>
            <span className = 'next_text'>Next</span>
        </button>
                    <button type="button" className='stop'>
            <span className="material-symbols-outlined">
                stop_circle
            </span>
            <span className = 'stop_text'>End Recording</span>
        </button>
                    <button type="button" className='stop'>
            <span className="material-symbols-outlined">
                delete_forever
            </span>
            <span className = 'stop_text'>Cancel</span>
             </button>
                </div>
        </div>

        </div>
    </div>
</div>
</div>
)}
