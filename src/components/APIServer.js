import React, { useEffect, useState } from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { Alert, AlertTitle, Divider } from "@mui/material";
import CircularProgress from "@mui/material/CircularProgress";
import { Navigate, useNavigate } from "react-router-dom";
import axios from 'axios';

const APIServer = () => {

    const [serverURL, setServerURL] = useState("");

    const [submitSuccess, setSubmitSuccess] = useState(false);
    const [submitError, setSubmitError] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    const navigate = useNavigate();

    useEffect(() => {
        console.log(localStorage.getItem('server_url'))
        if (localStorage.getItem('server_url')) {
            navigate("/");
        }
    }, [])

    const handleSubmit = async (event) => {
        event.preventDefault();

        setSubmitting(true);

        axios({
            method: 'get',
            url: `${serverURL}`,
        }).then(function (response) {
            console.log(response);

            if (response.data.App == 'Magic Image Toolkit') { 
                setSubmitError(false); 
                setSubmitSuccess(true); 

                let serverUrlFormatted = serverURL.replace(/\/+$/, '');
                localStorage.setItem('server_url', serverUrlFormatted);

                navigate("/");
            }

            setSubmitting(false); 
        }).catch(function (error) {
            console.log(error);
            setSubmitting(false); 
            setSubmitSuccess(false); 
            setSubmitError(true); 
        });
    };

    return (
        <Container component="main" maxWidth="sm">
            <CssBaseline />
            <Box sx={{ marginTop: 8, marginBottom: 8, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography component="h1" variant="title">
                    Image AI
                </Typography>
                <Typography component="h1" variant="h5">
                    Please enter Server's URL
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                    <TextField 
                        value={serverURL} 
                        onChange={(event) => setServerURL(event.target.value)} 
                        margin="normal" required fullWidth id="identifier" label="Server's URL" name="identifier" />

                    {
                        submitError ? 
                        (
                            <Alert severity="error" sx={{ mt: 3 }}>
                                <AlertTitle>The server's URL is invalid!!</AlertTitle>
                            </Alert>
                        ) : (<></>)
                    }
                    {
                        submitSuccess ? 
                        (
                            <Alert severity="error" sx={{ mt: 3 }}>
                                <AlertTitle>The server's URL is valid!!</AlertTitle>
                                Welcome to our Magic Image Toolkit!!!!
                            </Alert>
                        ) : (<></>)
                    }
                    <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
                        {!submitting && "Submit"}
                        {submitting && <CircularProgress color="inherit" />}
                    </Button>
                </Box>
            </Box>
        </Container>
    );
};

export default APIServer;
