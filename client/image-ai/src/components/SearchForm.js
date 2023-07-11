import React, { useContext, useEffect } from "react";
import Input from "./Input";
import FileForm from "./FileForm";
import styled from "styled-components";
import axios from "axios";
import { SearchResultContext } from "../context/SearchResultContext";
import { apiServer, apiKey } from "../api/config";

const SearchForm = ({ setQuery }) => {
    const { runVisualSearch } = useContext(SearchResultContext);

    const [state, setState] = React.useState({
        gdriveUrl: "",
        query: "",
      });

    const onSubmitStorage = (event) => {
      event.preventDefault();
      var data = new FormData();
      data.append('access_token', 'abc');
      data.append('storage_url', state.gdriveUrl);

      var config = {
          method: 'post',
          url: `${apiServer}/import_storage`, 
          headers:{
              "Accept":"application/json, text/plain, /", 
              "Content-Type": "application/json",
              'ngrok-skip-browser-warning': true
          },
          data : data
      }
      axios(config)
          .then(function (response) {
              console.log(response.data);
          })
          .catch(function (error) {
              console.log(error);
          });        
    }      

    const onSubmitQuery = (event) => {
      event.preventDefault();
      setQuery(state.query);
    }

    const onFileFormSubmit = (imageBase64) => {
      runVisualSearch(imageBase64);
    }

    return (
        <SearchFormContainer>
          <div>
            Add Storage
            <form onSubmit={onSubmitStorage} style={{marginTop: -1 + 'em'}}>
              <Input
                label="Google Drive URL"
                type="text"
                value={state.gdriveUrl}
                onChange={(val) => setState({ ...state, gdriveUrl: val })}
              />
              <button type="submit">Import storage</button>
            </form>
          </div>
          {/* <div style={{marginTop: 10 + 'em'}}>Text Search</div> */}
          <div>
            Text Search
            <form onSubmit={onSubmitQuery} style={{marginTop: -1 + 'em'}}>
              <Input
                label="Query"
                type="text"
                value={state.query}
                onChange={(val) => setState({ ...state, query: val })}
              />
              <button type="submit">Search</button>
            </form>
          </div>
          {/* <h3> Visual search </h3> */}
          <div>
            <div style={{marginBottom: 2 + 'em'}}>Visual Search</div>
            <FileForm onSubmit={onFileFormSubmit}/>
          </div>
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
    flex-direction: row;
    align-items: baseline;
    justify-content: center;
    background-color: white;
    margin: 0 100px 20px 100px;
    gap: 30px;
`;