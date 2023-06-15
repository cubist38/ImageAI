import React, { useContext, useEffect } from "react";
import SearchResultContainer from "./SearchResultContainer";
import SearchForm from "./SearchForm";

const ImageSearch = () => {
    return (
        <div>
            <SearchForm style={{ width: 50 }}/>
            <SearchResultContainer />
        </div>
    );
};

export default ImageSearch;

