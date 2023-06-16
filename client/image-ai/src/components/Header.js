import React from "react";
import { BiArrowBack } from "react-icons/bi"
const Header = ({ back }) => {
    return (
        <div>
            {back && <div className="back" onClick={back}>{<BiArrowBack />}</div>}
            <div style={{color: "transparent"}}>.</div>
            
            <h1 className="app-name">Image AI</h1>
        </div>
    )
}

export default Header;