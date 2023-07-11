import React, { useState, useContext } from "react";

const FileForm = ({onSubmit}) => {

    const [file, setFile] = useState(null);
    
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
        onSubmit(file.base64);
    }

    return (
        <div>
            <div>
                <form onSubmit={handleSubmit}>
                    <input type="file" onChange={handleFileInputChange}/>
                    <button type="submit">Upload</button>
                </form>
            </div>
        </div>
    );
};

export default FileForm;