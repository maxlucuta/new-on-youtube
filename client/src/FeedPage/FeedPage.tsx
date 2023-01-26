import { useState } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import testSummaries from "../test/test_summaries.json";

const FeedPage = () => {
    const modes = ["Recent", "Popular", "Favourites"] as ["Recent", "Popular", "Favourites"];
    const [mode, updateMode] = useState("Recent" as "Recent" | "Popular" | "Favourites");
    return (
        <div>
            <NavBar />
            <div style={{ backgroundColor: "#FAD000" }}>
                <Title>Your Feed</Title>
            </div>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    width: "max-content",
                    margin: "auto",
                }}>
                {modes.map((m, i) => (
                    <>
                        {i !== 0 ? <Title>|</Title> : <></>}
                        <FeedSelector selected={mode === m} onClick={() => updateMode(m)}>
                            {m}
                        </FeedSelector>
                    </>
                ))}
            </div>

            <div style={{ width: "60%", margin: "auto" }}>
                {testSummaries.map(r => (
                    <Result href={r.url}>
                        <Img src={r.thumbnail} />
                        <Description>{r.description}</Description>
                    </Result>
                ))}
            </div>
        </div>
    );
};

export default FeedPage;

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
