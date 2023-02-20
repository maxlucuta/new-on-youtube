import axios from "axios";
import React, { createContext, useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RootContext } from "./context";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./HomePage/HomePage";
import SearchPage from "./SearchPage/SearchPage";
import FeedPage from "./FeedPage/FeedPage";
import RegisterPage from "./RegisterPage/RegisterPage";
import SignInPage from "./RegisterPage/SignInPage";
import { useToken } from "./functions";
import TimeOut from "./TimeOut/TimeOut";

const App = () => {
    // conditionally switched to production url in live
    const PRODUCTION = window.location.href.startsWith("https://new-on-youtube.herokuapp.com");
    const SERVER_URL = PRODUCTION
        ? "https://new-on-youtube.herokuapp.com"
        : "http://localhost:5000";

    
    const {token, setToken} = useToken()

    const router = createBrowserRouter([
        {
            path: "/",
            element: <HomePage />,
        },
        {
            path: "/Search",
            element: <SearchPage />,
        },
        {
            path: "/Feed",
            element: <FeedPage />,
        },
        {
            path: "/Register",
            element: <RegisterPage />,
        },
        {
            path: "/SignIn",
            element: <SignInPage />,
        },
        {
            path: "/TimeOut",
            element: <TimeOut />,
        },
    ]);

    return (
        <React.StrictMode>
            <RootContext.Provider value={{ SERVER_URL, token, setToken }}>
                <RouterProvider router={router} />
            </RootContext.Provider>
        </React.StrictMode>
    );
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);
