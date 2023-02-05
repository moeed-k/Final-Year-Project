import React from 'react'
import "../Stylings/style.css"

import {

    Link
  } from "react-router-dom";

   

export default function Login() {
  

  return (
<div>    
    <div className="background">
  
    <nav className="NavigationBar">
        <div>
            <img src={process.env.PUBLIC_URL+"SpeakEasy1.png"} alt="Pic not found " width="100px" height ="100px" />
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
        <img src={process.env.PUBLIC_URL+"SpeakEasy1.png"} alt="Trulli" />
      </figure>
    
    <div className="formContainer" >   
        <h1 className="centralHeading">Log in</h1>
    <form action='/profile' method="post" >  
       
        <div className = "flexContainer">
            <i className="fa-solid fa-user makeCenter"></i>
            <input className="inputContainer" type="text" placeholder="Enter Username" name="username" required         defaultChecked={true}
/>   
        </div>
        <div className = "flexContainer">
            <i className="fa-solid fa-lock makeCenter"></i>
            <input className="inputContainer" type="password" placeholder="Enter Password" name="password" required         defaultChecked={true}
/>  
        </div>
        <Link to="/profile" id="profilelogin">
        <button type="submit" >Login</button> 
        </Link>
        <div className = "flexAllign">
            <div >
               
                  <input type="checkbox"   defaultChecked={true}/> Remember me   
                
            </div>  
            <a id="forget" href="#">  Forgot password? </a>  
        </div>
        <div className = "flexAllign" >
            <Link to="CreateAccount">Create Account</Link>
            <Link to="help"> Need Help</Link>
         </div>
     
    </form>    
    </div>  

    


   

</div> 


</div>

</div>
  )
}
