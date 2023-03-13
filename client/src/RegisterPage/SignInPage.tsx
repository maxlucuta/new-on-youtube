import { useContext, useEffect, useState } from "react";
import { useNavigate, Navigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import { usePost } from "../functions";
import NavBar from "../NavBar/Navbar";
import logo from "../assets/logoColour.png";
import { Link } from "react-router-dom";
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

const SignInPage = () => {
    const [username, updateUsername] = useState("");
    const [password, updatePassword] = useState("");
    const [userDoesNotExist, updateUserDoesNotExist] = useState(false);
    const [invalidPassword, updateInvalidPassword] = useState(false);
    const { setToken, token } = useContext(RootContext);
    const navigate = useNavigate();
    const post = usePost();
    const CustomAlert = withReactContent(Swal);

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
        if (message === "invalid fields") CustomAlert.fire({
            icon: "error",
            title: <AlertMessage>Please enter a username and password</AlertMessage>,
            });
        else if (message === "username not found") {
            updateInvalidPassword(false);
            updateUserDoesNotExist(true);
        } else if (message === "incorrect password") {
            updateInvalidPassword(true);
            updateUserDoesNotExist(false);
        } else if (message === "logged in") {
            setToken(res.token);
        }
    };

    if (token !== "") return <Navigate replace to="/Feed" />;

    return (
        <div className="signup_background">
            <NavBar />
            <PageFrame>
                <RegFrame>
                    <LogoImage src={logo} />
                    <Title>Sign in to your account</Title>
                    <div style={{ textAlign: "center" }}>
                        <RegForm>
                            <FormInput
                                type="email"
                                name="email"
                                placeholder="Enter Username"
                                onChange={handleEmailChange}
                            />
                            {userDoesNotExist ? <MessageText>Username not found, please try again</MessageText> : <p></p>}
                            <FormInput
                                type="password"
                                name="password"
                                placeholder="Enter Password"
                                onChange={e => handlePasswordChange(e)}
                            />
                            {invalidPassword ? <MessageText>Invalid password, please try again</MessageText> : <p></p>}
                        </RegForm>

                        <SubmitButton
                            active={password.length > 0 && username.length > 0}
                            onClick={handleSubmit}>
                            SIGN IN
                        </SubmitButton>
                        <MessageText>Don't have an account yet?&nbsp;&nbsp;
                            <Link to="/Register" style={{color: "var(--colour-pink-accent"}}>Register</Link>
                        </MessageText>
                    </div>
                </RegFrame>
            </PageFrame>
        </div>
    );
};

export default SignInPage;

const MessageText = styled.p`
    font-size: 13px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
`

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 15px;
    width: 90%;
    margin-top: 10px;
    margin-bottom: 10px;
    background-color: var(--colour-pink-accent);
    color: white;
    font-weight: bold;
    border: none;
    outline: none;
    border-radius: 3px;
    &:hover {
        cursor: pointer;
    }
`;

const Title = styled.div`
    text-align: center;
    padding-top: 30px;
    padding-bottom: 15px;
    font-size: 30px;
    font-weight: 500;
    font-family: 'Rubik', sans-serif;
`;

const PageFrame = styled.div`
    display: flex;
    justify-content: center;
    width: 80%;
    padding-top: 50px;
    margin: 0 auto 0 auto;
`;

const RegFrame = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: none;
    width: 75%;
`;

const RegForm = styled.form`
    background-color: none;
    border-radius: 10px;
`;

const FormInput = styled.input`
    padding: 12px;
    width: 80%;
    margin: 8px;
    border: 1px solid grey;
    border-radius: 3px;
    outline: none;  
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
`;

const LogoImage = styled.img`
    width: 75px;
    margin-top: 50px;
`;

const AlertMessage = styled.div`
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif
`;