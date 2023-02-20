import axios from "axios";
import { useContext } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import logo from "../assets/logo.png";
import { RootContext } from "../context";

const backgroundGrey = '#f0f0f1';

const NavBar = () => {
    const { user, updateUser, SERVER_URL } = useContext(RootContext);
    const signOut = async () => {
        const { message } = (await axios.post(SERVER_URL + "/logout", {})).data;
        console.log(message);
        if (message === "logged out") updateUser("");
        else alert("Unable to sign out");
    };

    return (
        <Backing>
            <Bar>
                <Link to="/">
                    <Logo>
                        <div style={{ margin: "5px 10px 0 10px" }}>
                            <img src={logo} width="30px" />
                        </div>
                        <div>New on YouTube</div>
                    </Logo>
                </Link>
                <Link to="/Search">
                    <Item>Search</Item>
                </Link>
                <Link to="/Feed">
                    <Item>Feed</Item>
                </Link>
                {user && <SignedInIcon>Signed in as: {user}</SignedInIcon>}
                {user && (
                    <Item onClick={signOut} style={{ cursor: "pointer" }}>
                        Sign Out
                    </Item>
                )}
            </Bar>
            <SignInButton>
                {!user && (
                    <Link to={user ? "/" : "/SignIn"}>
                        <Item>Sign In</Item>
                    </Link>
                )}
            </SignInButton>
        </Backing>
    );
};

export default NavBar;

const Backing = styled.div`
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    background-color: ${backgroundGrey};
`;

const Bar = styled.div`
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    background-color: ${backgroundGrey};
    margin: 0 auto 0 400px;
`;

const SignInButton = styled.button`
    display: flex;
    flex-direction: row-reverse;
    position: sticky;
    color: black;
    top: 0;
    background-color: ${backgroundGrey};
    margin: 0 500px 0 auto;
    border-color: #e52b87;
    border-radius: 5px;
    transition: 0.5s;
    &:hover {
        color: white;
        background-color: #e52b87;
        cursor: pointer;
        transform: scale(1.0);
    }
`;

const Item = styled.div`
    margin: 10px 20px;
    color: black;
`;

const SignedInIcon = styled.div`
    margin: 10px 20px;
    color: green;
`;

const Logo = styled.div`
    display: flex;
    align-items: center;
    margin: 5px;
    border-radius: 10px;
    padding: 0 10px 0 0;
    background-color: ${backgroundGrey};
    color: black;
`;
