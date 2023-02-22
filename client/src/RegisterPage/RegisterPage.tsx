import { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router";
import { Form } from "react-router-dom";
import styled from "styled-components";
import { RootContext } from "../context";
import { usePost } from "../functions";
import NavBar from "../NavBar/Navbar";
import topics from "../TopicTags/topicTagsMasterList";
import "./register.css";

const RegisterPage = () => {
    const [username, updateUsername] = useState("");
    const [password1, updatePassword1] = useState("");
    const [password2, updatePassword2] = useState("");
    const [userAlreadyExists, updateUserAlreadyExists] = useState(false);
    const [searchBarValue, updateSearchBarValue] = useState("");
    const [filteredTopicSelection, updateFilteredTopicSelection] = useState(topics as string[]);
    const [selectedTopics, updateSelectedTopics] = useState([] as string[]);
    const { token, setToken } = useContext(RootContext);
    const navigate = useNavigate();
    const post = usePost();

    const handleEmailChange = (e: any) => {
        updateUsername(e.target.value);
    };

    const handlePasswordChange = (e: any, idx: number) => {
        idx === 0 ? updatePassword1(e.target.value) : updatePassword2(e.target.value);
    };

    const handleSearchBar = (e: any) => {
        updateSearchBarValue(e.target.value);
        if (e.target.value.length !== 0) {
            updateFilteredTopicSelection(topics.filter(c => c.startsWith(e.target.value)));
        } else {
            updateFilteredTopicSelection(topics);
        }
    };

    const handleSelectedTopics = (c: string) => {
        if (!selectedTopics.includes(c)) {
            updateSelectedTopics(selectedTopics.concat([c]));
        } else {
            updateSelectedTopics(s => s.filter(cat => cat !== c));
        }
        console.log(selectedTopics)
    };

    const handleSubmit = async () => {
        const payload = { username: username, password: password1, confirmation: password2, topics: selectedTopics};
        const res = await post("/register", payload) as any;
        const message = res.message;
        console.log(message)
        if (message === "invalid fields") alert("Please enter a username, password, and matching password confirmation");
        if (message === "username already in use") updateUserAlreadyExists(true);
        if (message === "no topics selected") alert("Please select at least one topic");
        if (message === "successfully added and logged in") {
            setToken(res.token);
            navigate("/");
        }
        if (message === "unrecognised error") alert("Registration unsuccessful, please try again")
    };

    const validPassword = password1.length !== 0 && password1 === password2;

    if (token !== "") return <Navigate replace to = "/" />

    return (
        <div>
            <div style={{backgroundColor: "#f0f0f1", height: "100vh"}}>
                <NavBar />
                <PageFrame>
                    <LeftFrame>
                        <RegFrame>
                        <div style={{textAlign: "center"}}>
                        <Title>Create an account</Title>
                        <RegForm>
                            <FormInput
                                type="email"
                                name="email"
                                placeholder="Enter Email"
                                onChange={handleEmailChange}
                            />
                            {userAlreadyExists
                                ? username.length > 0 && <div>That username is already in use, please try a different username</div>
                                : <div></div>}
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
                            {!validPassword
                                ? password2.length > 0 && <div>Passwords do not match</div>
                                : password2.length > 0 && <div>Valid password!</div>}
                        </RegForm>
                        
                      
                        <SubmitButton
                            active={validPassword && username.length > 0 && selectedTopics.length > 0}
                            onClick={handleSubmit}>
                            REGISTER
                        </SubmitButton>
                        </div>
                        </RegFrame>

                        <PanelTitle>Selected Topics</PanelTitle>
                        <SelectedContainer>
                            {selectedTopics.map(c => (
                                <SelectedCategory selected={true} onClick={() => handleSelectedTopics(c)}>
                                    {c}
                                </SelectedCategory>
                            ))}
                        </SelectedContainer>
                        
                    </LeftFrame>
                    <RightFrame>
                        <VerticalFrame>
                            <PanelTitle>Select Topics</PanelTitle>
                            <SearchBar
                                placeholder="Search"
                                onChange={handleSearchBar}
                            />
                            <SelectionContainer>
                                {searchBarValue.length !== 0 && (
                                    <SelectionCategory
                                        selected={selectedTopics.includes(searchBarValue)}
                                        onClick={() => handleSelectedTopics(searchBarValue)}>
                                        Add Custom Topic: {searchBarValue}
                                    </SelectionCategory>
                                )}
                                {filteredTopicSelection.map(c => (
                                    <SelectionCategory
                                        selected={selectedTopics.includes(c)}
                                        onClick={() => handleSelectedTopics(c)}>
                                        {c}
                                    </SelectionCategory>
                                ))}
                            </SelectionContainer>
                        </VerticalFrame>
                        <VerticalFrame>
                            
                        </VerticalFrame>
                    </RightFrame> 
                </PageFrame>
            </div>
        </div>

    );
};

export default RegisterPage;

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

const LeftFrame = styled.div`
    display: flex;
    flex-direction: column;
    text-align: left;
    width: 45%;
    height: 100vh;
`;

const RightFrame = styled.div`
    display: flex;
    flex-direction: column;
    text-align: left;
    width: 55%;
    height: 100vh;
`;


const VerticalFrame = styled.div`
    text-align: left;
    width: 100%;
`;

const RegFrame = styled.div`
    display: flex;
    flex-direction: column; 
    background-color: #f0f0f1;    
    width: 75%;
    border-radius: 3px;
    margin-bottom: 40px;
    filter: drop-shadow(0 0.3rem 0.25rem grey);
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
const SearchBar = styled.input`
    margin: 10px;
    width: 250px;
    font-size: 20px;
    border-style: none;
    border-bottom: 2px solid grey;
    &:focus {
        outline: none;
    }
`;

const PanelTitle = styled.div`
    font-size: 30px;
    font-weight: 500;
    font-family: 'Rubik', sans-serif;
`;

const SelectionContainer = styled.div`
    display: flex;
    width: 100%;
    flex-wrap: wrap;
    justify-content: left;
    overflow: scroll;
    max-height: 70vh;
`;

const SelectedContainer = styled.div`
    display: flex;
    width: 75%;
    flex-wrap: wrap;
    justify-content: left;
    overflow: scroll;
    max-height: 30vh;
`;


const SelectionCategory = styled.button<{ selected: boolean }>`
    margin: 5px;
    color: ${props => (props.selected ? "white" : "black")};
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    padding: 10px;
    border-style: none;
    background-color: ${props => (props.selected ? "#2d1871" : "#B0B0B0")};
    border-radius: 2px;
    &:hover {
        transform: scale(1.1);c
        cursor: pointer;
    }
`;

const SelectedCategory = styled.button<{ selected: boolean }>`
    margin: 5px;
    color: "black"  ;
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    padding: 10px;
    border-style: none;
    background-color: none;
    border-radius: 2px;
    &:hover {
        cursor: pointer;
    }
`;
