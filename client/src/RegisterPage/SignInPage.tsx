import { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import { usePost } from "../functions";
import NavBar from "../NavBar/Navbar";
import "./signin.css";

const SignInPage = () => {
    const [username, updateUsername] = useState("");
    const [password, updatePassword] = useState("");
    const [userDoesNotExist, updateUserDoesNotExist] = useState(false);
    const [invalidPassword, updateInvalidPassword] = useState(false);
    const { setToken, token } = useContext(RootContext);
    const navigate = useNavigate();
    const post = usePost();

    const handleEmailChange = (e: any) => {
        updateUsername(e.target.value);
    };

    const handlePasswordChange = (e: any) => {
        updatePassword(e.target.value);
    };

    const handleSubmit = async () => {
        const payload = { username, password: password };
        const res = (await post("/login", payload)) as any;
        const message = res.message;
        console.log(message);
        if (message === "invalid fields") alert("Please enter a username and password");
        else if (message === "username not found") {
            updateInvalidPassword(false);
            updateUserDoesNotExist(true);
        } else if (message === "incorrect password") {
            updateInvalidPassword(true);
            updateUserDoesNotExist(false);
        } else if (message === "logged in") {
            setToken(res.token);
            navigate("/Feed");
        }
    };

    if (token !== "") return <Navigate replace to="/" />;

    return (
        <div className="signup_background">
            <NavBar />
            <PageFrame>
                <RegFrame>
                    <div style={{ textAlign: "center" }}>
                        <Title>Sign in</Title>
                        <RegForm>
                            <FormInput
                                type="email"
                                name="email"
                                placeholder="Enter Email"
                                onChange={handleEmailChange}
                            />
                            {userDoesNotExist ? <div>Username not found, please try again</div> : <div></div>}
                            <FormInput
                                type="password"
                                name="password"
                                placeholder="Enter Password"
                                onChange={e => handlePasswordChange(e)}
                            />
                            {invalidPassword ? <div>Invalid password, please try again</div> : <div></div>}
                        </RegForm>


                        <SubmitButton
                            active={password.length > 0 && username.length > 0}
                            onClick={handleSubmit}>
                            SIGN IN
                        </SubmitButton>
                    </div>
                </RegFrame>
            </PageFrame>
        </div>
    );
};

export default SignInPage;

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 12px 30px;
    width: 65%;
    margin: 40px;
    background-color: black;
    opacity: ${props => (props.active ? "1" : "0.2")};
    color: white;
    font-weight: bold;
    border: none;
    outline: none;
    border-radius: 5px;
    &:hover {
        cursor: ${props => (props.active ? "pointer" : "not-allowed")};
        background-color: ${props => (props.active ? "#e52b87" : "black")};
    }
`;

const Title = styled.div`
    text-align: center;
    padding-top: 30px;
    padding-bottom: 15px;
    font-size: 25px;
    font-weight: 500;
    font-family: 'Rubik', sans-serif;
`;

const PageFrame = styled.div`
    display: flex;
    justify-content: center;
    width: 80%;
    max-height: 100vh;
    padding-top: 75px;
    padding-left: 10%;
    padding-right: 10%;
    margin: 0 auto 0 auto;
`;

// RegFrame after back-col -> background-image: ${smoke};
const RegFrame = styled.div`
    display: flex;
    flex-direction: column;
    background-color: #f0f0f1;
    width: 75%;
    border-radius: 3px;
    margin-bottom: 40px;
    filter: drop-shadow(0 0.3rem 0.25rem grey);
    opacity: 0;
    animation: fade-in 1s ease-in-out forwards;
    animation-delay: 0.3s;

    @keyframes fade-in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
`;
const RegForm = styled.form`
    background-color: none;
    border-radius: 10px;
`;

const FormInput = styled.input`
    padding: 12px;
    width: 65%;
    margin: 15px;
    border: 1px solid black;
    outline: none;
    border-radius: 5px;
    background-color: #f0f0f1;
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
`;