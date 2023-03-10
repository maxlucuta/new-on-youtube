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
            <BarNav>
                <NavBarItems>
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
                    <NavBarItemContainer>
            
                        <Link to="/Search">
                            <NavBarItem>Search</NavBarItem>
                        </Link> 
        
                        {token && (
                            <Link to={token ? "/Feed" : "/"}>
                                <NavBarItem>Feed</NavBarItem>
                            </Link>
                        )}
                        {token && (
                            <Link to={token ? "/TopicSelection" : "/"}>
                                <NavBarItem>Topics</NavBarItem>
                            </Link>
                        )}
                        {!token && (
                            <Link to={token ? "/" : "/Register"}>
                                <NavBarItem>Register</NavBarItem>
                            </Link>
                        )}
                        {/* Removed sign in text for now. Replace with icon with info tooltip on hover?*/}
                        {/*{token && <SignedInIcon>Signed in as: {tokenToEmail(token)}</SignedInIcon>}*/}
                    </NavBarItemContainer>
                </NavBarItems>
                <div style={{paddingTop: "10px"}}>
                <Link to={token ? "/" : "/SignIn"}>
                    <SignInOutButton onClick={token ? signOut : function(){}} style={{ cursor: "pointer" }}>
                        {token ? "Sign Out" : "Sign In"}
                    </SignInOutButton>  
                </Link>
                </div>

            </BarNav>
            
    );
};

export default NavBar;

const Bar = styled.div`
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-top: 10px;
    background-color: none;

`;

const BarNav = styled.div`
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-top: 20px;
    background-color: none;
    width: 80%;
    margin: 5px auto;

`;
const NavBarItemContainer = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
`;

const NavBarItems = styled.div`
    flex: 1;
    display: flex;
    justify-content: flex-start;
    align-items: center;
`;

const NavBarItem = styled.p`
    color: black;
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
    margin-right: 30px;
    transition: 0.5s;
    &:hover {
        text-decoration: underline;
    }
`;

const SignInOutButton = styled.button`
    display: flex;
    flex-direction: flex-end;
    padding: 10px;
    font-size: 16px;
    font-weight: 400;
    font-family: 'Rubik', sans-serif;
    width: max-content;
    border-color: var(--colour-pink-accent);
    border-radius: 5px;
    transition: 0.5s;
    &:hover {
        background-color: var(--colour-pink-accent);
        color: white;
        cursor: pointer;    
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
    margin-right: 30px;
    border-radius: 10px;
    padding: 0 10px 0 0;
    background-color: none;
    color: black;
`;
