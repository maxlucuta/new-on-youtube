import axios from "axios";
import { useState, useContext } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import NavBar from "../NavBar/Navbar";
import img from "./img.png";
import "./signin.css";

const SignInPage = () => {
    const [username, updateUsername] = useState("");
    const [password, updatePassword] = useState("");
    const [userDoesNotExist, updateUserDoesNotExist] = useState(false);
    const [invalidPassword, updateInvalidPassword] = useState(false);
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
        if (message === "user already logged in") alert("You are already logged in. Go to /logout to logout");
        else if (message === "did not provide all fields") alert("Please enter a username and password");
        else if (message === "username does not exist in db") updateUserDoesNotExist(true);
        else if (message === "incorrect password") {
            updateInvalidPassword(true);
            updateUserDoesNotExist(false);
        } else if (message === "logged in") {
            updateUser(username);
            navigate("/");
        }
    };

    return (
        <div className="signin_background">
            <NavBar />
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
                    {userDoesNotExist ? <div>Username not found, please try again"</div> : <div></div>}
                    <input
                        type="password"
                        name="password"
                        className="box"
                        placeholder="Enter Password"
                        onChange={e => handlePasswordChange(e)}
                    />
                    {invalidPassword ? <div>Invalid password, please try again</div> : <div></div>}
                    <SubmitButton
                        active={password.length > 0 && username.length > 0}
                        onClick={handleSubmit}>
                        SIGN IN
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
