import React, { createContext, useState } from "react";

export const ImageContext = createContext();

const ImageContextProvider = props => {
    const [image, setImage] = useState(null);

    return (
        <ImageContext.Provider value= {{ image, setImage }}>
            {props.children}
        </ImageContext.Provider>
    );
};

export default ImageContextProvider;