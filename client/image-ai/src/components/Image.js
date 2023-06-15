import React from "react";

const Image = ({ url, title, key}) => {
    return (
        <li key={key}>
            <img src={url} alt={title}/>
        </li>
    );
};

export default Image;