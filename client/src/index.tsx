import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RootContext } from "./context";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./HomePage/HomePage";
import SearchPage from "./SearchPage/SearchPage";
import FeedPage from "./FeedPage/FeedPage";
import RegisterPage from "./RegisterPage/RegisterPage";
import SignInPage from "./RegisterPage/SignInPage";
import { detectMobile, useToken } from "./functions";
import TimeOut from "./ClientErrorPages/TimeOut";
import TopicSelectionPage from "./TopicSelection/TopicSelection";
import UnsupportedDevice from "./ClientErrorPages/UnsupportedDevice";

const App = () => {
    // conditionally switched to production url in live
    const PRODUCTION = window.location.href.indexOf("newonyoutube.com") > -1;
    const TEST_DEPLOY = window.location.href.indexOf("new-on-youtube.herokuapp.com") > -1;

    const SERVER_URL = PRODUCTION
        ? "https://www.newonyoutube.com"
        : TEST_DEPLOY
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
            path: "/TopicSelection",
            element: <TopicSelectionPage />,
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
        {
            path: "/UnsupportedDevice",
            element: <UnsupportedDevice />,
        },
    ]);

    return (
        <React.StrictMode>
            <RootContext.Provider value={{ SERVER_URL, token, setToken }}>
                {detectMobile() ? <UnsupportedDevice /> : <RouterProvider router={router} />}
            </RootContext.Provider>
        </React.StrictMode>
    );
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);
