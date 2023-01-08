
import React from "react";
import Login from "./component/login";

import BarChart from "./component/BarChart";
import { useState } from "react";
import { BrowserRouter as Router} from "react-router-dom";
import { Routes, Route } from "react-router-dom";
import Signup  from "./component/signup";
import Home from './component/Home';
import Analytics from "./component/Analytics";
import Test from "./component/Test";
function App() {
   
    return ( 
        <React.StrictMode>
            <Router>
                 <Routes>
                    <Route path="/" element={<Login />}/>
                    <Route path="/login" element={<Login />}/>
                    <Route path="/About" element={<p>welcome to About</p>}/>
                    <Route path="/ContactUs" element={<p>Welcome to Contact us</p>}/>
                    <Route path="/login/CreateAccount" element={<Signup/>}/>
                    <Route path="/login/help" element={<p>help</p>}/>
                    <Route path="/login/home" element={<p>help</p>}/>
                    <Route path="/home" element={<Home />}/>
                    <Route path="/profile" element={<Home/>}/>
                    <Route path="/analytic" element={<Analytics/>}/>
                    <Route path="/Test" element={<Test/>}/>
                </Routes>
            </Router>
        </React.StrictMode>
    
    );
}


export default App;