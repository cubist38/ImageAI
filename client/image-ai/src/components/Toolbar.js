import React, { useState } from "react";
import { BsFillEraserFill } from "react-icons/bs";
import { FaHighlighter } from "react-icons/fa";
import { ToolBarContainer } from "./style.js";
import Tool from "./Tool"

const Toolbar = () => {

    const InpaintOnClicked = (event) => {
    }

    return (
        <ToolBarContainer>
            <Tool text="Inpaint" icon={<BsFillEraserFill/>} action={InpaintOnClicked}/>
            <Tool text="Highlight" icon={<FaHighlighter/>}/>
        </ToolBarContainer>
    );
};

export default Toolbar;