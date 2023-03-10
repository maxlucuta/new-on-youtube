import logo from "../assets/logoColour.png";

const UnsupportedDevice = () => {
    return (
        <div style = {{ width: "80%", margin: "auto", padding: "40px 10px" }}>
            <div style = {{ width: "50%", margin: "auto" }}>
                <img width = "100%" src = {logo} />
            </div>
            <div style = {{ textAlign: "center", marginTop: "20px", fontSize: "50px" }} >
                Oops ...
            </div>
            <div style = {{ textAlign: "center", marginTop: "20px", color: "grey" }} >
                New On Youtube currently does not support mobile devices. 
                Please try using your desktop browser!
            </div>
        </div>
    )
}

export default UnsupportedDevice

