import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { RootContext } from "../context";
import styled from "styled-components";
import testSummaries from "../test/test_summaries.json";
import logo from "../assets/logo.png";
import options from "../assets/options.png";
import select from "../assets/select.png";
import read from "../assets/read.png";
import NavBar from "../NavBar/Navbar";
import { Link } from "react-router-dom";
import { Summary } from "../types";
import Result from "../Result";
import Feed from "../Feed/Feed";

const HomePage = () => {
    const [summaries, updateSummaries] = useState([] as Summary[]);
    const [mode, updateMode] = useState("Feed" as "Feed" | "Popular");

    const { SERVER_URL } = useContext(RootContext);

    const getPopularVideos = async () => {
        const results = await (await axios.get(SERVER_URL + "/popular_videos")).data;
        updateSummaries(results);
    };

    useEffect(() => {
        getPopularVideos();
    }, []);

    return (
        <div>
            <NavBar />
            <div
                style={{
                    backgroundColor: "#FAD000",
                    textAlign: "center",
                }}>
                <div
                    style={{
                        display: "flex",
                        width: "max-content",
                        margin: "0 auto 50px auto",
                        alignItems: "center",
                    }}>
                    <div style={{ margin: "20px" }}>
                        <img width="200px" src={logo} />
                    </div>
                    <div style={{ margin: "20px" }}>
                        <Title>New On YouTube</Title>
                        <SubTitle>Find your favourite videos!</SubTitle>
                    </div>
                </div>

                <div style={{ display: "flex", justifyContent: "space-around" }}>
                    <Panel>
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}>
                            <Number>1</Number>&nbsp;&nbsp;&nbsp;
                            <img src={options} width="75px" />
                        </div>
                        <PanelTitle>Choose your categories</PanelTitle>
                    </Panel>
                    <Panel>
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}>
                            <Number>2</Number>&nbsp;&nbsp;&nbsp;
                            <img src={select} width="75px" />
                        </div>
                        <PanelTitle>Select vidoes you like</PanelTitle>
                    </Panel>
                    <Panel>
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                            }}>
                            <Number>3</Number>&nbsp;&nbsp;&nbsp;
                            <img src={read} width="75px" />
                        </div>
                        <PanelTitle>Checkout their details!</PanelTitle>
                    </Panel>
                </div>

                <Link to="/Search">
                    <Start>New search!</Start>
                </Link>
            </div>

            <div style={{ marginTop: "100px" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <FeedSelector selected={mode === "Feed"} onClick={() => updateMode("Feed")}>
                        Your Feed
                    </FeedSelector>
                    <Title>|</Title>
                    <FeedSelector
                        selected={mode === "Popular"}
                        onClick={() => updateMode("Popular")}>
                        Popular Videos
                    </FeedSelector>
                </div>
            </div>

            <Feed results={summaries} />
        </div>
    );
};

export default HomePage;

const Title = styled.div`
    font-size: 60px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
`;

const SubTitle = styled.div`
    color: grey;
    font-size: 30px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
`;

const Panel = styled.div`
    width: 25%;
    padding: 20px;
    background-color: #ffe200;
    border: 5px solid black;
    &:hover {
        transform: scale(1.1);
    }
`;

const Number = styled.div`
    font-size: 50px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
`;

const PanelTitle = styled.div`
    font-size: 20px;
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
`;

const Start = styled.button`
    width: 30%;
    margin: 50px;
    font-size: 40px;
    background-color: black;
    color: white;
    border: 2px solid #fad000;
    border-radius: 5px;
    padding: 10px;
    &:hover {
        color: #fad000;
        cursor: pointer;
        transform: scale(1.1);
    }
`;

const FeedSelector = styled.div<{ selected: boolean }>`
    font-size: ${props => (props.selected ? "50px" : "30px")};
    font-weight: bold;
    font-family: "Monaco", "Courier New", monospace;
    margin: 20px;
    color: ${props => (props.selected ? "black" : "grey")};
    &:hover {
        color: #fad000;
        cursor: pointer;
    }
`;
