import React, { useContext, useState } from "react";
import SearchResultContainer from "./SearchResultContainer";
import SearchForm from "./SearchForm";
import { ImageContext } from "../context/ImageContext";

const ImageSearch = () => {
    const [query, setQuery] = useState("");
    const { image, setImage } = useContext(ImageContext);
    
    const handleImageSelection = (src) => {
        let img = new Image();
        img.onLoad = () => {
            img.width = this.width;
            img.height = this.height;
        }
        img.src = src;
        setImage(img);
    }

    return (
        <div>
            <SearchForm setQuery={setQuery} style={{ width: 50 }}/>
            <SearchResultContainer query={query} handleImageSelection={handleImageSelection}/>
        </div>
    );
};

export default ImageSearch;

