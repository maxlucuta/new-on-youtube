import axios from "axios";
import { useState, useContext } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import img from "./img.png";
import "./signin.css";

const SignInPage = () => {
    const [username, updateUsername] = useState("");
    const [password, updatePassword] = useState("");
    const { SERVER_URL, updateUser } = useContext(RootContext);
    const navigate = useNavigate();

    const handleEmailChange = (e: any) => {
        updateUsername(e.target.value);
    };

    const handlePasswordChange = (e: any) => {
        updatePassword(e.target.value);
    };

    const handleSubmit = async () => {
        const payload = { username, password: password };
        const { message } = (await axios.post(SERVER_URL + "/login", payload)).data;
        console.log(message);
        if (message === "already logged in") navigate("/");
        else if (message === "invalid fields") alert("Incorrect input!");
        else if (message === "no username") alert("Incorrect username");
        else if (message === "incorrect password") alert("Incorrect password");
        else if (message === "logged in") {
            updateUser(username);
            navigate("/");
        }
    };

    return (
        <div className="signin_background">
            <div className="container">
                <div className="form">
                    <h2>SIGN IN</h2>
                    <input
                        type="email"
                        name="email"
                        className="box"
                        placeholder="Enter Email"
                        onChange={handleEmailChange}
                    />
                    <input
                        type="password"
                        name="password"
                        className="box"
                        placeholder="Enter Password"
                        onChange={e => handlePasswordChange(e)}
                    />
                    <SubmitButton
                        active={password.length > 0 && username.length > 0}
                        onClick={handleSubmit}>
                        SIGN UP
                    </SubmitButton>
                    <a href="#">Forgotten Password?</a>
                </div>
                <div className="side">
                    <img src={img} alt="" />
                </div>
            </div>
        </div>
    );
};

export default SignInPage;

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 12px 30px;
    width: 40%;
    margin-top: 40px;
    background-color: black;
    opacity: ${props => (props.active ? "1" : "0.2")};
    color: white;
    font-weight: bold;
    border: none;
    outline: none;
    border-radius: 20px;
    &:hover {
        cursor: ${props => (props.active ? "pointer" : "not-allowed")};
        background-color: ${props => (props.active ? "#750000" : "black")};
    }
`;
