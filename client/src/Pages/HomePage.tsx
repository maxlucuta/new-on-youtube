import axios from "axios";
import { useContext, useState } from "react";
import { RootContext } from "../context";
import styled from "styled-components";


const HomePage = () => {
    const [serverResponse, updateServerResponse] = useState({success: false, message: "Click button to test!"});

    const { SERVER_URL } = useContext(RootContext)

    const testServer = async () => {
        console.log(SERVER_URL)
        const res = (await axios.get(SERVER_URL + "/test")).data;
        updateServerResponse(res);
    }

    return (
        <div style = {{ textAlign: "center", width: "80%", margin: "auto" }}>
            <Title>YouTube Recommendations App</Title>
            <Button onClick = {testServer}>Test Server!</Button>
            <Box success = { serverResponse.success }> { serverResponse.message }</Box>
        </div>
    )
}

export default HomePage;

const Title = styled.div`
    padding: 50px;
    font-size: 50px;
`

const Button = styled.button`
    background-color: #FAD000;
    border-radius: 5px;
    border-style: none;
    display: block;
    margin: auto;
    width: 50%;
    font-size: 25px;
    padding: 10px;
    cursor: pointer;
    &:hover {
        transform: scale(1.03);
    }
`

const Box = styled.button<{success: boolean}>`
    display: block;
    margin: 20px auto;
    width: 50%;
    height: 200px;
    font-size: 25px;
    background-color: ${ props => props.success ? "#7aff8a" : "grey" };
    border-radius: 5px;
    border-style: none;
`