import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import topics from "../TopicTags/topicTagsMasterList";
import { RootContext } from "../context";
import { tokenToEmail, usePost } from "../functions";

const TopicSelection = () => {
    const { token } = useContext(RootContext);
    const [selectedTopics, updateSelectedTopics] = useState([]);
    const [searchValue, updateSearchValue] = useState("");
    const [newTopicSelection, updateNewTopicSelection] = useState([] as string[]);
    const [filtered, updateFiltered] = useState(topics as string[]);
    const post = usePost();

    const handleLoadSelectedTopics = async () => {
        const payload = { username: tokenToEmail(token)};
        const response = await post("/get_user_topics", payload) as any;
        if (response.status_code != 200) console.log("Request Error!", response)
        else {
            updateSelectedTopics(response.results);
            updateNewTopicSelection(response.results);
        }
    }

    useEffect(() => {
        handleLoadSelectedTopics();
    }, []);

    const handleSearchChange = (e: any) => {
        updateSearchValue(e.target.value);
        if (e.target.value.length !== 0) {
            updateFiltered(topics.filter(c => c.startsWith(e.target.value)));
        } else {
            updateFiltered(topics);
        }
    };

    const handleSelection = (c: string) => {
        if (!newTopicSelection.includes(c)) {
            updateNewTopicSelection(newTopicSelection.concat([c]));
        } else {
            updateNewTopicSelection(s => s.filter(cat => cat !== c));
        }
    };

    const handleNewEntryEnter = (e: any) => {
        if (e.key != "Enter") return;
        if (filtered.length !== 0) return;
        if (true) {
            updateNewTopicSelection(newTopicSelection.concat([searchValue]));
            e.target.value = "";
            updateSearchValue("");
            updateFiltered(topics);
        }
    };

    const handleUpdatedTopics = async () => {
        if (newTopicSelection.length === 0) {
            alert("Please select at least one topic");
            return;
        }
        console.log(newTopicSelection)
        const payload = { username: tokenToEmail(token), topics: newTopicSelection };
        const response = await post("/update_user_topics", payload) as any;
        if (response.status_code != 200) {
            console.log("Request Error!", response)
            alert("Failed to update topics, please try again");
        } else handleLoadSelectedTopics();
    };

    return (
        <div>
            <NavBar />
            <div style={{ marginLeft: "20%" }}>
                <Title>Your Selected Topics</Title>
            </div>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: "max-content",
                    margin: "auto",
                }}>
            </div>

            <div style={{ display: "flex", width: "60%", margin: "auto", justifyContent: "left" }}>
                <Description style={{marginRight: "10px", fontWeight: "500"}}>Topics in your feed:</Description>
                {selectedTopics.map((r, i) => (
                    <>
                    {i !== 0 ? <div style={{fontSize: "20px", margin: "0 10px 0 10px"}}>|</div>: <></>}
                    <Description>{r}</Description>
                    </>
                ))}
            </div>
            <TwoPanel>
                <LeftPanel>
                    <PanelTitle>Available</PanelTitle>
                    <SearchBar
                        placeholder="Search"
                        onChange={handleSearchChange}
                        onKeyDown={handleNewEntryEnter}
                    />
                    <CategoryContainer>
                        {searchValue.length !== 0 && (
                            <Category
                                selected={newTopicSelection.includes(searchValue)}
                                onClick={() => handleSelection(searchValue)}>
                                Add Custom Topic: {searchValue}
                            </Category>
                        )}
                        {filtered.map(c => (
                            <Category
                                selected={newTopicSelection.includes(c)}
                                onClick={() => handleSelection(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </LeftPanel>
                <RightPanel>
                    <PanelTitle>Selected</PanelTitle>
                    <CategoryContainer>
                        {newTopicSelection.map(c => (
                            <Category selected={true} onClick={() => handleSelection(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
            <SearchButton
                onClick={handleUpdatedTopics}>
                Update Topics
            </SearchButton>

        </div>
    );
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
