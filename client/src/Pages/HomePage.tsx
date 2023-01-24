import axios from "axios";
import { useContext, useState } from "react";
import { RootContext } from "../context";
import styled from "styled-components";
import SearchResults from "./SearchResults";
import CategorySelector from "./CategorySelector";

const HomePage = () => {
    const [selectedCategories, updateSelectedCategories] = useState([] as any[]);
    const [mode, updateMode] = useState("Category Selection" as "Category Selection" | "Results");

    const { SERVER_URL } = useContext(RootContext);

    const testServer = async () => {
        console.log(SERVER_URL);
        console.log("Testing backend");
        console.log((await axios.get(SERVER_URL + "/test")).data);
    };

    return (
        <div style={{ textAlign: "center", width: "80%", margin: "auto" }}>
            <Title>Find your favourite videos!</Title>
            <ModeButtonContainer>
                <ModeButton
                    selected={mode == "Category Selection"}
                    onClick={() => updateMode("Category Selection")}>
                    Category Selection
                </ModeButton>
                <ModeButton selected={mode == "Results"} onClick={() => updateMode("Results")}>
                    Search!
                </ModeButton>
            </ModeButtonContainer>

            {mode == "Category Selection" && (
                <CategorySelector
                    selectedCategories={selectedCategories}
                    updateSelectedCategories={updateSelectedCategories}
                />
            )}
            {mode == "Results" && <SearchResults selectedCategories={selectedCategories} />}
        </div>
    );
};

export default HomePage;

const Title = styled.div`
    padding: 50px;
    font-size: 50px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
`;

const ModeButtonContainer = styled.div`
    display: flex;
    width: 100%;
    margin: auto;
    border-bottom: 2px solid #fad000;
    justify-content: center;
`;

const ModeButton = styled.button<{ selected: boolean }>`
    width: 40%;
    font-size: 25px;
    background-color: ${props => (props.selected ? "#fad000" : "white")};
    height: 40px;
    border: 2px solid #fad000;
    border-bottom: none;
    &:hover {
        background-color: ${props => (props.selected ? "#fad000" : "#fff1ac")};
        cursor: pointer;
    }
`;
