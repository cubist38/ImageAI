import React, { useState, useEffect } from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import MenuItem from "@mui/material/MenuItem";
import CircularProgress from "@mui/material/CircularProgress";
import { Alert, AlertTitle } from "@mui/material";
import useFetch from "../../hooks/useFetch";
import axios from "axios";
import { Navigate, useNavigate } from "react-router-dom";

const Register = () => {
    const DEFAULT_ACCOUNT_TYPE = "indi";

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordConfirm, setPasswordConfirm] = useState("");

    const [emailValidate, setEmailValidate] = useState({ error: false, helperText: "" });
    const [passwordValidate, setPasswordValidate] = useState({ error: false, helperText: "" });
    const [passwordConfirmValidate, setPasswordConfirmValidate] = useState({ error: false, helperText: "" });

    const [registerSuccess, setRegisterSuccess] = useState(false);
    const [registering, setRegistering] = useState(false);
    const [errorMessage, setErrorMessage] = useState(''); 
    const navigate = useNavigate();

    useEffect(() => { 
        if (!localStorage.getItem('server_url'))  { 
            navigate("/server-url");
        } 
        console.log(localStorage.getItem('access_token'))
        if (localStorage.getItem('access_token'))  { 
            navigate("/");
        }
    }, [])

    const validateEmail = (email) => {
        if (!email || email.trim().length === 0) {
            setEmailValidate({
                error: true,
                helperText: "Email Address is required!",
            });
            return false;
        }

        if (!/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(email)) {
            setEmailValidate({
                error: true,
                helperText: "Invalid email address!",
            });
            return false;
        }

        setEmailValidate({
            error: false,
            helperText: "",
        });

        return true;
    };

    const validatePassword = (password) => {
        if (!password || password.trim().length === 0) {
            setPasswordValidate({
                error: true,
                helperText: "Password is required!",
            });
            return false;
        }
        // if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/.test(password)) {
        //     setPasswordValidate({
        //         error: true,
        //         helperText: "Password must contain at least one  number and one uppercase and lowercase letter, and at least 8 or more characters!",
        //     });
        //     return false;
        // }
        setPasswordValidate({
            error: false,
            helperText: "",
        });
        return true;
    };

    const validatePasswordConfirm = (input) => {
        if (!input || input.trim().length === 0 || input.trim() !== password.trim()) {
            setPasswordConfirmValidate({
                error: true,
                helperText: "Password not match!",
            });
            return false;
        }
        setPasswordConfirmValidate({
            error: false,
            helperText: "",
        });
        return true;
    };

    const handleSubmit = async (event) => {
        let apiServer = localStorage.getItem("server_url");

        event.preventDefault();

        const validEmail = validateEmail(email);
        const validPassword = validatePassword(password) && validatePasswordConfirm(passwordConfirm);

        if (!(validEmail && validPassword)) return;

        // Send API request
        // const registerResponse = await register(`${apiServer.BASE_API_URL}/api/auth/local/register`, {
        //     method: "POST",
        //     body: JSON.stringify(requestBody),
        //     headers: {
        //         "Content-Type": "application/json",
        //     },
        // });

        // if (registerResponse) setRegisterSuccess(true);

        var data = new FormData();
        data.append('email', email);
        data.append('password', password);

        var config = {
            method: 'post',
            url: `${apiServer}/sign_up`, 
            headers:{
                "Accept":"application/json, text/plain, /", 
                "Content-Type": "application/json",
                'ngrok-skip-browser-warning': true
            },
            data : data
        };

        setRegistering(true);

        axios(config)
            .then(function (response) {
                console.log(response.data);

                setRegistering(false); 
                setErrorMessage(''); 
                setRegisterSuccess(true); 
            })
            .catch(function (error) {
                console.log(error);

                setRegistering(false); 
                setRegisterSuccess(false); 
                setErrorMessage(error.response.data.message);
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
                    Create a new account
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField value={email} onChange={(event) => setEmail(event.target.value)} onBlur={(event) => validateEmail(event.target.value)} onKeyUp={(event) => validateEmail(event.target.value)} error={emailValidate.error} helperText={emailValidate.helperText} required fullWidth id="email" label="Email Address" name="email" autoComplete="email" />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField value={password} onChange={(event) => setPassword(event.target.value)} onBlur={(event) => validatePassword(event.target.value)} onKeyUp={(event) => validatePassword(event.target.value)} error={passwordValidate.error} helperText={passwordValidate.helperText} required fullWidth name="password" label="Password" type="password" id="password" autoComplete="new-password" />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField value={passwordConfirm} onChange={(event) => setPasswordConfirm(event.target.value)} onBlur={(event) => validatePasswordConfirm(event.target.value)} onKeyUp={(event) => validatePasswordConfirm(event.target.value)} error={passwordConfirmValidate.error} helperText={passwordConfirmValidate.helperText} required fullWidth name="passwordConfirm" label="Confirm Password" type="password" id="passwordConfirm" />
                        </Grid>
                    </Grid>
                    {errorMessage != '' && (
                        <Alert severity="error" sx={{ mt: 3 }}>
                            <AlertTitle>Register Failed!</AlertTitle>
                            {errorMessage}
                        </Alert>
                    )}
                    {errorMessage == '' && registerSuccess && (
                        <Alert severity="success" sx={{ mt: 3 }}>
                            <AlertTitle>Registered Successfully!</AlertTitle>
                            Your account has been successfully created —{" "}
                            <strong>
                                <a href="/auth/login">Login now!</a>
                            </strong>
                        </Alert>
                    )}
                    <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2, padding: 1.5 }}>
                        {!registering && "Sign up"}
                        {registering && <CircularProgress color="inherit" />}
                    </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href="/auth/login" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
    );
};

export default Register;
