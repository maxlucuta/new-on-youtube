import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import Feed from "../Feed/Feed";
import { tokenToEmail, usePost } from "../functions";
import { Summary } from "../types";
import { RootContext } from "../context";

const FeedPage = () => {
    const { token } = useContext(RootContext);
    const modes = ["Recent", "Popular", "Favourites"] as ["Recent", "Popular", "Favourites"];
    const [mode, updateMode] = useState("Recent" as "Recent" | "Popular" | "Favourites");
    const [searchResults, updateResults] = useState([] as Summary[]);
    const post = usePost();

    const handleRequest = async () => {
        const payload = { username: tokenToEmail(token), amount: 5, sort_by: mode};
        const response = await post("/user_request", payload) as any;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateResults(response.results);
    };

    useEffect(() => {
        handleRequest();
    }, []);

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

            <div>
                <Feed results={searchResults} />
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
        background-color: red;
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
