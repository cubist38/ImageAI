import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import { ImageContext } from './context/ImageContext';
import FileForm from "./components/FileForm";
import ImageEditor from "./components/ImageEditor"
// import _ImageEditor from "./components/ImageEditor"
import ServerStatusContextProvider from "./context/ServerStatusContext";
import ImageBrowser from "./components/ImageBrowser"

function App() {
  
  const {imageStack, setImageStack} = useContext(ImageContext);

  const back = () => {
    setImageStack([]);
  }
  return (
    <div>
      <Header back={imageStack.length > 0 ? back : null}/>
      { imageStack.length === 0 && <ImageBrowser />}

      <ServerStatusContextProvider>
        { imageStack.length > 0 && <ImageEditor/> }
      </ServerStatusContextProvider>
      
    </div>
  );
}

export default App;
