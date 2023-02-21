import { useContext, useState } from "react";
import { useNavigate, Navigate } from "react-router";
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
                    {userAlreadyExists
                        ? username.length > 0 && <div>That username is already in use, please try a different username</div>
                        : <div></div>}
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
                    </div>
                </div>
            <div>


            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Select Your Topics!</Title>
            </div>
            <TwoPanel>
                <LeftPanel>
                    <PanelTitle>Available Topics</PanelTitle>
                    <SearchBar
                        placeholder="Search"
                        onChange={handleSearchBar}
                    />
                    <CategoryContainer>
                        {searchBarValue.length !== 0 && (
                            <Category
                                selected={selectedTopics.includes(searchBarValue)}
                                onClick={() => handleSelectedTopics(searchBarValue)}>
                                Add Custom Topic: {searchBarValue}
                            </Category>
                        )}
                        {filteredTopicSelection.map(c => (
                            <Category
                                selected={selectedTopics.includes(c)}
                                onClick={() => handleSelectedTopics(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </LeftPanel>
                <RightPanel>
                    <PanelTitle>Selected Topics</PanelTitle>
                    <CategoryContainer>
                        {selectedTopics.map(c => (
                            <Category selected={true} onClick={() => handleSelectedTopics(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
        </div>

        <SubmitButton
            active={validPassword && username.length > 0 && selectedTopics.length > 0}
            onClick={handleSubmit}>
            REGISTER
        </SubmitButton>

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

const Title = styled.div`
    font-size: 40px;
    font-weight: bold;
    margin: auto;
    padding: 35px 0;
    width: max-content;
`;

const TwoPanel = styled.div`
    display: flex;
    justify-content: center;
    width: 80%;
    max-height: 50vh;
    margin: 50px auto 0 auto;
`;

const LeftPanel = styled.div`
    text-align: center;
    width: 50%;
    border-right: 2px solid black;
`;

const RightPanel = styled.div`
    text-align: center;
    width: 50%;
    border-left: 2px solid black;
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
    font-weight: bold;
`;

const CategoryContainer = styled.div`
    display: flex;
    width: 100%;
    flex-wrap: wrap;
    justify-content: center;
    overflow: scroll;
    max-height: 80%;
`;

const Category = styled.button<{ selected: boolean }>`
    margin: 10px;
    font-size: 30px;
    padding: 10px;
    border-style: none;
    background-color: ${props => (props.selected ? "orange" : "#fad000")};
    border-radius: 5px;
    &:hover {
        transform: scale(1.1);
        cursor: pointer;
    }
`;
