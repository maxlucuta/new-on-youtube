import { useContext } from "react";
import { RootContext } from "../context";
import styled from "styled-components";
import heroImage from "../assets/logoColour.png";
import nlpIcon from "../assets/nlpClear.png";
import choiceIcon from "../assets/choiceClear.png";
import recommendIcon from "../assets/recommend.png";
import feedIcon from "../assets/filmReel.png";
import NavBar from "../NavBar/Navbar";
import { Link, Navigate } from "react-router-dom";
import { detectMobile } from "../functions";

const HomePage = () => {
    const { token } = useContext(RootContext);

    //if (detectMobile()) return <Navigate replace to="/UnsupportedDevice" />;

    return (
        <div>
            <div
                style={{
                    backgroundColor: "var(--colour-background-grey)", 
                    paddingBottom: "5px",
                    textAlign: "left",
                    minWidth: "100%"
                }}>
                <NavBar />
                <Container>
                    <HeroBox>
                        <div style={{ margin: "10px", paddingRight: "130px" }}>
                            <Title>New On YouTube</Title>
                            <SubTitle>Daily videos on your favourite topics, <br></br>summarised.</SubTitle>
                            <Text>Harness the power of GPT-3 and use detailed video summaries</Text>
                            <Text>to find what interests you, faster.</Text>
                            <br></br>
                            <Text>No promotions. No marketing. Just content.</Text>
                            <Link to={token ? "/Feed" : "/Register"}>
                                {token ? <Start>Go To Video Feed</Start> : <Start>Register Now</Start> }
                            </Link>
                        </div>


                        <div style={{ width: "max-content" , textAlign: "left"}}>
                            <LogoImage  src={heroImage} alt="New on YouTube logo"/>
                        </div>
                    </HeroBox>
                </Container>
            </div>

            <Container>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <SubTitle>Finding out what's new on YouTube</SubTitle>
                    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "left"}}>
                        <Panel>
                            <PanelIcon src={choiceIcon}/>
                            <PanelTitle>Choose your topics</PanelTitle>
                            <Text>Choose the topics that interest you from our library of topics, 
                                or set your own custom topics. Whatever the topic, we can fetch the videos.</Text>
                        </Panel>

                        <Panel>
                            <PanelIcon src={nlpIcon}/>
                            <PanelTitle>Generate Summaries</PanelTitle>
                            <Text>We process the transcripts of your videos with GPT-3 to give 
                                you a clear written summary of the full video, in plain English.</Text>
                        </Panel>
                    </div>
                    <div></div>
                    <div style={{ display: "flex", flexWrap: "wrap" , justifyContent: "left"}}>
                        <Panel>
                            <PanelIcon src={feedIcon}/>
                            <PanelTitle>Browse your feed</PanelTitle>
                            <Text>Your feed will be updated with the latest and most popular YouTube 
                                videos for the topics you selected. Check back regularly to enjoy more new videos.</Text>
                        </Panel>
                        <Panel>
                            <PanelIcon src={recommendIcon}/>
                            <PanelTitle>Get recommendations</PanelTitle>
                            <Text>Watch the videos you like and we'll add similar videos to 
                                your recommendations with every click. So you can always find something new to watch.</Text>
                        </Panel>
                        
                    </div>
                </div>
            </Container>
        </div>
    );
};

export default HomePage;

const Container = styled.div`
    width: 80%;
    margin: 50px auto;
`;

const HeroBox = styled.div`
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 10px;
`;

    

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
    height: max-content;
    text-align: justify;
    text-justify: inter-word;
    margin: 20px 40px 20px 0;
    padding: 30px 30px 45px 30px;
    background-color: var(--colour-background-grey);
    border: none;
    border-radius: 30px;
    transition: 0.3s;
    &:hover {
        background-color: var(--colour-background-darker-grey);
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
    background-color: none;
    color: black;
    border-color: #e52b87;
    border-radius: 5px;
    padding: 10px;
    transition: 0.5s;
    &:hover {
        color: white;
        background-color: var(--colour-pink-accent);
        cursor: pointer;
    }
`;

const LogoImage = styled.img`
    width: 250px;
    margin-top: 50px;
    filter: drop-shadow(0 0.3rem 0.25rem grey);
`;