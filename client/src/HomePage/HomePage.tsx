import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { RootContext } from "../context";
import styled from "styled-components";
import testSummaries from "../test/test_summaries.json";
import laptop from "../assets/laptop.png";
import nlpIcon from "../assets/nlpClear.png";
import choiceIcon from "../assets/choiceClear.png";
import NavBar from "../NavBar/Navbar";
import { Link } from "react-router-dom";
import { Summary } from "../types";
import Result from "../Result";
import Feed from "../Feed/Feed";
import Simple from "./Simple";

const backgroundGrey = '#f0f0f1';

const HomePage = () => {
    const [summaries, updateSummaries] = useState([] as Summary[]);
    const [mode, updateMode] = useState("Feed" as "Feed" | "Popular");

    const { SERVER_URL } = useContext(RootContext);

    const getPopularVideos = async () => {
        const response = await (await axios.get(SERVER_URL + "/popular_videos")).data;
        if (response.status_code != 200) alert(SERVER_URL)
        else updateSummaries(response.results);
    };

    useEffect(() => {
        getPopularVideos();
    }, []);

    return (
        <div>
            <NavBar />
            <div
                style={{
                    backgroundColor: backgroundGrey,
                    textAlign: "left",
                }}>
                <div
                    style={{
                        display: "flex",
                        width: "max-content",
                        margin: "0 auto 0 400px",
                        paddingTop: "75px",
                        paddingBottom: "50px",
                        alignItems: "left",
                    }}>

                    <div style={{ margin: "20px" }}>
                        <Title>New On YouTube</Title>
                        <SubTitle>Daily videos on your favourite topics, <br></br>summarised.</SubTitle>
                        <Text>Harness the power of GPT-3 and use detailed video summaries</Text>
                        <Text>to find what interests you, faster.</Text>
                        <br></br>
                        <Text>No promotions. No marketing. Just content.</Text> 
                        <Link to="/Register">
                            <Start>Register Now</Start>
                        </Link>
                    </div>

                    <div style={{ margin: "20px" , width: "500px"}}>
                        <div><LaptopImage src={laptop}/></div>
                    </div>  
                    
                </div>
                
            </div>

            <div style={{ marginTop: "100px", marginLeft: "400px" }}>
                <div style={{ display: "flex", flexDirection: "column", justifyContent: "left" }}>
                    <SubTitle>Finding out what's new on YouTube</SubTitle>
                    <div style={{ display: "flex"}}>
                        <Panel>
                            <PanelIcon src={choiceIcon}/>
                            <PanelTitle>Choose your topics</PanelTitle>       
                            <Text>Choose something from our comprehensive library of topics or customise your own.</Text> 
                        </Panel>
                        
                        <Panel>
                            <PanelIcon src={nlpIcon}/>
                            <PanelTitle>Generate Summaries</PanelTitle>       
                            <Text>We process the transcripts of your videos to give you a clear written summary of the full video, in plain English.</Text>
                        </Panel>
                    </div>
                    <div></div>
                    <div style={{ display: "flex"}}>
                        <Panel>Recommendations</Panel>
                        <Panel>Feed</Panel>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HomePage;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
`;

const SubTitle = styled.div`
    padding-bottom: 20px;
    font-size: 30px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
`;

const Text = styled.div`
    padding-top: 5px;
    font-size: 18px;
    font-weight: 300;
    font-family: 'Rubik', sans-serif;
`;

const Panel = styled.div`
    width: 400px;
    height: 300px;
    margin: 20px;
    padding: 30px;
    background-color: ${backgroundGrey};
    border: none;
    border-radius: 30px;
    transition: 0.3s;
    &:hover {
        background-color: #e4e4e5;
    }
`;

const PanelIcon = styled.img`
    width: 75px;
    }
`;

const PanelTitle = styled.div`
    padding-top: 30px;
    padding-bottom: 15px;
    font-size: 20px;
    font-weight: 500;
    font-family: 'Rubik', sans-serif;
`;



const Start = styled.button`
    width: 200px;
    margin-top: 40px;
    font-size: 20px;
    font-weight: regular;
    font-family: 'Rubik', sans-serif;
    background-color: ${backgroundGrey};
    color: black;
    border-color: #e52b87;
    border-radius: 5px;
    padding: 10px;
    transition: 0.5s;
    &:hover {
        color: white;
        background-color: #e52b87;
        cursor: pointer;
        transform: scale(1.0);
    }
`;

const LaptopImage = styled.img`
    width: 550px;
    filter: drop-shadow(0 0.3rem 0.25rem grey);
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
