import React, { useContext } from "react";
import { BsFillEraserFill } from "react-icons/bs";
import { FaHighlighter } from "react-icons/fa";
import { ToolBarContainer } from "./style.js";
import Tool from "./Tool"

const Toolbar = ({ inpaint, highlight, undo }) => {

    return (
        <ToolBarContainer>
            <Tool text="Inpaint" icon={<BsFillEraserFill/>} action={inpaint}/>
            <Tool text="Highlight" icon={<FaHighlighter/>} action={highlight}/>
            <Tool text="Undo" action={undo}/>
        </ToolBarContainer>
    );
};

export default Toolbar;