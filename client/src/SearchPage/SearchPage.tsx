import { useContext, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import topics from "../TopicTags/topicTagsMasterList";
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
            updateFiltered(topics.filter(c => c.toLowerCase().includes(e.target.value.toLowerCase())));
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
        if (filtered.length != 0) return;
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
            <div style={{
                display: "flex",
                alignItems: "center",
                width: "max-content",
                marginLeft: "20%"
            }}>
                <Title>Find Videos</Title>
                <NewSearchButton 
                    style={{display: displaySelector ? "none" : "block"}}
                    onClick={() => {
                        updateDisplaySelector(!displaySelector);
                        updateSelection([]);
                        updateSearchResults([]);
                    }}>
                    New Search
                </NewSearchButton>
            </div>
            
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    width: "max-content",
                    marginLeft: "20%",
                }}>
                <LeftPanel style={{border: "none"}}>
                </LeftPanel>
                <RightPanel style={{border: "none"}}>

                </RightPanel>

            </div>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    marginLeft: "20%",
                    marginRight: "25%"
                }}>

                {/* -- DROPDOWN SELECT - NEEDS MORE WORK --
                <select >
                    {topics.map(e => (
                        <DropdownSelect 
                            key={e} 
                            value={e}
                            onClick={() => handleSelection(e)}>
                                {e}
                        </DropdownSelect>
                    ))}
                </select>
                */}
            </div>
            <TwoPanel style={{ display: displaySelector ? "flex" : "none" , marginBottom: "20px"}}>
                <LeftPanel>
                    <div style={{display: "flex", flexDirection: "column", maxHeight: "50vh"}}>
                        <CategoryContainer style={{justifyContent: "right", paddingRight: "30px", borderRight: "0.5px solid black"}}>
                            <SearchBar
                                placeholder="Filter and select topics"
                                onChange={handleSearchChange}
                                onKeyDown={handleNewEntryEnter}
                            />
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
                        <div style={{display: "flex", width: "100%", justifyContent: "center"}}>
                        <SearchButton
                            onClick={() => {
                                handleSubmission();
                                updateDisplaySelector(!displaySelector);
                            }}>
                            Search videos
                        </SearchButton>
                        </div>
                    </div>
                </LeftPanel>
                <RightPanel>
                    <CategoryContainer style={{justifyContent: "center"}}>
                        {selection.map(c => (
                            <SelectedCategory selected={true} onClick={() => handleSelection(c)}>
                                {c}
                            </SelectedCategory>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
            {searchCompleted ? (
                <Feed results={searchResults} />) : (<Container></Container>
            )}
        </div>
    );
};

export default SearchPage;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
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
`;

const RightPanel = styled.div`
    text-align: center;
    width: 50%;
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
const SelectorToggle = styled.div`
    color: grey;
    margin: 20px auto;
    width: max-content;

    &:hover {
        cursor: pointer;
    }
`;

const SearchButton = styled.div`
    width: 50%;
    margin-top: 40px;
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

const NewSearchButton = styled.div`
    width: 200px;
    margin: 40px 0 0 40px;
    font-size: 20px;
    text-align: center;
    background-color: #f0f0f1;
    color: black;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    &:hover {
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
