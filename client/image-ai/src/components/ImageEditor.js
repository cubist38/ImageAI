import React, { useContext } from "react";
import { ImageContext } from "../context/ImageContext";
import Toolbar from "./Toolbar";
import ClickableImage from "./ClickableImage";
import { ServerStatusContext } from "../context/ServerStatusContext";
import styled from "styled-components";

const ImageEditor = () => {
    const {image, setImage} = useContext(ImageContext);
    const {processing, setProcessing} = useContext(ServerStatusContext);
    return (
        <div>
            <Toolbar />
            <MyContainer>
                
                <ClickableImage image={image}/>
            </MyContainer>
        </div>
    );
}

export default ImageEditor;

const MyContainer = styled.container`
    position: relative;
`;

