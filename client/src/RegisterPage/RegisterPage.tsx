import { useContext, useEffect, useState } from "react";
import { useNavigate, Navigate } from "react-router";
import Select, { ActionMeta, MultiValue } from "react-select";
import styled from "styled-components";
import { RootContext } from "../context";
import { usePost, MAX_TOPICS } from "../functions";
import NavBar from "../NavBar/Navbar";
import logo from "../assets/logoColour.png";
import { Link } from "react-router-dom";
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

type SelectOption = {
    label: string;
    value: string;
}

const RegisterPage = () => {
    const [username, updateUsername] = useState("");
    const [password1, updatePassword1] = useState("");
    const [password2, updatePassword2] = useState("");
    const [userAlreadyExists, updateUserAlreadyExists] = useState(false);
    const [passwordTooShort, updatePasswordTooShort] = useState(false);
    const [searchBarValue, updateSearchBarValue] = useState("");
    // const [filteredTopicSelection, updateFilteredTopicSelection] = useState(topics as string[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[]);
    const [selectedTopics, updateSelectedTopics] = useState([] as string[]);
    const { token, setToken } = useContext(RootContext);
    const navigate = useNavigate();
    const post = usePost();
    const CustomAlert = withReactContent(Swal);

    const handleEmailChange = (e: any) => {
        updateUsername(e.target.value);
        updateUserAlreadyExists(false)
    };

    const handlePasswordChange = (e: any, idx: number) => {
        idx === 0 ? updatePassword1(e.target.value) : updatePassword2(e.target.value);
        updatePasswordTooShort(false);
    };

    // const handleSearchBar = (e: any) => {
    //     updateSearchBarValue(e.target.value);
    //     if (e.target.value.length !== 0) {
    //         updateFilteredTopicSelection(topics.filter(c => c.startsWith(e.target.value)));
    //     } else {
    //         updateFilteredTopicSelection(topics);
    //     }
    // };

    const handleSelectedTopics = (c: string) => {
        if (!selectedTopics.includes(c)) {
            updateSelectedTopics(selectedTopics.concat([c]));
        } else {
            updateSelectedTopics(s => s.filter(cat => cat !== c));
        }
        console.log(selectedTopics)
    };

    const getAvailableTopics = async () => {
        const response = (await post("/unique_topics", {}));
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateAvailableTopics(response.topics);
    }

    useEffect(() => {
        getAvailableTopics();
    }, []);

    const handleChange = (newValue: MultiValue<SelectOption>, actionMeta: ActionMeta<SelectOption>) => {
        if (newValue.length > MAX_TOPICS) CustomAlert.fire({
            icon: "error",
            title: <AlertTitle>Sorry, you can't add more than {MAX_TOPICS} topics</AlertTitle>,
            });
        else updateSelectedTopics(newValue.map(nv => nv.value));
    }

    const handleSubmit = async () => {
        if (password1.length < 8) {
            updatePasswordTooShort(true);
            return;
        }
        const payload = { username: username, password: password1, confirmation: password2, topics: selectedTopics };
        const res = await post("/register", payload) as any;
        const message = res.message;
        console.log(message)
        if (message === "invalid fields") alert("Please enter a username, password, and matching password confirmation");
        if (message === "username already in use") updateUserAlreadyExists(true);
        if (message === "no topics selected") CustomAlert.fire({
            icon: "error",
            title: <AlertTitle>Please select at least one topic</AlertTitle>,
            text: "So that we can add some videos to your feed"
            });
        if (message === "successfully added and logged in") {
            setToken(res.token);
        }
        if (message === "unrecognised error") alert("Registration unsuccessful, please try again")
    };

    const validPassword = password1.length > 7 && password1 === password2;
    const passwordsMatch = password1 === password2;

    if (token !== "") return <Navigate replace to="/Feed" />;

    return (
        <div>
            <NavBar />
            <PageFrame>
                <RegFrame>
                    <LogoImage src={logo} />
                    <Title>Create an account</Title>
                    <div style={{ textAlign: "center" }}>

                        <div style = {{ margin: "20px 0", textAlign: "left"}}>
                        <Select
                            value = {selectedTopics.map(t => { return {value: t, label: t} })}
                            options = {availableTopics.map(t => { return {value: t, label: t} })}
                            isClearable=  {true}
                            isSearchable = {true}
                            isMulti = {true}
                            onChange = {handleChange}
                            placeholder={<PlaceholderText>Select some topics for your feed</PlaceholderText>}
                            styles={{
                                control: (baseStyles, state) => ({
                                  ...baseStyles,
                                  borderColor: state.isFocused ? 'black' : 'black',
                                }),
                            
                            }}
                            theme={(theme) => ({
                                ...theme,
                                borderRadius: 0,
                                colors: {
                                  ...theme.colors,
                                  primary25: 'var(--colour-background-grey)',
                                  primary: 'none',
                                },
                            })}
                            />
                        </div>
                        <Division data-content="AND"/>
                        <RegForm>
                            <FormInput
                                type="email"
                                name="email"
                                placeholder="Enter Username"
                                onChange={handleEmailChange}
                            />
                            {userAlreadyExists
                                ? username.length > 0 && <MessageText>That username is already in use, please try a different username</MessageText>
                                : <p style={{margin: "0", padding: "0"}}></p>}
                            <FormInput
                                type="password"
                                name="password"
                                placeholder="Enter Password"
                                onChange={e => handlePasswordChange(e, 0)}
                            />
                            <FormInput
                                type="password"
                                name="confirm password"
                                placeholder="Confirm Password"
                                onChange={e => handlePasswordChange(e, 1)}
                            />
                            {passwordTooShort ? <MessageText>Password must be at least 8 characters</MessageText> : <p style={{margin: "0", padding: "0"}}></p>}
                            {!passwordsMatch ? <MessageText>Passwords do not match</MessageText> : <p style={{margin: "0", padding: "0"}}></p>}
                        </RegForm>

                        


                        <SubmitButton
                            active={validPassword && username.length > 0 && selectedTopics.length > 0}
                            onClick={handleSubmit}>
                            REGISTER
                        </SubmitButton>
                        <MessageText>Already have an account?&nbsp;&nbsp;
                            <Link to="/SignIn" style={{color: "var(--colour-pink-accent"}}>Sign in</Link>
                        </MessageText>
                    </div>
                </RegFrame>
            </PageFrame>
        </div>
    );
};

export default RegisterPage;

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 15px;
    width: 70%;
    margin-top: 25px;
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

const MessageText = styled.p`
    font-size: 13px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
`;

const AlertTitle = styled.div`
text-align: center;
font-size: 20px;
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
    width: 30%;
`;
const RegForm = styled.form`
    background-color: none;
    border-radius: 10px;
`;  

const FormInput = styled.input`
    padding: 12px;
    width: 60%;
    margin: 12px;
    border: 1px solid grey;
    border-radius: 3px;
    outline: none;  
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
`;

const PlaceholderText = styled.div`
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
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
