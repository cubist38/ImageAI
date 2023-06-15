import React, { useContext, useState } from "react";
import { ImageContext } from "../context/ImageContext";
import Toolbar from "./Toolbar";
import ClickableImage from "./ClickableImage";
import ReactLoading from "react-loading";
import { ServerStatusContext } from "../context/ServerStatusContext";
import styled from "styled-components";


const ImageEditor = () => {
    const {image, setImage} = useContext(ImageContext);
    const {processing, setProcessing} = useContext(ServerStatusContext);
    
    const [selectedPoints, setSelectedPoints] = useState([]);
    const inpaint = () => {
        setProcessing(true);
        console.log("Send to server image: " + image.src);
        console.log(selectedPoints);
        setTimeout( function() { setProcessing(false); }, 1000);
        setSelectedPoints([]);
    }

    const undo = () => {
        var tempPoints = selectedPoints.slice(0, -1);
        setSelectedPoints(tempPoints);
    }

    return (
        <div>
            <Toolbar inpaint={inpaint}
                    undo={undo}/>
            <MyContainer>
                { processing && <ReactLoading type="bubbles" color="#0000FF" height={100} width={50}/> }
                <ClickableImage image={image} selectedPoints={selectedPoints} setSelectedPoints={setSelectedPoints}/>
            </MyContainer>
        </div>
    );
}

export default ImageEditor;

const MyContainer = styled.section`
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: column;
  gap: 0;
`;

