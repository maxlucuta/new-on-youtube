import { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import axios from "axios";
import { RootContext } from "../context";
import ResultsPage from "./ResultsPage";
import { ActionMeta, MultiValue } from 'react-select'
import Creatable from 'react-select/creatable'
import { MAX_TOPICS, delay } from "../functions";
import Spinner from "../spinner";
import refresh from "../assets/refreshSlim.png";

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
        let response = (await axios.post(SERVER_URL + "/request", payload)).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        else {
            updateMode("RESULTS")
            while (response.results.length < 3) {
                await delay(5000);
                response = (await axios.post(SERVER_URL + "/request", payload)).data;
                console.log("Resent request")
            }
            updateSearchResults(response.results);
        }
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
            <div style={{ display: "flex", borderBottom: mode === "SELECTION" ? "none" : "2px solid black"}}>
                <Title>Find Videos</Title>
                {
                    mode === "SELECTION" 
                        ? <div></div> 
                    
                        : <div style={{ display: "flex"}}>
                        <NewSearchButton
                            onClick={() => {
                                updateMode("SELECTION")
                                updateSelection([]);
                                updateSearchResults([]);
                            }}>
                            <span className="button-text">New Search</span>
                        </NewSearchButton>
                        <RefreshButton onClick={handleSubmission}>
                            <RefreshIcon src={refresh} />
                        </RefreshButton>
                        </div>
                }
                
            </div>
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
                                placeholder={<PlaceholderText>Select topics, or search and create your own</PlaceholderText>}
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

                        {
                            selection.length > 0
                                ?   <div style={{padding: "20px"}}>
                                    <SearchButton
                                        onClick={handleSubmission}>
                                        Search videos
                                    </SearchButton>
                                    </div>
                                : <div></div>
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
            {noResults && mode === "RESULTS" && <Loading style={{ textAlign: "center", color: "grey" }}>Generating videos, please wait a few minutes</Loading>}
            {noResults && mode === "RESULTS" && <div><Spinner/></div>}
            </Container>
        </div>
    )
};

export default SearchPage;

const Container = styled.div`
    width: 70%;
    padding: 10px;
    margin: 20px auto;
`;

const Loading = styled.div`
    padding-bottom: 15px;
`;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
`;

const SearchButton = styled.div`
    width: 20%;
    margin: 50px auto;
    font-size: 20px;
    text-align: center;
    background-color: var(--colour-pink-accent);
    color: white;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const PlaceholderText = styled.div`
    font-size: 15px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
`;

const NewSearchButton = styled.button`
    font-size: 20px;
    text-align: center;
    width: max-content;
    padding: 10px;
    margin: 60px 20px 20px 30px;
    background-color: var(--colour-background-grey);
    color: black;
    border-style: none;
    border-radius: 5px;
    font-size: 17px;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const RefreshButton = styled.div`
    margin: 60px 20px 20px 10px;
    font-size: 20px;
    background-color: var(--colour-background-grey) ;
    align-items: center;
    vertical-align: middle;

    color: black;
    border-style: none;
    border-radius: 5px;
    padding: 10px 10px 5px 10px;
    font-size: 20px;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const RefreshIcon = styled.img`
    width:35px;
`;


