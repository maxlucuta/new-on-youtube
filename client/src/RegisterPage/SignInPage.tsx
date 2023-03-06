import { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router";
import styled from "styled-components";
import { RootContext } from "../context";
import { usePost } from "../functions";
import NavBar from "../NavBar/Navbar";
import logo from "../assets/logoColour.png";
import { Link } from "react-router-dom";

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
                    <LogoImage src={logo} />
                    <Title>Sign in to your account</Title>
                    <div style={{ textAlign: "center" }}>
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
                        <RegisterText>Don't have an account yet?&nbsp;&nbsp;
                            <Link to="/Register" style={{color: "var(--colour-pink-accent"}}>Register</Link>
                        </RegisterText>
                        <Division data-content="OR"/>
                    </div>
                </RegFrame>
            </PageFrame>
        </div>
    );
};

export default SignInPage;

const RegisterText = styled.p`
    font-size: 12px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
`

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 15px;
    width: 90%;
    margin-top: 20px;
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
    padding-top: 75px;
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
    margin: 15px;
    border: 1px solid grey;
    border-radius: 3px;
    outline: none;  
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
    &:focus {
        border-color: red;
        outline: 0;
    };
`;

const LogoImage = styled.img`
    width: 75px;
    margin-top: 50px;
`;

const Division = styled.hr`
    line-height: 1em;
    position: relative;
    outline: 0;
    border: 0;
    color: black;
    text-align: center;
    height: 1.5em;
    opacity: .5;
    &:before {
        content: '';
        background: grey;
        position: absolute;
        left: 0;
        top: 50%;
        width: 100%;
        height: 1px;
        }
    &:after {
        content: attr(data-content);
        position: relative;
        display: inline-block;
        color: black;

        padding: 0 .5em;
        line-height: 1.5em;
        color: #818078;
        background-color: #fcfcfa;
        }
`;