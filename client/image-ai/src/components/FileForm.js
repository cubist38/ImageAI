import React, { useState, useContext } from "react";

import { FileUploadContainer } from "./style.js";
import { ImageContext } from "../context/ImageContext";

const FileForm = () => {

    const [file, setFile] = useState(null);
    const { image, setImage } = useContext(ImageContext);

    const handleFileInputChange = (event) => {
        let fileObj = URL.createObjectURL(event.target.files[0])
        setFile(fileObj);
    }
    
    const handleSubmit = (event) => {
        event.preventDefault();
        setImage(file);
    }

    return (
        <div>
            <FileUploadContainer>
                <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
                    <input type="file" onChange={handleFileInputChange}/>
                    <button type="submit">Upload</button>
                </form>
            </FileUploadContainer>
        </div>
    );
};

export default FileForm;