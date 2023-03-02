import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import Feed from "../Feed/Feed";
import { tokenToEmail, usePost } from "../functions";
import { Summary } from "../types";
import { RootContext } from "../context";

const FeedPage = () => {
    const { token } = useContext(RootContext);
    const modes = ["Recommended", "Popular", "Liked", "Recent", "Random"] as ["Recommended", "Popular", "Liked", "Recent", "Random"];
    const [mode, updateMode] = useState("Recommended" as String);
    const [searchResults, updateResults] = useState([] as Summary[]);
    const post = usePost();

    const handleRequest = async (sort_by_mode: String | ((prevState: String) => String)) => {
        const payload = { username: tokenToEmail(token), amount: 20, sort_by: sort_by_mode};
        const response = await post("/user_request", payload) as any;
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateResults(response.results);
    };

    useEffect(() => {
        handleRequest(mode);
    }, []);

    const noResults = searchResults.length === 0;

    return (
        <div>
            <NavBar />
            <div>
                <Title>Your Feed</Title>
            </div>
            <div
                style={{
                    display: "flex",
                    alignItems: "center",
                    width: "max-content",
                    marginLeft: "20%",
                }}>
                {modes.map((m, i) => (
                    <>
                        {i !== 0 ? <div style={{fontSize: "30px", margin: "0 20px 0 20px"}}>|</div>: <></>}
                        <FeedSelector selected={mode === m} onClick={() => {updateMode(m); handleRequest(m);}}>
                            {m}
                        </FeedSelector>
                    </>
                ))}
                <RefreshButton
                    style={{display: "flex", margin: "0 20px 0 20px"}}
                    onClick={() => {
                        handleRequest(mode);
                    }}>
                    Refresh
                </RefreshButton>
            </div>
            {noResults ? mode === "Recommended" && <div style={{textAlign: "center"}}>Please watch at least one video to receive recommendations</div> : <div></div>}
            {noResults ? mode !== "Recommended" && <div style={{textAlign: "center"}}>Generating videos, please wait a few minutes</div> : <div></div>}
            <div>
                <Feed results={searchResults} />
            </div>
        </div>
    );
};

export default FeedPage;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-left: 20%;
    margin-top: 50px;
`;

const FeedSelector = styled.div<{ selected: boolean }>`
    font-size: 30px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    color: ${props => (props.selected ? "#e52b87" : "black")};
    margin: 20px 0 20px 0;
    &:hover {
        background-color: ${props => (props.selected ? "none" : "#f0f0f1")};;
        cursor: ${props => (props.selected ? "default" : "pointer")};
    }
`;

const RefreshButton = styled.div`
    width: 100px;
    margin: 40px 0 0 40px;
    font-size: 20px;
    text-align: center;
    background-color: #f0f0f1;
    color: black;
    border-style: none;
    border-radius: 5px;
    padding: 10px;
    font-size: 20px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
    &:hover {
        cursor: pointer;
        transform: scale(1.1);
    }
`;