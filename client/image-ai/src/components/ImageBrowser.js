import React, { useContext } from "react";
import FileForm from "./FileForm";
import ImageSearch from "./ImageSearch";
import SearchResultContextProvider from "../context/SearchResultContext";
import { ImageContext } from "../context/ImageContext";
import { FileUploadContainer } from "./style.js";

const ImageBrowser = () => {
    const { imageStack, setImageStack } = useContext(ImageContext);
    const onFileFormSubmit = (imageBase64) => {
        var data = {
            displayImage: imageBase64
        }
        var tempImageStack = [...imageStack, data];
        setImageStack(tempImageStack);
    }

    return (
        <div>
            <FileUploadContainer>
                <div style={{marginBottom: 2 + 'em'}}>Upload image</div>
                <FileForm onSubmit={onFileFormSubmit}/>
            </FileUploadContainer>
            <SearchResultContextProvider>
                <ImageSearch />
            </SearchResultContextProvider>
        </div>
    );
}

export default ImageBrowser;