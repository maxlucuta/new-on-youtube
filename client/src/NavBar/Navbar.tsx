import { useContext } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import logo from "../assets/logo.png";
import { RootContext } from "../context";
import { tokenToEmail } from "../functions";

const NavBar = () => {
    const { token, setToken } = useContext(RootContext);
    const signOut = async () => { setToken("") };

    return (
        <Backing>
            <Bar>
                <Link to="/">
                    <Logo>
                        <div style={{ margin: "5px 10px 0 10px" }}>
                            <img src={logo} width="30px" />
                        </div>
                        <div style={{
                            fontSize: "16px",
                            fontWeight: "400",
                            fontFamily: "'Rubik', sans-serif"
                        }}>New on YouTube</div>
                    </Logo>
                </Link>
                <Link to="/Search">
                    <Item>Search</Item>
                </Link>

                {token && (
                    <Link to={token ? "/Feed" : "/"}>
                        <Item>Feed</Item>
                    </Link>
                )}
                {token && (
                    <Link to={token ? "/TopicSelection" : "/"}>
                        <Item>Topics</Item>
                    </Link>
                )}
                {!token && (
                    <Link to={token ? "/" : "/Register"}>
                        <Item>Register</Item>
                    </Link>
                )}
                {token && <SignedInIcon>Signed in as: {tokenToEmail(token)}</SignedInIcon>}
            </Bar>
            <SignInOutButton>
                {!token && (
                    <Link to={token ? "/" : "/SignIn"}>
                        <Item>Sign In</Item>
                    </Link>
                )}
                {token && (
                    <Link to={token ? "/" : "/"}>
                        <Item onClick={signOut} style={{ cursor: "pointer" }}>Sign Out</Item>
                    </Link>
                )}
            </SignInOutButton>
        </Backing>

    );
};

export default NavBar;

const Backing = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 10px;
    background-color: none;
    margin-left: 20%;
`;

const Bar = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 10px;
    background-color: none;

`;

const Item = styled.div`
    margin: 10px 20px;
    color: black;
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
    transition: 0.5s;
    &:hover {
        text-decoration: underline;
    }
`;

const SignInOutButton = styled.button`
    display: flex;
    flex-direction: row-reverse;
    position: sticky;
    color: black;
    top: 0;
    background-color: none;
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

const SignedInIcon = styled.div`
    margin: 10px 20px;
    color: #707070;
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
`;

const Logo = styled.div`
    display: flex;
    align-items: center;
    margin: 5px;
    border-radius: 10px;
    padding: 0 10px 0 0;
    background-color: none;
    color: black;
`;
