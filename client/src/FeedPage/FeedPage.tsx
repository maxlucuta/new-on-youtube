import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import Feed from "../Feed/Feed";
import { tokenToEmail, usePost } from "../functions";
import { Summary } from "../types";
import { RootContext } from "../context";

const FeedPage = () => {
    const { token } = useContext(RootContext);
    const modes = ["Most viewed", "Recommended", "Most liked", "Random"] as ["Most viewed", "Recommended", "Most liked", "Random"];
    const [mode, updateMode] = useState("Most viewed" as String);
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
            </div>

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