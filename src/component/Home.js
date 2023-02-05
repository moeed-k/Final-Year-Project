import React from 'react'
import "../Stylings/style2.css"


import {
 
    Link
  } from "react-router-dom";
export default function Home() {
   
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
                    <Link to="/home"> <span className="material-symbols-outlined">
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
                            </span>
                            Analytics</Link>
                </li>
                <li className="sidebuttonBlock">
                    <Link to="/recommendation">
                        <span className="material-symbols-outlined">
                            recommend
                            </span>
                        Recommend Exercises
                        </Link>
                </li>
            </ul>
        </div>
        <div className="contents">

        <div className="Home">
                <h1>Welcome to SpeakEasy</h1>
                <div className="textContainer">
                    <h2>About us</h2>
                    <p>Speak Easy is an soft skill training system that uses Computer vision and natural language processing to improve the communication skills of the person </p>

            
                </div>
                <div className="textContainer">
                    <h2> How it Works?</h2>
                    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Sit minus dicta nobis quibusdam nemo nostrum ducimus fugit consequuntur quae cupiditate sapiente necessitatibus, asperiores architecto accusamus perspiciatis provident. Qui,
                        expedita dolore. Aut, it laboriosam
                        modi.</p>

            
                </div>
            </div>
        

        </div>

    </div>

    

    
</div>


  )

}