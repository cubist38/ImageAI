import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import { ImageContext } from './context/ImageContext';
import FileForm from "./components/FileForm";
import ImageEditor from "./components/ImageEditor"

function App() {
  
  const {image, setImage} = useContext(ImageContext);

  return (
    <div>
      <Header />
      { !image && <FileForm />}
      { image && <ImageEditor/> }
    </div>
  );
}

export default App;
