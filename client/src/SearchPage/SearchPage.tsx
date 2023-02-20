import { useContext, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import topics from "./tags";
import axios from "axios";
import { RootContext } from "../context";
import Feed from "../Feed/Feed";

const SearchPage = () => {
    const [searchValue, updateSearchValue] = useState("");
    const [selection, updateSelection] = useState([] as string[]);
    const [filtered, updateFiltered] = useState(topics as string[]);
    const [displaySelector, updateDisplaySelector] = useState(true);
    const [searchResults, updateSearchResults] = useState([] as Summary[]);
    const { SERVER_URL } = useContext(RootContext);

    const searchCompleted = searchResults.length > 0;

    const handleSearchChange = (e: any) => {
        updateSearchValue(e.target.value);
        if (e.target.value.length !== 0) {
            updateFiltered(topics.filter(c => c.startsWith(e.target.value)));
        } else {
            updateFiltered(topics);
        }
    };

    const handleSelection = (c: string) => {
        if (!selection.includes(c)) {
            updateSelection(selection.concat([c]));
        } else {
            updateSelection(s => s.filter(cat => cat !== c));
        }
    };

    const handleSubmission = async () => {
        const payload = { topics: selection, amount: 10 };
        const response = (await axios.post(SERVER_URL + "/request", payload)).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateSearchResults(response.results);
    };

    const handleNewEntryEnter = (e: any) => {
        if (e.key != "Enter") return;
        if (filtered.length !== 0) return;
        if (true) {
            updateSelection(selection.concat([searchValue]));
            e.target.value = "";
            updateSearchValue("");
            updateFiltered(topics);
        }
    };

    return (
        <div>
            <NavBar />
            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Select Your Topics!</Title>
            </div>
            <SelectorToggle onClick={() => updateDisplaySelector(!displaySelector)}>
                {displaySelector ? "hide" : "show"} topic selection
            </SelectorToggle>
            <TwoPanel style={{ display: displaySelector ? "flex" : "none" }}>
                <LeftPanel>
                    <PanelTitle>Available Topics</PanelTitle>
                    <SearchBar
                        placeholder="Search"
                        onChange={handleSearchChange}
                        onKeyDown={handleNewEntryEnter}
                    />
                    <CategoryContainer>
                        {searchValue.length !== 0 && (
                            <Category
                                selected={selection.includes(searchValue)}
                                onClick={() => handleSelection(searchValue)}>
                                Add Custom Topic: {searchValue}
                            </Category>
                        )}
                        {filtered.map(c => (
                            <Category
                                selected={selection.includes(c)}
                                onClick={() => handleSelection(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </LeftPanel>
                <RightPanel>
                    <PanelTitle>Selected Topics</PanelTitle>
                    <CategoryContainer>
                        {selection.map(c => (
                            <Category selected={true} onClick={() => handleSelection(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
            <SearchButton
                style={{ display: displaySelector ? "block" : "none" }}
                onClick={handleSubmission}>
                Search!
            </SearchButton>
            {searchCompleted ? (
                <Feed results={searchResults} />
            ) : (
                <Container>
                    <Description>Select topics and click search!</Description>
                </Container>
            )}
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

const Container = styled.a`
    display: flex;
    text-decoration: none;
    color: black;
    align-items: center;
    padding: 10px;
    margin: 20px 0;
`;

const Description = styled.div`
    text-align: center;
    width: 85%;
    font-size: 25px;
    margin: auto;
`;
