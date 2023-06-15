import React, { useContext } from "react";
import { ImageContext } from "../context/ImageContext";
import { ImageDisplay } from "./style"
import Toolbar from "./Toolbar";

const ImageEditor = () => {
    const {image, setImage} = useContext(ImageContext);
    
    return (
        <div>
            <Toolbar />
            <ImageDisplay src={image}/>     
        </div>
    );
}

export default ImageEditor;