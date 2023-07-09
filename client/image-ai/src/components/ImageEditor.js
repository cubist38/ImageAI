import React, { useContext, useState } from "react";
import { ImageContext } from "../context/ImageContext";
import Toolbar from "./Toolbar";
import ClickableImage from "./ClickableImage";
import ReactLoading from "react-loading";
import { ServerStatusContext } from "../context/ServerStatusContext";
import styled from "styled-components";
import axios from "axios";
import { apiServer, apiKey } from "../api/config";

const ImageEditor = () => {
    const {image, setImage} = useContext(ImageContext);
    const {processing, setProcessing} = useContext(ServerStatusContext);
    
    const [selectedPoints, setSelectedPoints] = useState([]);
    const inpaint = () => {
        setProcessing(true);
        console.log("Send to server image: " + image.src);
        console.log(selectedPoints);

        // Send inpaint api request
        const endpoint = `https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=${apiKey}&tags=mountain&per_page=50&format=json&nojsoncallback=1`;
        //const endpoint = `${apiServer}/`;

        var data = new FormData();
        data.append('file', image);

        var config = {
            method: 'get',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "multipart/form-data",
                'ngrok-skip-browser-warning': true},
            data : data
        };

        axios(config)
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });

        setTimeout( function() { setProcessing(false); }, 1000);
        setSelectedPoints([]);
    }

    const highlight = () => {
        setProcessing(true);
        console.log("Send to server image: " + image.src);
        console.log(selectedPoints);

        // Send highlight api request
        const endpoint = `https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=${apiKey}&tags=mountain&per_page=50&format=json&nojsoncallback=1`;
        //const endpoint = `${apiServer}/`;

        var data = new FormData();
        data.append('file', image);

        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "multipart/form-data",
                'ngrok-skip-browser-warning': true},
            data : data
        };

        axios(config)
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });

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
                    highlight={highlight}
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

