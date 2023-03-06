import styled from "styled-components";
import { useContext } from "react";
import { tokenToEmail, thumbnail, url, usePost } from "../functions";
import { Summary } from "../types";

import { RootContext } from "../context";
type ResultProps = {
    summary: Summary;
};

const Result = (props: ResultProps) => {

    const THREE_DAYS = 3*24*3600*1000;
    const isRecent = Date.now() - Date.parse(props.summary.published_at) < THREE_DAYS;

    const { token } = useContext(RootContext);
    const post = usePost();

    const handleWatchVideo = (summary: Summary) => {
        if (token) {
            const payload = { username: tokenToEmail(token), keyword: summary.keyword, video_id: summary.video_id };
            post("/update_user_watched_videos", payload);
        }
    };

    return (
        <Container onClick={() => handleWatchVideo(props.summary)} href = {url(props.summary.video_id)} target = "_blank">
            <Img src={thumbnail(props.summary.video_id)} />
            <MetaData>
            {isRecent && <RecentlyAdded>
                <div style = {{ margin: "10px 0" }}><b>Recently Added!</b></div>
            </RecentlyAdded>}
            <Detail>
                <div style = {{ margin: "10px 0" }}><b>Title</b>: {props.summary.video_title}</div>
            </Detail>
                <div style = {{ margin: "10px 30px" }}><b>Description</b></div>
                <Description>{props.summary.summary}</Description>
                <Detail>
                    <div style = {{ margin: "10px 20px 10px 0" }}><b>Channel</b>: {props.summary.channel_name}</div>
                    <div style = {{ margin: "10px 20px 10px 0" }}><b>Views</b>: {props.summary.views}</div>
                    <div style = {{ margin: "10px 20px 10px 0" }}><b>Likes</b>: {props.summary.likes}</div>
                    <div style = {{ margin: "10px 20px 10px 0" }}><b>Uploaded on</b>: {props.summary.published_at}</div>
                </Detail>
            </MetaData>

        </Container>
    );
};
export default Result;

const Container = styled.a`
    display: flex;
    align-items: center;
    text-decoration: none;
    color: black;
    padding: 10px;
    background-color: none;
    border-radius: 10px;
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    margin: 20px 0;
    &:hover {
        cursor: pointer;
        background-color: #e1e1e1;
    }
`;

const Img = styled.img`
    border-radius: 10px;
    height: 200px;
`;

const MetaData = styled.div`

`;

const Detail = styled.div`
    display: flex;
    margin-left: 30px;
`;

const RecentlyAdded = styled.div`
    display: flex;
    margin-left: 30px;
    color: ${"#e52b87"};
`;

const Description = styled.div`
    margin: 5px 30px 5px 30px;
    text-align: left;
    width: 85%;
    font-size: 20px;
`;
