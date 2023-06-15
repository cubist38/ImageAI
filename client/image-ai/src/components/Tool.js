import React from "react";
import { ToolButton } from "./style.js";

const Tool = ({ text, icon, action }) => {
    return (
        <div>
            <ToolButton icon={icon} onClick={action}>{text}</ToolButton>
        </div>
    );
};

export default Tool;