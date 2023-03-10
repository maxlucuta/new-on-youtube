import { useContext, useState, useEffect } from "react";
import styled from "styled-components";
import NavBar from "../NavBar/Navbar";
import { RootContext } from "../context";
import { tokenToEmail, usePost, MAX_TOPICS } from "../functions";
import { ActionMeta, MultiValue } from "react-select";
import Creatable from 'react-select/creatable'

type SelectOption = {
    label: string;
    value: string;
}

const TopicSelection = () => {
    const { token } = useContext(RootContext);
    const [awaitingUserTopics, updateAwaitingUserTopics] = useState(false);
    const [userTopics, updateUserTopics] = useState([] as string[]);
    const [availableTopics, updateAvailableTopics] = useState([] as string[])
    const post = usePost();

    const loadUserTopics = async () => {
        updateAwaitingUserTopics(true);
        const payload = { username: tokenToEmail(token)};
        const response = await post("/get_user_topics", payload) as any;
        if (response.status_code !== 200) console.log("Request Error!", response)
        else {
            updateUserTopics(response.results);
        }
        updateAwaitingUserTopics(false);
    }

    const getAvailableTopics = async () => {
        const response = (await post("/unique_topics", {}));
        if (response.status_code != 200) console.log("Request Error!", response)
        else updateAvailableTopics(response.topics);
    }

    useEffect(() => {
        loadUserTopics();
        getAvailableTopics();
    }, []);

    const updateUserTopicsDatabase = async (topics: string[]) => {
        if (topics.length === 0) {
            return alert("Please select at least one topic");
        }
        const payload = { username: tokenToEmail(token), topics };
        updateAwaitingUserTopics(true);
        const response = await post("/update_user_topics", payload) as any;
        if (response.status_code != 200) {
            alert("Failed to update topics, please try again");
        } else loadUserTopics();
        updateAwaitingUserTopics(false);
    }

    const handleChange = (newValue: MultiValue<SelectOption>, actionMeta: ActionMeta<SelectOption>) => {
        if (newValue.length > MAX_TOPICS) alert("Maximum of 20 topics allowed.");
        else updateUserTopicsDatabase(newValue.map(nv => nv.value));
    }

    const handleNewOption = (newOption: string) => {
        if (userTopics.length > MAX_TOPICS - 1) alert("Maximum of 20 topics allowed.");
        else updateUserTopicsDatabase(userTopics.concat([newOption]));
    }

    return (
    <div>
        <NavBar />
        <div style={{  width: "80%", margin: "auto"  }}>
            <Title>Your Selected Topics</Title>
        </div>
        <div style = {{ width: "80%", margin: "auto" }}>
            <div style = {{ marginTop: "20px" }}>
                <Creatable
                    value = {userTopics.map(t => { return { label: t, value: t }})}
                    options = {availableTopics.map(t => { return { label: t, value: t }})}
                    isClearable=  {true}
                    isSearchable = {true}
                    isMulti = {true}
                    onChange = {handleChange}
                    isLoading = { awaitingUserTopics }
                    onCreateOption = {handleNewOption}
                    isDisabled = {userTopics.length == 0}
                    styles={{
                        control: (baseStyles, state) => ({
                        ...baseStyles,
                        borderColor: state.isFocused ? 'black' : 'black',
                        }),
                        multiValue: (base) => ({
                            ...base,
                            padding: `10px`,
                            margin: `10px`,
                            fontSize: `20px`
                          }),
                    
                    }}
                    theme={(theme) => ({
                        ...theme,
                        borderRadius: 0,
                        colors: {
                        ...theme.colors,
                        primary25: 'var(--colour-background-grey)',
                        primary: 'none',
                        },
                    })}
                />
            </div>
            <div style={{
                marginTop: "30px",
                color: "grey",
                fontWeight: "300",
                textAlign: "center"}}
                >New videos will be added to your feed regularly for any topics shown above.
                Select or search to add new topics to your feed.<br></br>
                Feel free to type in and create new topics. You will just have to wait a few minutes for them to appear in your feed.<br></br>
                Removing topics here will remove all videos for that topic from your feed.
            </div>
        </div>
        {/* { awaitingUserTopics && <div>Loading message goes here!</div> } */}
    </div>
    )
};

export default TopicSelection;

const Title = styled.div`
    padding-bottom: 10px;
    font-size: 50px;
    font-weight: 600;
    font-family: 'Rubik', sans-serif;
    margin-top: 50px;
`;