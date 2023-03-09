import { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import axios from "axios";
import { RootContext } from "../context";
import ResultsPage from "./ResultsPage";
import { ActionMeta, MultiValue } from 'react-select'
import Creatable from 'react-select/creatable'
import { MAX_TOPICS } from "../functions";

type SelectOption = {
    label: string;
    value: string;
}

const SearchPage = () => {
    const [selection, updateSelection] = useState([] as string[]);
    const [searchResults, updateSearchResults] = useState([] as Summary[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[])
    const [mode, updateMode] = useState("SELECTION" as "SELECTION" | "RESULTS")
    const { SERVER_URL } = useContext(RootContext);

    const noResults = searchResults.length === 0;

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

    const handleChange = (newValue: MultiValue<SelectOption>, actionMeta: ActionMeta<SelectOption>) => {
        if (selection.length > MAX_TOPICS) alert("Maximum of 20 topics allowed.");
        else updateSelection(newValue.map(nv => nv.value));
    }

    const handleNewOption = (newOption: string) => {
        if (selection.length > MAX_TOPICS - 1) alert("Maximum of 20 topics allowed.");
        else updateSelection(s => s.concat([newOption]));
    }

    return (

        <div>
            <NavBar />
            <Container>
                <Title>Find Videos</Title>
            {
                mode === "SELECTION"
                    ? <>
                        <div style = {{ marginTop: "20px" }}>
                            <Creatable
                                value = {selection.map(t => { return {value: t, label: t} })}
                                options = {availableTopics.map(t => { return {value: t, label: t} })}
                                isClearable=  {true}
                                isSearchable = {true}
                                isMulti = {true}
                                onChange = {handleChange}
                                onCreateOption = {handleNewOption}
                            />
                        </div>

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
            {noResults && mode === "RESULTS" && <div style={{ textAlign: "center", color: "grey" }}>Generating videos, please wait a few minutes</div>}
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
    background-color: #f0f0f1;
    color: black;
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

