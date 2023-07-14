import React, { useContext, useEffect, useState } from "react";
import { SearchResultContext } from "../context/SearchResultContext";
import Loader from "./Loader"
import Gallery from "./Gallery"
import styled from "styled-components";
import { Pagination, Grid } from '@mui/material';

const SearchResultContainer = ({ handleImageSelection, query }) => {
    const { results, storageUrls, loading, runSearch, getImages, getStorage } = useContext(SearchResultContext);
    const [page, setPage] = useState(0);
    useEffect(() => {
        console.log("Running query " + query);
        runSearch(query);
    }, [query]);

    useEffect(() => {
        getStorage();
    }, [storageUrls]);

    useEffect(() => {
        if (page < storageUrls.length) {
            console.log("Get images in page " + page);
            console.log(storageUrls);
            getImages(page);
        }
    }, [page]);

    const handleChange = (event, value) => {
        setPage(value - 1);
    };

    if (query !== null) {
        return (
                <Grid container direction="column" justifyContent="center" alignItems="center">
                    <div className="photo-container">
                            { loading ? <Loader /> : <Gallery data={results} handleImageSelection={handleImageSelection}/> }
                    </div>
                    {/* {storageUrls.map((url, index) => (
                        <button onClick={() => setPage(index)}>{index}</button>
                    ))} */}
                    <Pagination count={storageUrls.length} page={page} onChange={handleChange} />
                </Grid>
        );
    }
    else {
        return (
            <div></div>
        );
    }
};

export default SearchResultContainer;