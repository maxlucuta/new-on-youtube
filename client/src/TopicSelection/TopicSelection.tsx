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
            <div style={{ backgroundColor: "#FAD000" }}>
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

            <div style={{ width: "60%", margin: "auto" }}>
                {selectedTopics.map(r => (<Description>{r}</Description>))}
            </div>

            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Change Your Topics!</Title>
            </div>
            <TwoPanel>
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
                    <PanelTitle>Selected Topics</PanelTitle>
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
    font-size: 60px;
    font-weight: bold;
    margin: auto;
    padding: 50px 0;
    width: max-content;
`;

const FeedSelector = styled.div<{ selected: boolean }>`
    font-size: 30px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
    text-decoration: ${props => (props.selected ? "underline" : "none")};
    margin: 20px;
    &:hover {
        color: #fad000;
        cursor: pointer;
    }
`;

const Result = styled.a`
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

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 12px 30px;
    width: 40%;
    margin-top: 40px;
    background-color: black;
    opacity: ${props => (props.active ? "1" : "0.2")};
    color: white;
    font-weight: bold;
    border: none;
    outline: none;
    border-radius: 20px;
    &:hover {
        cursor: ${props => (props.active ? "pointer" : "not-allowed")};
        background-color: ${props => (props.active ? "#750000" : "black")};
    }
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
