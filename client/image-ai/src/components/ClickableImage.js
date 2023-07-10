import React, { useState } from "react";
import styled from "styled-components";
import { apiServer, apiKey } from "../api/config";

const ClickableImage = ({ image, onClickCallback, selectedPoints, setSelectedPoints }) => {
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
        
        onClickCallback(x, y, allCircles);

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

