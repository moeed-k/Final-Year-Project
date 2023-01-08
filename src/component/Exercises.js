import React from 'react'
import "../Stylings/recommend.css"
import {
 
    Link
  } from "react-router-dom";
export default function Exercises() {
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
            <div className="test">
            </div>
            <div className='recommendouter'>
                <div className='feedbackHeading'>
                    <div className='feedbackText'>
                        <b>Training Feedback</b>
                    </div>
                </div>
                <div className='points'>
                    <div className='positivePoints'>
                        <div className='p_pointsHeadingFlex'>
                            <span className='positive_pointsHeading'><b>Positive Points</b></span>
                            <span className="material-symbols-outlined">
                        check_circle
                    </span>
                        </div>
                        <div className='pointsListFlex'>
                            <ul className='bullet'>
                                <li>Maintained good eye contact</li>
                                <li>Good Speech Rate</li>
                            </ul>
                        </div>
                    </div>

                    <div className='negativePoints'>
                        <div className='n_pointsHeadingFlex'>
                            <span className='negative_pointsHeading'><b>Negative Points</b></span>
                            <span className="material-symbols-outlined">
                        cancel
                    </span>
                        </div>
                        <div className='pointsListFlex'>
                            <ul className='bullet'>
                                <li>Voice was not clear</li>
                                <li>Too many filler words were used</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div className='recommendList'>
                    <div className='p_pointsHeadingFlex'>
                        <span className='positive_pointsHeading'><b>Recommendations</b></span>
                        <span className="material-symbols-outlined">
                    tips_and_updates
                </span>
                    </div>
                    <ul className='bullet'>
                        <li>
                            Try to pronounce your words more clearly
                        </li>
                    </ul>
                </div>
            </div>
</div>
</div>
</div>
  )
}
