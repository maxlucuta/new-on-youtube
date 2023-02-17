import axios from "axios";
import React, { createContext, useState } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RootContext } from "./context";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./HomePage/HomePage";
import SearchPage from "./SearchPage/SearchPage";
import FeedPage from "./FeedPage/FeedPage";
import RegisterPage from "./RegisterPage/RegisterPage";
import SignInPage from "./RegisterPage/SignInPage";

const App = () => {
    // conditionally switched to production url in live
    const PRODUCTION = window.location.href.startsWith("https://new-on-youtube.herokuapp.com");
    const SERVER_URL = PRODUCTION
        ? "https://new-on-youtube.herokuapp.com"
        : "http://localhost:5000";

    const loggedInFunc = async () => {
        const { message } = (await axios.post(SERVER_URL + "/logged_in", {})).data;
        console.log("Logged in: ", message)
    }
    loggedInFunc();
    const [user, updateUser] = useState("");
    console.log("this was run")
    console.log(user)


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
    ]);

    return (
        <React.StrictMode>
            <RootContext.Provider value={{ SERVER_URL, user, updateUser }}>
                <RouterProvider router={router} />
            </RootContext.Provider>
        </React.StrictMode>
    );
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);
