import axios from "axios";
import { useEffect } from "react";
import styled from "styled-components";
import { thumbnail, url } from "../functions";
import { Summary } from "../types";

type ResultProps = {
    summary: Summary;
};

const Result = (props: ResultProps) => {

    return (
        <Container href = {url(props.summary.video_id)} target = "_blank">
            <Img src={thumbnail(props.summary.video_id)} />
            <MetaData>
            <Detail>
                <div style = {{ margin: "10px 0" }}><b>Title</b>: {props.summary.video_title}</div>
            </Detail>
                <div style = {{ margin: "10px 30px" }}><b>Description</b></div>
                <Description>{props.summary.summary}</Description>
                <Detail>
                 <div style = {{ margin: "10px 0" }}><b>Channel</b>: {props.summary.channel_name}</div>
                    <div style = {{ margin: "10px 0" }}><b>View Count</b>: {props.summary.views}</div>
                    <div style = {{ margin: "10px 0" }}><b>Likes</b>: {props.summary.likes}</div>
                </Detail>
            </MetaData>
            
        </Container>
    );
};
export default Result;

const Container = styled.a`
    display: flex;
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
    width: 50%;
`;

const MetaData = styled.div`
    
`;

const Detail = styled.div`
    margin-left: 30px;
`;

const Description = styled.div`
    margin: 5px 30px 5px 30px;
    text-align: left;
    width: 85%;
    font-size: 20px;
`;
