import React, { createContext, useState } from "react";
import axios from "axios";
import { apiServer, apiKey } from "../api/config";

export const SearchResultContext = createContext();

const getAllImages = ({setResults, setLoading}) => {
    var data = new FormData();
    data.append('access_token', 'abc');
    
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
            var storage = response.data.urls[0];
            var data = new FormData();
            data.append('access_token', 'abc');
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
                    // console.log(response.data.urls);
                    setResults(response.data.urls);
                    setLoading(false);
                })
                .catch(function (error) {
                    console.log(error);
                });
        })
        .catch(function (error) {
            console.log(error);
        });
}

const SearchResultContextProvider = props => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    
    const runSearch = (query) => {
        var data = new FormData();
        data.append('access_token', 'abc');
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
        var data = new FormData();
        data.append('access_token', 'abc');
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
        getAllImages(setResults, setLoading);
    }

    return (
        <SearchResultContext.Provider value= {{ results, loading, runSearch, runVisualSearch }}>
            {props.children}
        </SearchResultContext.Provider>
    );
};

export default SearchResultContextProvider;