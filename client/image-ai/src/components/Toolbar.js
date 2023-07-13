import React, { useContext } from "react";
import { BsFillEraserFill } from "react-icons/bs";
import { FaHighlighter } from "react-icons/fa";
import { ToolBarContainer } from "./style.js";
import Tool from "./Tool"

const Toolbar = ({ newImage, inpaint, highlight, undo, caption }) => {

    return (
        <ToolBarContainer>
            <Tool text="New image" icon={<BsFillEraserFill/>} action={newImage}/>
            <Tool text="Inpaint" icon={<BsFillEraserFill/>} action={inpaint}/>
            <Tool text="Highlight" icon={<FaHighlighter/>} action={highlight}/>
            <Tool text="Undo" action={undo}/>
            <Tool text="Caption" action={caption}/>
        </ToolBarContainer>
    );
};

export default Toolbar;