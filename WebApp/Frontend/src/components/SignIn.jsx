import React from 'react';

const SignIn = () => {
    return (
        <div className="flex items-center justify-center h-screen">
            <div className="bg-white p-8 shadow-md rounded-md w-full max-w-md">
                {/* Adjusted width using max-w-md class */}
                <h2 className="text-2xl font-bold mb-4">Sign In</h2>
                <form className="space-y-4">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email Address</label>
                        <input type="email" id="email" name="email" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
                    </div>
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                        <input type="password" id="password" name="password" className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
                    </div>
                    <button type="submit" className="w-full bg-gradient-to-r from-orange-500 via-pink-500 to-pink-800 py-2 px-4 rounded-md text-white font-medium hover:bg-gradient-to-r hover:from-orange-600 hover:via-pink-600 hover:to-pink-900">
                        Sign In
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SignIn;
