import { useContext, useState , useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import axios from "axios";
import { RootContext } from "../context";

const TopicSelection = () => {
    const { SERVER_URL } = useContext(RootContext);
    const [selectedTopics, updateSelectedTopics] = useState([]);

    const handleSelectedTopics= async () => {
        const response = (await axios.post(SERVER_URL + "/user_topics")).data;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateSelectedTopics(response.results);
    };

    return (
        <div>
            <NavBar />
            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Your Selected Topics</Title>
            </div>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: "max-content",
                    margin: "auto",
                }}>
            </div>

            <div style={{ width: "60%", margin: "auto" }}>
                {selectedTopics.map(r => (<Title>{r}</Title>))}
            </div>

            <SubmitButton active={true} onClick={handleSelectedTopics}>
                Load Topics
            </SubmitButton>
        </div>
    );
};

export default TopicSelection;

const Title = styled.div`
    font-size: 60px;
    font-weight: bold;
    margin: auto;
    padding: 50px 0;
    width: max-content;
`;

const FeedSelector = styled.div<{ selected: boolean }>`
    font-size: 30px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
    text-decoration: ${props => (props.selected ? "underline" : "none")};
    margin: 20px;
    &:hover {
        color: #fad000;
        cursor: pointer;
    }
`;

const Result = styled.a`
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

const SubmitButton = styled.button<{ active: boolean }>`
    padding: 12px 30px;
    width: 40%;
    margin-top: 40px;
    background-color: black;
    opacity: ${props => (props.active ? "1" : "0.2")};
    color: white;
    font-weight: bold;
    border: none;
    outline: none;
    border-radius: 20px;
    &:hover {
        cursor: ${props => (props.active ? "pointer" : "not-allowed")};
        background-color: ${props => (props.active ? "#750000" : "black")};
    }
`;