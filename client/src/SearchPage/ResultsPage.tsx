import { Dispatch, SetStateAction } from "react";
import styled from "styled-components";
import { Summary } from "../types";
import Feed from "../Feed/Feed";

type ResultsPageProps = {
    updateMode: Dispatch<SetStateAction<"SELECTION" | "RESULTS">>;
    updateSelection: Dispatch<SetStateAction<string[]>>;
    updateSearchResults: Dispatch<SetStateAction<Summary[]>>;
    handleSubmission: () => void;
    searchResults: Summary[];
}

const ResultsPage = (props: ResultsPageProps) => {

    return (
        <>
            <div style = {{ display: "flex", marginBottom: "20px" }}>
                <NewSearchButton
                    onClick={() => {
                        props.updateMode("SELECTION")
                        props.updateSelection([]);
                        props.updateSearchResults([]);
                    }}>
                    New Search
                </NewSearchButton>
                <RefreshButton onClick={props.handleSubmission}>
                    Refresh
                </RefreshButton>
            </div>
            {/*  add loading logic */}
            <Feed results={props.searchResults} />
        </>
    );
};

export default ResultsPage;

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


const RefreshButton = styled.div`
    width: 100px;
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
