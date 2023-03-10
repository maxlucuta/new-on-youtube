import { Dispatch, SetStateAction } from "react";
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
            <Feed results={props.searchResults} />
        </>
    );
};

export default ResultsPage;