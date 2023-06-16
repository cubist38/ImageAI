import React, { useContext, useEffect } from "react";
import { SearchResultContext } from "../context/SearchResultContext";
import Loader from "./Loader"
import Gallery from "./Gallery"
import styled from "styled-components";

const SearchResultContainer = ({ handleImageSelection, query }) => {
    const { results, loading, runSearch } = useContext(SearchResultContext);

    useEffect(() => {
        runSearch(query);
    }, [query]);

    if (query != "") {
        return (
            <div className="photo-container">
                    { loading ? <Loader /> : <Gallery data={results} handleImageSelection={handleImageSelection}/> }
            </div>
        );
    }
    else {
        return (
            <div></div>
        );
    }
};

export default SearchResultContainer;