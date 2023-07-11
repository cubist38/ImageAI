import React from "react";
import Image from "./Image";
import NoImage from "./NoImage";

const Gallery = ({ data, handleImageSelection }) => {
    const results = data;
    let images;
    let noImage;

    if (results.length > 0) {
        console.log(results);
        images = results.map((url, id) => {
            return <Image url={url} key={id} handleOnClick={handleImageSelection} />;
        });

    } else {
        noImage = <NoImage />;
    }

    return (
        <div>
            <ul>{images}</ul>
            {noImage}
        </div>
    );
};

export default Gallery;