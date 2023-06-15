import React, { createContext, useState } from "react";
import axios from "axios";
import { apiKey } from "../api/config"

export const SearchResultContext = createContext();

const SearchResultContextProvider = props => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    
    const runSearch = (query) => {
        axios
        .get(
            `https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=${apiKey}&tags=${query}&per_page=50&format=json&nojsoncallback=1`
        )
        .then(response => {
            setResults(response.data.photos.photo);
            setLoading(false);
        })
        .catch(error => {
            console.log(
            "Encountered an error with fetching and parsing data",
            error
            );
        });
    };

    return (
        <SearchResultContext.Provider value= {{ results, loading, runSearch }}>
            {props.children}
        </SearchResultContext.Provider>
    );
};

export default SearchResultContextProvider;