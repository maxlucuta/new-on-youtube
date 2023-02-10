import { useState } from "react";
import styled from "styled-components";
import Result from "../Result";
import SummaryModal from "./SummaryModal";
import { Summary } from "../types";

type FeedProps = {
    results: Summary[];
};

const defualtSummary: Summary = {
    id: "JRPC7a_AcQo",
    description: "This is just a placeholder video, database connection failed or empty",
    title: "Placeholder video",
};

const Feed = (props: FeedProps) => {
    const [summaryModalOpen, updateSummaryModalOpen] = useState(false);
    const [selectedSummary, updateSelectedSummary] = useState(defualtSummary as Summary);

    const selectResult = (summary: Summary) => {
        updateSelectedSummary(summary);
        updateSummaryModalOpen(true);
    };

    return (
        <SearchResults>
            {summaryModalOpen && (
                <SummaryModal
                    updateSummaryModalOpen={updateSummaryModalOpen}
                    summary={selectedSummary}
                />
            )}
            {props.results.map(r => (
                <span onClick={() => selectResult(r)}>
                    <Result summary={r} />
                </span>
            ))}
        </SearchResults>
    );
};

export default Feed;

const SearchResults = styled.div`
    width: 60%;
    border-top: 5px solid black;
    margin: auto;
`;
