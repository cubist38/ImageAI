import React from "react";
import Image from "./Image";
import NoImage from "./NoImage";

const Gallery = ({ data }) => {
    const results = data;
    let images;
    let noImage;

    if (results.length > 0) {
        images = results.map(image => {
            let farm = image.farm;
            let server = image.server;
            let id = image.id;
            let secret = image.secret;
            let title = image.title;
            let url = `https://farm${farm}.staticflickr.com/${server}/${id}_${secret}_m.jpg`;
            return <Image url={url} key={id} alt={title} />;
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