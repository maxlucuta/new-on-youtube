import { useContext, useState } from "react";
import styled from "styled-components";
import Result from "../Result";
import SummaryModal from "./SummaryModal";
import { Summary } from "../types";
import { RootContext } from "../context";
import { tokenToEmail, usePost } from "../functions";

type FeedProps = {
    results: Summary[];
};

const defualtSummary: Summary = {
    video_id: "JRPC7a_AcQo",
    summary: "This is just a placeholder video, database connection failed or empty",
    video_title: "Placeholder video",
    channel_name: "Placeholder channel name"
};

const Feed = (props: FeedProps) => {
    const { token } = useContext(RootContext);
    const [summaryModalOpen, updateSummaryModalOpen] = useState(false);
    const [selectedSummary, updateSelectedSummary] = useState(defualtSummary as Summary);
    const post = usePost();

    const selectResult = (summary: Summary) => {
        updateSelectedSummary(summary);
        updateSummaryModalOpen(true);
        if (token) {
            const payload = { username: tokenToEmail(token), video_id: summary.video_id };
            post("/update_user_watched_videos", payload);
        }
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
