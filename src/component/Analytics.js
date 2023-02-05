import React from 'react'
import "../Stylings/style2.css"
import {useState} from 'react';
import BarChart from '../component/BarChart.js';
import LineChart from '../component/LineChart.js';

import {
    Link
  } from "react-router-dom";
export default function Analytics() {
    const [chartData, setChartData] = useState({
        labels: ["Authenticity", "Confidence", "Persuasion"], 
        datasets: [
          {
            label: "Scores ",
            data: [50, 40, 80],
            borderWidth: 1,
            backgroundColor: [
              'rgba(168, 98, 189, 0.566)'
              
            ],
          }
        ]
      });
    

 
      const [chartData3, setChartData3] = useState({
        labels: ['', '', '', '','', '', '', ''],
      datasets: [{
        label: 'Pitch 1',
        data: [5, 4, 8, 1 ,10, 11, 2, 4],
        borderWidth: 1

      },
     {
        label: 'Pitch 2',
        data: [50, 40, 81, 11 ,40, 70, 20, 4],
        borderWidth: 1
        

      }
    
    ]
      });

      const [chartData2, setChartData2] = useState({
        labels: ['January', 'Febuary', 'March', 'April','May', 'June', 'July', 'August'],
      datasets: [{
        label: 'Number Of Tests',
        data: [5, 4, 8, 1 ,10, 11, 2, 4],
        borderWidth: 1,
        backgroundColor: [
          'rgba(168, 98, 189, 0.566)'
          
        ]
      }]
      });

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

        <div className="Analytics">
                <div className="Graphs">
                    <div className="Graph1">
                        <h1>Soft Skils</h1>
                        <BarChart chartData={chartData} />
                    </div>
                    <div className="Graph3">
                        <h1>Number Of Tests</h1>
                        <br/>
                        <LineChart chartData={chartData2} />
                        
                    </div>
                    <div className="Graph2">
                        <h1>Pitch</h1>
                        <br/>
                        <LineChart chartData={chartData3} />
                    </div>
                </div>


                <div id="averageHeading">
                    <h1>Average Per Minute Stats</h1>
                </div>

                <div className="averageBoxes">
                    <div id="wpm" className="boxes">
                        <p>WPM : 130</p>
                    </div>
                    <div id="Pause" className="boxes">
                        <p>Pauses: 3 </p>

                    </div>
                    <div id="FillerWords" className="boxes">
                        <p>Filler Words: 3</p>


                    </div>
                    <div id="FillerSounds" className="boxes">
                        <p>Filler Sounds:3</p>

                    </div>
                    <div id="Clarity" className="boxes">
                        <p>Clarity:60%</p>

                    </div>
                </div>

                <div id="ShowReports">
                    <a href="#">
                         Click to View Report History
                         
                    </a>
     
                 </div>
            </div> 

        </div>

    </div>

    

    
</div>


  )

}