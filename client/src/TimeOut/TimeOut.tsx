import { Link } from "react-router-dom"
import styled from "styled-components"
import NavBar from "../NavBar/Navbar"


const TimeOut = () => {
    return (
        <>
            <NavBar/>
            <Alert>
                You have been logged out due to inactivity, please Sign in again!
                <Link to = "/SignIn">
                    <SignInButton>
                        SIGN IN
                    </SignInButton>
                </Link>
            </Alert>
        </>
    )
}

export default TimeOut

const Alert = styled.div`
    width: 80%;
    margin: 50px auto;
    text-align: center;
    padding: 50px 20px;
    background-color: #fad000;
    border-radius: 5px;
`

const SignInButton = styled.div`
    width: 200px;
    margin: 20px auto 0 auto;
    background-color: black;
    color: #fad000;
    border-radius: 5px;
`