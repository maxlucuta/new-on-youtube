import { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import axios from "axios";
import { RootContext } from "../context";
import ResultsPage from "./ResultsPage";
import { MAX_TOPICS, delay } from "../functions";
import Spinner from "../spinner";
import refresh from "../assets/shuffleWhite.png";
import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'
import SearchPageBar from "./SearchPageBar";
import DefaultSearchPageBar from "./DefaultSearchPageBar";


const SearchPage = () => {
    const [selection, updateSelection] = useState([] as string[]);
    const [searchResults, updateSearchResults] = useState([] as Summary[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[]);
    const [mode, updateMode] = useState("SELECTION" as "SELECTION" | "RESULTS")
    const { SERVER_URL, token } = useContext(RootContext);
    const CustomAlert = withReactContent(Swal)

    const noResults = searchResults.length === 0;

    const handleSubmission = async () => {
        const payload = { topics: selection, amount: 20 };
        const selectedTopics = selection;
        let response = (await axios.post(SERVER_URL + "/request", payload)).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        if (response.results.length === 0) {
            CustomAlert.fire({
                icon: "success",
                title: <AlertMessage>
                            Generating videos for <b>{selectedTopics.join(', ')}</b>. We will let you know when they're ready with another popup.
                            <br></br><br></br>Carry on browsing and once the videos are ready you will be able to search for them here.
                        </AlertMessage>,
                timer: 10000
                });
            updateSelection([]);
            while (response.results.length === 0) {
                await delay(5000);
                response = (await axios.post(SERVER_URL + "/request", payload)).data;
                console.log("Resent request")
            }
            getAvailableTopics();
            CustomAlert.fire({
                icon: "info",
                title: <AlertMessage>
                            Videos for <b>{selectedTopics.join(', ')}</b> are ready.<br></br><br></br>
                            You can now enter this topic on the <b>Search Page</b> or when selecting topics for your <b>User Feed</b>. 
                        </AlertMessage>,
                });
        } else {
            updateMode("RESULTS")
            updateSearchResults(response.results);
        }
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
            <div style={{ display: "flex", marginTop: "50px", borderBottom: mode === "SELECTION" ? "none" : "2px solid black"}}>
                <Title>Find Videos</Title>
                {
                    mode === "SELECTION"
                        ? <div></div>

                        : <div style={{ display: "flex", flexDirection: "row-reverse", marginLeft: "auto", alignItems: "center"}}>    
                        <NewSearchButton
                            onClick={() => {
                                updateMode("SELECTION")
                                updateSelection([]);
                                updateSearchResults([]);
                            }}>
                            <span>New Search</span>
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
                            {
                                token
                                    ? <SearchPageBar
                                        selection={selection} 
                                        updateSelection={updateSelection} 
                                        availableTopics={availableTopics}
                                    />
                                    : <DefaultSearchPageBar 
                                        selection={selection} 
                                        updateSelection={updateSelection} 
                                        availableTopics={availableTopics}
                                    />
                            }
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
            { selection.length == 0 ?
            token ?
                <div style={{
                    marginTop: "30px",
                    color: "grey",
                    fontWeight: "300",
                    textAlign: "center"}}
                    >Use the menu above to select or search for topics. You can search for multiple topics at once - up to {MAX_TOPICS} at a time.<br></br><br></br>
                    If your topic isn't in our database yet, you can click <em>Create "Your Topic"</em>.<br></br>
                    For new topics we need to search YouTube, extract the transcript, and summarise it with GPT-3. So there will be a short delay.<br></br>
                    <br></br>A notification will let you know when your topic has been sent for processing, and another will let you know once the videos are ready!
                </div>
                :
                <div style={{
                    marginTop: "30px",
                    color: "grey",
                    fontWeight: "300",
                    textAlign: "center"}}
                    >Use the menu above to select or search for topics. You can search for multiple topics at once - up to {MAX_TOPICS} at a time.
                </div>

            : <div></div>
            }

            <div style={{marginTop: "50px"}}>
            {noResults && mode === "RESULTS" &&
                <Loading>
                    Searching Youtube for relevant videos. Extracting transcripts and summarising with GPT-3. <br></br>
                    We will let you know when your videos are ready!
                </Loading>}
            {noResults && mode === "RESULTS" && <div><Spinner/></div>}
            </div>
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

const Loading = styled.div`
    padding-bottom: 15px;
    text-align: center;
    color: black;
    font-weight: 300;
`;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
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
    font-size: 16px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif
`;

const NewSearchButton = styled.button`
    font-size: 20px;
    padding: 10px;
    text-align: center;
    width: max-content;
    background-color: var(--colour-pink-accent);
    color: white;
    border-style: none;
    border-radius: 5px;
    font-size: 17px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const RefreshButton = styled.button`
    font-size: 20px;
    background-color: var(--colour-pink-accent);
    padding-top: 5px;
    margin-right: 10px;
    color: black;
    border-style: none;
    border-radius: 5px;
    font-size: 20px;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const RefreshIcon = styled.img`
    width:30px;
`;

const AlertMessage = styled.div`
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif
`;

