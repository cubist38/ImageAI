import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import { ImageContext } from './context/ImageContext';
import ImageEditor from "./components/ImageEditor"
import ServerStatusContextProvider from "./context/ServerStatusContext";
import ImageBrowser from "./components/ImageBrowser"
import { useSelector } from "react-redux";
import AppAppBar from "./components/AppAppBar";

const MyApp = () => {
  const {imageStack, setImageStack} = useContext(ImageContext);
  return (
    <div>
      { imageStack.length === 0 && <ImageBrowser />}

      <ServerStatusContextProvider>
        { imageStack.length > 0 && <ImageEditor/> }
      </ServerStatusContextProvider>
      
    </div>
  );
}

function App() {
  const authenticated = useSelector((store) => store.authSlice.isAuthenticated);
  if (!authenticated) return <Navigate to="/auth/login" />;
  return (
      <React.Fragment>
          <AppAppBar />
          <Routes>
              {/* <Route path="issuers" element={<IssuersPage />} />
              <Route path="holders" element={<HoldersPage />} />
              <Route path="f/:id" element={<FormPage/>}/> */}
              <Route path="/" element={<MyApp />} />
          </Routes>
      </React.Fragment>
  );
}

export default App;
