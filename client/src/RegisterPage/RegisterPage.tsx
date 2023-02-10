import axios from "axios";
import { useContext, useState } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import NavBar from "../NavBar/Navbar";
import img from "./img.png";
import "./register.css";

const RegisterPage = () => {
    const [username, updateUsername] = useState("");
    const [password1, updatePassword1] = useState("");
    const [password2, updatePassword2] = useState("");
    const [userAlreadyExists, updateUserAlreadyExists] = useState(false);
    const { SERVER_URL } = useContext(RootContext);
    const navigate = useNavigate();

    const handleEmailChange = (e: any) => {
        updateUsername(e.target.value);
    };

    const handlePasswordChange = (e: any, idx: number) => {
        idx === 0 ? updatePassword1(e.target.value) : updatePassword2(e.target.value);
    };

    const handleSubmit = async () => {
        const payload = { username, password: password1, confirmation: password2 };
        const { message } = (await axios.post(SERVER_URL + "/register", payload)).data;
        if (message === "already logged in") navigate("/");
        if (message === "invalid fields") alert("Incorrect input!");
        if (message === "already exists") updateUserAlreadyExists(true);
        if (message === "successfully added") navigate("/SignIn");
    };

    const validPassword = password1.length !== 0 && password1 === password2;

    return (
        <div className="signin_background">
            <NavBar />
            <div className="container">
                <div className="form">
                    <h2>REGISTER</h2>
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
                        onChange={e => handlePasswordChange(e, 0)}
                    />
                    <input
                        type="password"
                        name="confirm password"
                        className="box"
                        placeholder="Confirm Password"
                        onChange={e => handlePasswordChange(e, 1)}
                    />
                    {!validPassword
                        ? password2.length > 0 && <div>Passwords do not match</div>
                        : password2.length > 0 && <div>Valid password!</div>}
                    <SubmitButton
                        active={validPassword && username.length > 0}
                        onClick={handleSubmit}>
                        SIGN UP
                    </SubmitButton>
                </div>
                <div className="side">
                    <img src={img} alt="" />
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;

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
