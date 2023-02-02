import { Link } from "react-router-dom";
import styled from "styled-components";
import logo from "../assets/logo.png";

const NavBar = () => {
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
            <Item>Previous Searches</Item>
            <Item>Account</Item>
            <Item>Sign In</Item>
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

const Logo = styled.div`
    display: flex;
    align-items: center;
    margin: 5px;
    border-radius: 10px;
    padding: 0 10px 0 0;
    background-color: #fad000;
    color: black;
`;
