import img from "./img.png";
import "./signin.css";

const SignInPage = () => {
    return (
        <div className="signin_background">
            <div className="container">
                <form action="" className="form">
                    <h2>SIGN IN</h2>
                    <input type="email" name="email" className="box" placeholder="Enter Email" />
                    <input
                        type="password"
                        name="password"
                        className="box"
                        placeholder="Enter Password"
                    />
                    <input type="submit" value="SIGN IN" id="submit" />
                    <a href="#">Forgotten Password?</a>
                </form>
                <div className="side">
                    <img src={img} alt="" />
                </div>
            </div>
        </div>
    );
};

export default SignInPage;
