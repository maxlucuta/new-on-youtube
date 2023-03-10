import { Dispatch, SetStateAction } from "react";
import styled from "styled-components";
import { Summary } from "../types";
import Feed from "../Feed/Feed";
import refresh from "../assets/refresh.png";

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
            <Feed results={props.searchResults} />
        </>
    );
};

export default ResultsPage;