import React from "react";
import { ToolButton } from "./style.js";

const Tool = ({ text }) => {
    return (
        <div>
            <ToolButton>{text}</ToolButton>
        </div>
    );
};

export default Tool;