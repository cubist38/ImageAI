import React, { useContext, useEffect } from "react";
import Input from "./Input";
import styled from "styled-components";

const SearchForm = ({ setQuery }) => {
    const [state, setState] = React.useState({
        gdriveUrl: "",
        query: "",
      });

    const onSubmit = (event) => {
      event.preventDefault();
      setQuery(state.query);
    }

    return (
        <SearchFormContainer>
          <form onSubmit={onSubmit}>
            <Input
              label="Google Drive URL"
              type="text"
              value={state.gdriveUrl}
              onChange={(val) => setState({ ...state, gdriveUrl: val })}
            />
            <Input
              label="Query"
              type="text"
              value={state.query}
              onChange={(val) => setState({ ...state, query: val })}
            />
            <button type="submit">Search</button>
          </form>
        </SearchFormContainer>
      );
};

export default SearchForm;

const SearchFormContainer = styled.section`
    position: relative;
    border: 2px dotted lightgray;
    padding: 35px 20px;
    border-radius: 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    margin: 0 100px 20px 100px;
`;