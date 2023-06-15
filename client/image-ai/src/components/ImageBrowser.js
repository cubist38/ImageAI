import React from "react";
import FileForm from "./FileForm";
import ImageSearch from "./ImageSearch";
import SearchResultContextProvider from "../context/SearchResultContext";

const ImageBrowser = () => {
    return (
        <div>
            <FileForm />
            <h2> Or </h2>
            <SearchResultContextProvider>
                <ImageSearch />
            </SearchResultContextProvider>
        </div>
    );
}

export default ImageBrowser;