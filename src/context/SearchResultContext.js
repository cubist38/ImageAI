import React, { createContext, useState } from "react";
import axios from "axios";

export const SearchResultContext = createContext();

const SearchResultContextProvider = props => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    const [storageUrls, setStorageUrls] = useState([]);
    
    const getStorage = () => {
        let apiServer = localStorage.getItem("server_url");

        var data = new FormData();
        data.append('access_token', localStorage.getItem('access_token'));
        
        let endpoint = `${apiServer}/storage`;
    
        var config = {
            method: 'post',
            url: endpoint, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        };
    
        axios(config)
            .then(function (response) {
                setStorageUrls(response.data.urls);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    const getImages = (pageIndex) => {
        let apiServer = localStorage.getItem("server_url");

        var storage = storageUrls[pageIndex];
        var data = new FormData();
        data.append('access_token', localStorage.getItem('access_token'));
        data.append('storage_url', storage);

        var config = {
            method: 'post',
            url: `${apiServer}/images`, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        }
        axios(config)
            .then(function (response) {
                setResults(response.data.urls);
                setLoading(false);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
   
    const runSearch = (query) => {
        let apiServer = localStorage.getItem("server_url");

        var data = new FormData();
        data.append('access_token', localStorage.getItem('access_token'));
        data.append('query', query);
        data.append('page', 0);

        var config = {
            method: 'post',
            url: `${apiServer}/text_search`, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        }
        axios(config)
            .then(function (response) {
                console.log(response.data.urls);
                setResults(response.data.urls);
                setLoading(false);
            })
            .catch(function (error) {
                console.log(error);
            });        
    };

    const runVisualSearch = (imageBase64) => {
        let apiServer = localStorage.getItem("server_url");

        var data = new FormData();
        data.append('access_token', localStorage.getItem('access_token'));
        data.append('image', imageBase64);
        data.append('page', 0);

        var config = {
            method: 'post',
            url: `${apiServer}/visual_search`, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        }
        axios(config)
            .then(function (response) {
                console.log(response.data.urls);
                setResults(response.data.urls);
                setLoading(false);
            })
            .catch(function (error) {
                console.log(error);
            });        
    };

    if (results === null) {
        console.log("No results");
        // getAllImages(setResults, setLoading);
        setResults([]);
    }

    return (
        <SearchResultContext.Provider value= {{ results, storageUrls, loading, runSearch, runVisualSearch, getStorage, getImages }}>
            {props.children}
        </SearchResultContext.Provider>
    );
};

export default SearchResultContextProvider;