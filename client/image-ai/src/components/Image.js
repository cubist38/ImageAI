import React from "react";

const Image = ({ url, title, key, handleOnClick}) => {

    const imageOnClick = (event) => { 
        handleOnClick(event.target.src);
    }

    return (
        <li key={key}>
            <img src={url} alt={title} onClick={imageOnClick}/>
        </li>
    );
};

export default Image;