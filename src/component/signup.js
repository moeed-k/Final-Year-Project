import React from 'react'
import "../Stylings/style.css"

import {
  
    Link
  } from "react-router-dom";

export default function Signup() {


  return (

<div>


    <div className="background">
  
    <nav className="NavigationBar">
        <div>
            <img src="../../SpeakEasy1.png" alt="Pic not found " width="100px" height ="100px" />
        </div>
        <ul>
            <li>
                <Link to="/login">Login</Link>
            </li>
            <li> 
                <Link to="/About"> About</Link>
            </li>
            <li> 
                <Link to="/ContactUs"> Contact us</Link>
            </li>
        </ul>
      
    </nav>

    <div >
    <figure className ="formImage">
        <img src="../../SpeakEasy1.png" alt="Trulli" />
      </figure>
    
  

    
    <div className="SignupformContainer" >   
        <h1 className="centralHeading">Sign Up</h1>
        <form>  
           
            <div className = "flexContainer">
            
                <input className="inputContainer" type="text" placeholder="Enter Username" name="username" required defaultChecked={true} />   
            </div>
            <div className = "flexContainer">
              
                <input className="inputContainer" type="password" placeholder="Enter New Password" name="password" required defaultChecked={true}/>  
            </div>
            <div className = "flexContainer">
             
                <input className="inputContainer" type="text" placeholder="Confirm New Password" name="username" required defaultChecked={true}/>   
            </div>
            <div className = "flexContainer">
              
                <input className="inputContainer" type="password" placeholder="Enter Email" name="password" required defaultChecked={true}/>  
            </div>
            <button type="submit">Sign up</button> 
          
         
         </form>    
        </div>  
    


   

</div> 


</div>

</div>
  )
}
