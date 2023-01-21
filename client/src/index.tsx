import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RootContext } from "./context";
import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";
import HomePage from "./Pages/HomePage";

// conditionally switched to production url in live
const SERVER_URL = "http://localhost:5000";

const router = createBrowserRouter([
	{
		path: "/",
		element: <HomePage />,
	},
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
	<React.StrictMode>
		<RootContext.Provider value = {{ SERVER_URL }}>
			<RouterProvider router={router} />
		</RootContext.Provider>
	</React.StrictMode>
);