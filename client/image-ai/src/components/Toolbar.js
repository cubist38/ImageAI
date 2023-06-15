import React from "react";
import { BsFillEraserFill } from "react-icons/bs";
import { ToolBarContainer } from "./style.js";
import Tool from "./Tool"

const Toolbar = () => {
    return (
        <ToolBarContainer>
            <Tool text={<BsFillEraserFill />}/>
            <Tool text="Inpaint"/>
        </ToolBarContainer>
    );
};

export default Toolbar;