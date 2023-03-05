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
                    ? <SelectorPage 
                        availableTopics = { availableTopics }
                        selection = { selection }
                        updateSelection = { updateSelection }
                        updateSearchResults = { updateSearchResults }
                        updateMode = { updateMode }
                        handleSubmission = { handleSubmission }
                    />
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

