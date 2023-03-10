import { Link } from "react-router-dom"
import styled from "styled-components"
import NavBar from "../NavBar/Navbar"


const TimeOut = () => {
    return (
        <>
            <NavBar/>
            <Alert>
                You have been logged out due to inactivity, please sign in again!
                <Link to = "/SignIn">
                    <SignInButton>
                        Sign In
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
    background-color: var(--colour-background-grey);
    border-radius: 5px;
`

const SignInButton = styled.div`
    width: 200px;
    margin: 20px auto 0 auto;
    color: white;
    padding: 10px;
    background-color: var(--colour-pink-accent);
    border-radius: 5px;
`