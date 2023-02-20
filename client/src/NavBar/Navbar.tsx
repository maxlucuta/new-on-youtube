import axios from "axios";
import { useContext } from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router";
import styled from "styled-components";
import logo from "../assets/logo.png";
import { RootContext } from "../context";

const NavBar = () => {
    const { user, updateUser, SERVER_URL } = useContext(RootContext);
    const navigate = useNavigate();
    const signOut = async () => {
        const { message } = (await axios.post(SERVER_URL + "/logout", {})).data;
        console.log(message);
        if (message === "logged out") {
            updateUser("");
            navigate("/");
        } else alert("Unable to sign out");
    };

    return (
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
                <Item>New Search</Item>
            </Link>
            {user && (
                <Link to="/Feed">
                    <Item>Feed</Item>
                </Link>
            )}
            {user && (
                <Link to="/TopicSelection">
                    <Item>Topic Selection</Item>
                </Link>
            )}
            {!user && (
                <Link to={user ? "/" : "/SignIn"}>
                    <Item>Sign In</Item>
                </Link>
            )}
            {!user && (
                <Link to={user ? "/" : "/Register"}>
                    <Item>Register</Item>
                </Link>
            )}
            {user && <SignedInIcon>Signed in as: {user}</SignedInIcon>}
            {user && (
                <Item onClick={signOut} style={{ cursor: "pointer" }}>
                    Sign Out
                </Item>
            )}
        </Bar>
    );
};

export default NavBar;

const Bar = styled.div`
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    background-color: black;
`;

const Item = styled.div`
    margin: 10px 20px;
    color: #fad000;
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
    background-color: #fad000;
    color: black;
`;
