import React, { useContext, useState } from "react";
import { ImageContext } from "../context/ImageContext";
import Toolbar from "./Toolbar";
import ClickableImage from "./ClickableImage";
import Caption from "./Caption";
import ReactLoading from "react-loading";
import { ServerStatusContext } from "../context/ServerStatusContext";
import styled from "styled-components";
import axios from "axios";
import { apiServer, apiKey } from "../api/config";
import { base64ToImage } from "../utils/utils";

const ImageEditor = () => {
    const { image, setImage, imageStack, setImageStack} = useContext(ImageContext);
    const {processing, setProcessing} = useContext(ServerStatusContext);
    
    const [selectedPoints, setSelectedPoints] = useState([]);
    const [imageCaption, setImageCaption] = useState("");

    const inpaint = () => {
        setProcessing(true);
        const endpoint = `${apiServer}/inpaint_selected_object`;

        console.log({
            'image': imageStack[imageStack.length - 1].Image,
            'mask': imageStack[imageStack.length - 1].Mask
        });

        var data = new FormData();
        data.append('image', imageStack[imageStack.length - 1].Image);
        data.append('mask', imageStack[imageStack.length - 1].Mask);

        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        };

        axios(config)
            .then(function (response) {
                console.log(response.data);
                setProcessing(false);
                setSelectedPoints([]);
                response.data.displayImage = response.data.Image;
                console.log(response.data);               

                let newImageStack = [...imageStack, response.data];
                setImageStack(newImageStack);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const highlight = () => {
        setProcessing(true);
        const endpoint = `${apiServer}/highlight_object`;

        var data = new FormData();
        data.append('image', imageStack[imageStack.length - 1].Image);
        data.append('mask', imageStack[imageStack.length - 1].Mask);
        
        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true},
            data : data
        };
        console.log(config);
        axios(config)
            .then(function (response) {
                setProcessing(false);
                setSelectedPoints([]);
                response.data.displayImage = response.data.Image;
                console.log(response.data);               

                let newImageStack = [...imageStack, response.data];

                setImageStack(newImageStack);
            })
            .catch(function (error) {
                console.log(error);
                alert("Error!!!");
            });

    }

    const undo = () => {
        var tempPoints = selectedPoints.slice(0, -1);
        setSelectedPoints(tempPoints);

        var tempImageStack = imageStack.slice(0, -1);
        setImageStack(tempImageStack);
    }

    const segment = (x, y, allCircles) => {
        // console.log(image.base64);
        console.log(x, y);

        var data = new FormData();
        data.append('image', imageStack[imageStack.length - 1].displayImage);
        data.append('x', x);
        data.append('y', y);

        // Send segment api request
        const endpoint = `${apiServer}/segment_selected_object`;
        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": true},
            data: data
        };
        console.log(config);
        axios(config)
            .then(function (response) {
                response.data.displayImage = response.data.maskedImage;
                let newImageStack = [...imageStack, response.data];
                console.log(response.data);
                
                setImageStack(newImageStack);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const caption = () => {
        console.log("Generating caption...");
        setImageCaption("Generating image description...");
        var data = new FormData();
        data.append('image', imageStack[imageStack.length - 1].displayImage);

        // Send segment api request
        const endpoint = `${apiServer}/generate_description`;
        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": true},
            data: data
        };

        axios(config)
            .then(function (response) {
                console.log(response.data);
                setImageCaption(response.data.Description);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const newImage = () => {
        setSelectedPoints([]);
        setImageStack([]);
    }

    // Always show displayImage of the last element of imageStack
    base64ToImage(imageStack[imageStack.length - 1].displayImage, (img) => {
        setImage(img);
    });

    return (
        <div >
            <div style={{margin: -5 + 'em'}}></div>
            <Toolbar
                    newImage={newImage} 
                    inpaint={inpaint}
                    highlight={highlight}
                    undo={undo}
                    caption={caption}/>
            <MyContainer>
                { processing && <ReactLoading type="bubbles" color="#0000FF" height={100} width={50}/> }
                {image && <ClickableImage image={image} onClickCallback={segment} selectedPoints={selectedPoints} setSelectedPoints={setSelectedPoints}/>}
                {(imageCaption !== "") && <Caption caption={imageCaption}/>}
            </MyContainer>
            <div style={{margin: 2 + 'em'}}></div>
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

