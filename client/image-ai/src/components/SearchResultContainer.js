import React, { useContext, useEffect } from "react";
import { SearchResultContext } from "../context/SearchResultContext";
import Loader from "./Loader"
import Gallery from "./Gallery"
import styled from "styled-components";

const SearchResultContainer = () => {
    const { results, loading, runSearch } = useContext(SearchResultContext);

    useEffect(() => {
        runSearch("mountain");
    }, []);

    return (
        <div className="photo-container">
                { loading ? <Loader /> : <Gallery data={results} /> }
        </div>
    );
};

export default SearchResultContainer;