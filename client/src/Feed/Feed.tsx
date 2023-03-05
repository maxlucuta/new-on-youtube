import styled from "styled-components";
import Result from "./Result";
import { Summary } from "../types";

type FeedProps = {
    results: Summary[];
};

const defaultSummary: Summary = {
    video_id: "JRPC7a_AcQo",
    summary: "This is just a placeholder video, database connection failed or empty",
    video_title: "Placeholder video",
    channel_name: "Placeholder channel name",
    keyword: "Placeholder keyword",
    likes: 1,
    views: 1,
    published_at: "Placeholder date"
};

const Feed = (props: FeedProps) => {

    return (
        <SearchResults>
            {props.results.map(r => (
                <Result summary={r} />
            ))}
        </SearchResults>
    );
};

export default Feed;

const SearchResults = styled.div`
    width: 100%;
    margin: auto;
`;
