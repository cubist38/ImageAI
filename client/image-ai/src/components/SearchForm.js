import React, { useContext, useEffect } from "react";
import Input from "./Input";
import styled from "styled-components";

const SearchForm = () => {
    const [state, setState] = React.useState({
        email: "",
        password: "",
        username: "",
        birthday: ""
      });

    return (
        <SearchFormContainer>
          <Input
            label="Google Drive URL"
            type="text"
            value={state.email}
            onChange={(val) => setState({ ...state, email: val })}
          />
          <Input
            label="Query"
            type="text"
            value={state.username}
            onChange={(val) => setState({ ...state, username: val })}
          />
          <button>Search</button>
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