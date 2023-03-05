import { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import topics from "../TopicTags/topicTagsMasterList";
import axios from "axios";
import { RootContext } from "../context";
import Feed from "../Feed/Feed";
import SelectorPage from "./SelectorPage";
import ResultsPage from "./ResultsPage";

const SearchPage = () => {
    const [selection, updateSelection] = useState([] as string[]);
    const [searchResults, updateSearchResults] = useState([] as Summary[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[])
    const [mode, updateMode] = useState("SELECTION" as "SELECTION" | "RESULTS")
    const { SERVER_URL } = useContext(RootContext);

    const handleSubmission = async () => {
        const payload = { topics: selection, amount: 20 };
        const response = (await axios.post(SERVER_URL + "/request", payload)).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateSearchResults(response.results);
        updateMode("RESULTS")
    };

    const getAvailableTopics = async () => {
        const response = (await axios.post(SERVER_URL + "/unique_topics", {})).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateAvailableTopics(response.topics);
    }

    useEffect(() => { getAvailableTopics(); }, [])

    return (
        
        <div>
            <NavBar />
            <Container>
                <Title>Find Videos</Title>
            {
                mode === "SELECTION"
                    ? <>
                        <SelectorPage 
                            availableTopics = { availableTopics }
                            selection = { selection }
                            updateSelection = { updateSelection }
                        />
                        { 
                            selection.length > 0
                                ? <SearchButton
                                    onClick={handleSubmission}>
                                    Search videos
                                </SearchButton>
                                : <NoSearchButton>
                                    Please make selection
                                </NoSearchButton>
                        }
                    </>
                    : <ResultsPage
                        updateMode = { updateMode }
                        updateSelection = { updateSelection }
                        updateSearchResults = { updateSearchResults }
                        handleSubmission = { handleSubmission }
                        searchResults = { searchResults }
                    />
            }
            </Container>
        </div>
    )
};

export default SearchPage;

const Container = styled.div`
    width: 80%;
    padding: 10px;
    margin: 20px auto;
`;

const Title = styled.div`
    padding-bottom: 10px;
    border-bottom: 2px solid black;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
`;

const SearchButton = styled.div`
    width: 50%;
    margin: 50px auto;
    font-size: 20px;
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

const NoSearchButton = styled.div`
    width: 50%;
    margin: 50px auto;
    font-size: 20px;
    text-align: center;
    background-color: grey;
    color: black;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
`;

