import styled from "styled-components";
import { thumbnail } from "./functions";
import { Summary } from "./types";

type ResultProps = {
    summary: Summary;
};

const Result = (props: ResultProps) => {
    return (
        <Container>
            <Img src={thumbnail(props.summary.video_id)} />
            <Description>{props.summary.summary}</Description>
        </Container>
    );
};

export default Result;

const Container = styled.a`
    display: flex;
    text-decoration: none;
    color: black;
    align-items: center;
    padding: 10px;
    background-color: #e1e1e1;
    border-radius: 10px;
    margin: 20px 0;
    &:hover {
        cursor: pointer;
        background-color: #fff1ac;
    }
`;

const Img = styled.img`
    border-radius: 10px;
    width: 15%;
`;

const Description = styled.div`
    text-align: center;
    width: 85%;
    font-size: 25px;
`;
