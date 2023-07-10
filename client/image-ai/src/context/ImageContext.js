import React, { createContext, useState } from "react";

export const ImageContext = createContext();

const ImageContextProvider = props => {
    const [image, setImage] = useState(null);
    const [imageStack, setImageStack] = useState([]);

    return (
        <ImageContext.Provider value= {{ image, setImage, imageStack, setImageStack }}>
            {props.children}
        </ImageContext.Provider>
    );
};

export default ImageContextProvider;