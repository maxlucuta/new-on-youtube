import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RootContext } from "./context";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./HomePage/HomePage";
import SearchPage from "./SearchPage/SearchPage";
import FeedPage from "./FeedPage/FeedPage";
import RegisterPage from "./RegisterPage/RegisterPage";
import SignInPage from "./RegisterPage/SignInPage";

// conditionally switched to production url in live
const PRODUCTION = !window.location.href.startsWith("http://localhost");
const SERVER_URL = PRODUCTION ? "https://new-on-youtube.herokuapp.com" : "http://localhost:5000";
var user = "";
const updateUser = (n: string) => {
    console.log("user updated!");
    user = n;
};

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

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
    <React.StrictMode>
        <RootContext.Provider value={{ SERVER_URL, user, updateUser }}>
            <RouterProvider router={router} />
        </RootContext.Provider>
    </React.StrictMode>
);
