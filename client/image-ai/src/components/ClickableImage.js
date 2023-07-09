import React, { useState } from "react";
import styled from "styled-components";
import { apiServer, apiKey } from "../api/config";
import axios from "axios";

const ClickableImage = ({ image, selectedPoints, setSelectedPoints }) => {
    const getClickCoords = (event) => {
        // from: https://stackoverflow.com/a/29296049/14198287
        var e = event.target;
        var dim = e.getBoundingClientRect();
        var x = event.clientX - dim.left;
        var y = event.clientY - dim.top;
        return [x, y];
    };

    const addCircle = (event) => {
        // get click coordinates
        let [x, y] = getClickCoords(event);

        // make new svg circle element
        // more info here: https://www.w3schools.com/graphics/svg_circle.asp
        let newCircle = (
        <circle
            key={selectedPoints.length + 1}
            cx={x}
            cy={y}
            r="5"
            // stroke="black"
            // strokeWidth="1"
            fill="red"
        />
        );

        // update the array of circles; you HAVE to spread the current array
        // as 'circles' is immutible and will not accept new info
        let allCircles = [...selectedPoints, newCircle];

        var data = new FormData();
        data.append('file', image.raw);

        // Send segment api request
        //const endpoint = `${apiServer}/segment_selected_object?x=0&y=0`;
        const endpoint = `${apiServer}/`;
        var config = {
            method: 'get',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "multipart/form-data",
                "ngrok-skip-browser-warning": true},
            data : data
        };

        axios(config)
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });

        // update 'circles'
        setSelectedPoints(allCircles);
    };


    var resizedWidth = (500 / image.height) * image.width;

    return (
        <div>
            <ClickableSVG width={resizedWidth} height="500" src="https://upload.wikimedia.org/wikipedia/commons/0/09/America_Online_logo.svg" onClick={addCircle}>
                {/* This loads your circles in the circles hook */}
                <image height="500" xlinkHref={image.src} />
                {selectedPoints}
            </ClickableSVG>
        </div>
    );
};

export default ClickableImage;

const ClickableSVG = styled.svg`
    & * {
        /* Block your circles from triggering 'add circle' */
        pointer-events: none;
    }
`;

