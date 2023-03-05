import { Dispatch, SetStateAction, useContext, useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { Summary } from "../types";
import topics from "../TopicTags/topicTagsMasterList";

type SelectorPageProps = {
    availableTopics: string[]
    selection: string[];
    updateSelection: (v: string[]) => void;
}

const SelectorPage = (props: SelectorPageProps) => {
    const [searchValue, updateSearchValue] = useState("");
    const [filtered, updateFiltered] = useState([] as string[]);

    const handleSearchChange = (e: any) => {
        updateSearchValue(e.target.value);
        if (e.target.value.length !== 0) {
            updateFiltered(props.availableTopics.filter(c => c.toLowerCase().startsWith(e.target.value.toLowerCase())));
        } else {
            updateFiltered(props.availableTopics); 
        }
    };

    const handleSelection = (c: string) => {
        if (!props.selection.includes(c)) {
            props.updateSelection(props.selection.concat([c]));
        } else {
            props.updateSelection(props.selection.filter(cat => cat !== c));
        }
    };

    const handleNewEntryEnter = (e: any) => {
        if (e.key != "Enter") return;
        if (filtered.length != 0) return;
        if (true) {
            props.updateSelection(props.selection.concat([searchValue]));
            e.target.value = "";
            updateSearchValue("");
            updateFiltered(topics);
        }
    };

    return (
        <>
            <div style = {{ display: "flex", justifyContent: "space-around", marginTop: "50px" }}>
                <div>Search for topics</div>
                <div>Your selection</div>
            </div>

            <TwoPanel>
                <LeftPanel>
                    <CategoryContainer>
                        <div>
                            <SearchBar
                                placeholder="Search for something..."
                                onChange={handleSearchChange}
                                onKeyDown={handleNewEntryEnter}
                            />
                        </div>
                        {filtered.length === 0 && searchValue && (
                            <Category
                                selected={props.selection.includes(searchValue)}
                                onClick={() => handleSelection(searchValue)}>
                                Add New Topic: {searchValue}
                            </Category>
                        )}
                        {searchValue && filtered.map(c => (
                            <Category
                                selected={props.selection.includes(c)}
                                onClick={() => handleSelection(c)}>
                                {c}
                            </Category>
                        ))}
                    </CategoryContainer>
                </LeftPanel>
                <RightPanel>
                    <CategoryContainer>
                        {props.selection.map(c => (
                            <SelectedCategory selected={true} onClick={() => handleSelection(c)}>
                                {c}
                            </SelectedCategory>
                        ))}
                    </CategoryContainer>
                </RightPanel>
            </TwoPanel>
        </>
    );
};

export default SelectorPage;


const Title = styled.div`
    padding-bottom: 10px;
    border-bottom: 2px solid black;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
`;

const TwoPanel = styled.div`
    display: flex;
    justify-content: space-between;
    max-height: 50vh;
    min-height: 20vh;
    margin: 20px auto 20px auto;
`;

const LeftPanel = styled.div`
    width: 50%;
    border-right: 0.5px solid black;
`;

const RightPanel = styled.div`
    text-align: center;
    width: 50%;
`;

const SearchBar = styled.input`
    margin: 10px auto;
    width: 250px;
    font-size: 20px;
    border-style: none;
    border-bottom: 2px solid grey;
    &:focus {
        outline: none;
    }
`;

const CategoryContainer = styled.div`
    justify-content: right;
    padding-right: 30px;
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



