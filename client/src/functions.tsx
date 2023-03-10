import { useContext, useState } from "react";
import jwt from 'jwt-decode'
import { RootContext } from "./context";
import axios from "axios";
import { useNavigate } from "react-router";

// broken id example _jVQ_pFxdrM

export const thumbnail = (id: string) => "https://img.youtube.com/vi/" + id + "/hqdefault.jpg";
export const url = (id: string) => "http://www.youtube.com/watch?v=" + id;
export const MAX_TOPICS = 20;

export const useToken = () => {
    const getToken = () => {
        const token = sessionStorage.getItem("token");
        return token ? token : "";
    };

    const [token, setToken] = useState(getToken());

    const saveToken: (userToken: string) => void = userToken => {
        sessionStorage.setItem("token", userToken);
        setToken(userToken);
    };

    return { token, setToken: saveToken };
};

export const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

export const tokenToEmail = (token: string) => {
    return (jwt(token) as any).sub
}

export const usePost = () => {
    const { SERVER_URL, token, setToken } = useContext(RootContext);
    const navigate = useNavigate();

    const post = async (endpointUrl: string, data: Object) => {
        const headers = { 'Authorization': "Bearer " + token }
        try {
            const response = (await axios.post(SERVER_URL + endpointUrl, data, { headers })).data
            // refreshed token returned by server
            setToken(response.token ? response.token : token)
            return response
        } catch(error: any) {
            if (error.response.status !== 401) return alert("Unknown error")
            // access denied by server
            console.log(error);
            setToken("")
            navigate("/TimeOut")
        }
    }

    return post;
}

export const detectMobile = () => {
    const toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
    ];
    
    return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem);
    });
}