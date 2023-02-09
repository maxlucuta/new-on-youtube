import { useContext, useEffect, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import testCategories from "../test/test_categories.json";
import { Summary } from "../types";
import topics from "./tags";
import Result from "../Result";
import axios from "axios";
import { RootContext } from "../context";

const SearchPage = () => {
    const [searchValue, updateSearchValue] = useState("");
    const [selection, updateSelection] = useState([] as string[]);
    const [available, updateAvailable] = useState(testCategories as string[]);
    const [displaySelector, updateDisplaySelector] = useState(true);
    const [searchResults, updateSearchResults] = useState([] as Summary[]);
    const { SERVER_URL } = useContext(RootContext);

    const searchCompleted = searchResults.length > 0;

    const handleSearchChange = (e: any) => {
        updateSearchValue(e.target.value);
    };

    const handleSelection = (c: string, type: "select" | "unselect") => {
        if (type === "select") {
            updateAvailable(a => a.filter(cat => cat !== c));
            updateSelection(selection.concat([c]));
        } else {
            updateAvailable(available.concat([c]));
            updateSelection(s => s.filter(cat => cat !== c));
        }
    };

    const handleSubmission = async () => {
        const payload = { topics: selection, amount: 10 };
        const results = await (await axios.post(SERVER_URL + "/request", payload)).data;
        updateSearchResults(results);
    };

    const getPopularTopics = async () => {
        updateAvailable(topics);
    };

    useEffect(() => {
        getPopularTopics();
    }, []);

    return (
        <div>
            <NavBar />
            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Select Your Categories!</Title>
            </div>
            <SelectorToggle onClick={() => updateDisplaySelector(!displaySelector)}>
                {displaySelector ? "hide" : "show"} topic selection
            </SelectorToggle>
            <TwoPanel style={{ display: displaySelector ? "flex" : "none" }}>
                <LeftPanel>
                    <PanelTitle>Available Topics</PanelTitle>
                    <SearchBar placeholder="Search" onChange={handleSearchChange} />
                    <CategoryContainer>
                        {available.map(c => (
                            <Category onClick={() => handleSelection(c, "select")}>{c}</Category>
                        ))}
                    </CategoryContainer>
                </LeftPanel>
                <RightPanel>
                    <PanelTitle>Selected Topics</PanelTitle>
                    <CategoryContainer>
                        {selection.map(c => (
                            <Category onClick={() => handleSelection(c, "unselect")}>{c}</Category>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
            <SearchButton
                style={{ display: displaySelector ? "block" : "none" }}
                onClick={handleSubmission}>
                Search!
            </SearchButton>
            <SearchResults>
                {searchCompleted ? (
                    searchResults.map(r => <Result summary={r} />)
                ) : (
                    <Container>
                        <Description>Select topics and click search!</Description>
                    </Container>
                )}
            </SearchResults>
        </div>
    );
};

export default SearchPage;

const Title = styled.div`
    font-size: 60px;
    font-weight: bold;
    margin: auto;
    padding: 50px 0;
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

const Category = styled.button`
    margin: 10px;
    font-size: 30px;
    padding: 10px;
    border-style: none;
    background-color: #fad000;
    border-radius: 5px;
    &:hover {
        transform: scale(1.1);
        cursor: pointer;
    }
`;

const SelectorToggle = styled.div`
    color: grey;
    margin: 20px auto;
    width: max-content;

    &:hover {
        cursor: pointer;
    }
`;

const SearchButton = styled.div`
    width: 300px;
    margin: 50px auto;
    font-size: 40px;
    text-align: center;
    background-color: black;
    color: white;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    &:hover {
        color: #fad000;
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const SearchResults = styled.div`
    width: 60%;
    border-top: 5px solid black;
    margin: auto;
`;

const Container = styled.a`
    display: flex;
    text-decoration: none;
    color: black;
    align-items: center;
    padding: 10px;
    background-color: #e1e1e1;
    border-radius: 10px;
    margin: 20px 0;
    &:hover {
        cursor: pointer;
        background-color: #fff1ac;
    }
`;

const Img = styled.img`
    border-radius: 10px;
    width: 15%;
`;

const Description = styled.div`
    text-align: center;
    width: 85%;
    font-size: 25px;
`;
