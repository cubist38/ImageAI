import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import { ImageContext } from './context/ImageContext';
import FileForm from "./components/FileForm";
import ImageEditor from "./components/ImageEditor"
import ServerStatusContextProvider from "./context/ServerStatusContext";
import ImageBrowser from "./components/ImageBrowser"

function App() {
  
  const {image, setImage} = useContext(ImageContext);

  return (
    <div>
      <Header />
      { !image && <ImageBrowser />}

      <ServerStatusContextProvider>
        { image && <ImageEditor/> }
      </ServerStatusContextProvider>
      
    </div>
  );
}

export default App;
