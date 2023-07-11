import React, { useContext, useState } from "react";
import SearchResultContainer from "./SearchResultContainer";
import SearchForm from "./SearchForm";
import { ImageContext } from "../context/ImageContext";

function toDataUrl(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        var reader = new FileReader();
        reader.onloadend = function() {
            callback(reader.result);
        }
        reader.readAsDataURL(xhr.response);
    };
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.send();
}



const ImageSearch = () => {
    const [query, setQuery] = useState("");
    const { image, setImage, imageStack, setImageStack } = useContext(ImageContext);
    
    const handleImageSelection = (src) => {
        // let img = new Image();
        // img.onLoad = () => {
        //     img.width = this.width;
        //     img.height = this.height;
        // }
        // img.src = src;
        toDataUrl(src, function(myBase64) {
            let base64String = myBase64.replace("data:", "").replace(/^.+,/, "");

            var data = {
                displayImage: base64String
            }
            var tempImageStack = [...imageStack, data];
            setImageStack(tempImageStack);
        });
    }

    return (
        <div>
            <SearchForm setQuery={setQuery} style={{ width: 50 }}/>
            <SearchResultContainer query={query} handleImageSelection={handleImageSelection}/>
        </div>
    );
};

export default ImageSearch;

