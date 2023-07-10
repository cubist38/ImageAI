import React, { useState, useContext } from "react";

import { FileUploadContainer } from "./style.js";
import { ImageContext } from "../context/ImageContext";

const FileForm = () => {

    const [file, setFile] = useState(null);
    const { image, setImage } = useContext(ImageContext);

    const handleFileInputChange = (event) => {
        var _URL = window.URL || window.webkitURL;
        let fileObj = _URL.createObjectURL(event.target.files[0])
        console.log(event.target.files)

        const reader = new FileReader();
        reader.onload = function () {
            var base64String = reader.result.replace("data:", "")
                .replace(/^.+,/, "");

            let img = new Image();
            img.onLoad = () => {
                img.width = this.width;
                img.height = this.height;
            }
            img.src = fileObj;
            img.base64 = base64String;
            setFile(img);
        }
        reader.readAsDataURL(event.target.files[0]);        
    }
    
    const handleSubmit = (event) => {
        event.preventDefault();
        setImage(file);
    }

    return (
        <div>
            <FileUploadContainer>
                <form onSubmit={handleSubmit}>
                    <input type="file" onChange={handleFileInputChange}/>
                    <button type="submit">Upload</button>
                </form>
            </FileUploadContainer>
        </div>
    );
};

export default FileForm;