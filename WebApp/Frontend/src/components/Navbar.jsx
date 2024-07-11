import React, { useState } from 'react';
import logo from "../assets/logo.png";
import { navItems } from "../constants";
import SignIn from './SignIn';
import CreateAccount from './CreateAccount'; 

const Navbar = () => {
    const [showSignIn, setShowSignIn] = useState(false);
    const [showCreateAccount, setShowCreateAccount] = useState(false); 

    const toggleSignIn = () => {
        setShowSignIn(!showSignIn);
        setShowCreateAccount(false); // Ensure only one component is shown at a time
    };

    const toggleCreateAccount = () => {
        setShowCreateAccount(!showCreateAccount);
        setShowSignIn(false); // Ensure only one component is shown at a time
    };

    return (
        <nav className="sticky top-0 z-50 py-3 backdrop-blur-lg border-b border-neutral-700/80">
            <div className="container px-4 mx-auto relative lg:text-sm">
                <div className="flex justify-between items-center">
                    <div className="flex items-center flex-shrink-0">
                        <img className="h-14 w-55 mr-2" src={logo} alt="Logo" />
                    </div>
                    <ul className="hidden lg:flex ml-14 space-x-12">
                        {navItems.map((item, index) => (
                            <li key={index}>
                                <a href={item.href} className="hover-underline-gradient text-lg">{item.label}</a>
                            </li>
                        ))}
                    </ul>
                    <div className="hidden lg:flex justify-center space-x-12 items-center">
                        <button onClick={toggleSignIn} className="py-2 px-3 border rounded-md hover-border-gradient">
                            Sign In
                        </button>
                        <button
                            onClick={toggleCreateAccount}
                            className="bg-gradient-to-r from-orange-500 via-pink-500 to-pink-800 py-2 px-3 rounded-md text-white hover:bg-gradient-to-r hover:from-orange-600 hover:via-pink-600 hover:to-pink-900 transition duration-300"
                            // Added hover effect classes
                        >
                            Create an account
                        </button>
                    </div>
                </div>
            </div>
            {showSignIn && <SignIn />}
            {showCreateAccount && <CreateAccount />} {/* Render CreateAccount component based on showCreateAccount state */}
        </nav>
    );
};

export default Navbar;
