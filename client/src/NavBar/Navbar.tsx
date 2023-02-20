import axios from "axios";
import { useContext } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import logo from "../assets/logo.png";
import { RootContext } from "../context";
import { tokenToEmail, usePost } from "../functions";

const NavBar = () => {
    const { token, setToken } = useContext(RootContext);
    const post = usePost();
    const signOut = async () => { setToken("") };
    const testJWT = () => {
        const res = post("/my_categories", {echo: "ecgo"})
        console.log("Response: ", res, token)
    }
    

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
            <Link to="/Feed">
                <Item>Feed</Item>
            </Link>
            {!token && (
                <Link to={token ? "/" : "/SignIn"}>
                    <Item>Sign In</Item>
                </Link>
            )}
            {!token && (
                <Link to={token ? "/" : "/Register"}>
                    <Item>Register</Item>
                </Link>
            )}
            {token && <SignedInIcon>Signed in as: {tokenToEmail(token)}</SignedInIcon>}
            {token && (
                <Item onClick={signOut} style={{ cursor: "pointer" }}>
                    Sign Out
                </Item>
            )}
            {token && (
                <Item onClick={testJWT} style={{ cursor: "pointer" }}>
                    Test JWT refresh
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
