import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import Feed from "../Feed/Feed";
import { tokenToEmail, usePost } from "../functions";
import { Summary } from "../types";
import { RootContext } from "../context";
import refresh from "../assets/refresh.png";
import Spinner from "../spinner";

const FeedPage = () => {
    const { token } = useContext(RootContext);
    const modes = ["Recent", "Popular", "Liked", "Recommended", "Random"] as ["Recent", "Popular", "Liked", "Recommended", "Random"];
    const [mode, updateMode] = useState("Recent" as String);
    const [searchResults, updateResults] = useState([] as Summary[]);
    const post = usePost();

    const handleRequest = async (sort_by_mode: String | ((prevState: String) => String)) => {
        const payload = { username: tokenToEmail(token), amount: 20, sort_by: sort_by_mode };
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
                        {i !== 0 ? <div style={{ fontSize: "30px", margin: "0 20px 0 20px" }}>|</div> : <></>}
                        <FeedSelector selected={mode === m} onClick={() => { updateMode(m); handleRequest(m); }}>
                            {m}
                        </FeedSelector>
                    </>
                ))}
                <RefreshButton
                    style={{ display: "flex", margin: "0 20px 0 20px" }}
                    onClick={() => {
                        handleRequest(mode);
                    }}>
                    <div><RefreshIcon src={refresh} /></div>
                </RefreshButton>
            </div>
            {noResults && mode === "Recommended" && <div style={{ textAlign: "center", color: "grey" }}>Please watch at least one video to receive recommendations</div>}
            {noResults && mode !== "Recommended" && <Loading style={{ textAlign: "center", color: "grey" }}>Generating videos, please wait a few minutes</Loading>}
            {noResults && mode !== "Recommended" && <div><Spinner/></div>}
            <div style={{ width: "80%", margin: "auto" }}>
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

const Loading = styled.div`
padding-bottom: 15px;
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

const RefreshIcon = styled.img`
    width: 30px;
    margin-top: 10px;
    `