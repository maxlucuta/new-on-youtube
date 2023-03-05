import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import topics from "../TopicTags/topicTagsMasterList";
import { RootContext } from "../context";
import { tokenToEmail, usePost } from "../functions";
import SelectorPage from "../SearchPage/SelectorPage";

const TopicSelection = () => {
    const { token } = useContext(RootContext);
    const [awaitingUserTopics, updateAwaitingUserTopics] = useState(false);
    const [userTopics, updateUserTopics] = useState([] as string[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[])
    const post = usePost();

    const loadUserTopics = async () => {
        updateAwaitingUserTopics(true);
        const payload = { username: tokenToEmail(token)};
        const response = await post("/get_user_topics", payload) as any;
        if (response.status_code != 200) console.log("Request Error!", response)
        else {
            updateUserTopics(response.results);
        }
        updateAwaitingUserTopics(false);
    }

    const getAvailableTopics = async () => {
        const response = (await post("/unique_topics", {}));
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateAvailableTopics(response.topics);
    }

    useEffect(() => {
        loadUserTopics();
        getAvailableTopics();
    }, []);

    const updateUserTopicsDatabase = async (topics: string[]) => {
        if (topics.length === 0) {
            return alert("Please select at least one topic");
        }
        const payload = { username: tokenToEmail(token), topics };
        updateAwaitingUserTopics(true);
        const response = await post("/update_user_topics", payload) as any;
        if (response.status_code != 200) {
            alert("Failed to update topics, please try again");
        } else loadUserTopics();
        updateAwaitingUserTopics(false);
    }

    return (
    <div>
        <NavBar />
        <div style={{ marginLeft: "10%" }}>
            <Title>Your Selected Topics</Title>
        </div>
        <div style = {{ width: "80%", margin: "auto" }}>
            <SelectorPage 
                selection = { userTopics }
                availableTopics = { availableTopics }
                updateSelection = { updateUserTopicsDatabase }
            />
        </div>
        {/* { awaitingUserTopics && <div>Loading message goes here!</div> } */}
    </div>
    )
};

export default TopicSelection;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
`;

const Description = styled.div`
    text-align: left;
    font-size: 18px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
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
    font-weight: 500;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
    margin-bottom: 20px;
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
    margin: 5px;
    color: ${props => (props.selected ? "white" : "black")};
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    padding: 10px;
    border-style: none;
    background-color: ${props => (props.selected ? "#2d1871" : "#b0b0b0")};
    border-radius: 2px;
    &:hover {
        transform: scale(1.1);
        cursor: pointer;
    }
`;

const SearchButton = styled.div`
    width: 300px;
    margin: 50px auto;
    font-size: 30px;
    text-align: center;
    background-color: black;
    color: white;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    font-size: 20px;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;
