import { createSlice } from "@reduxjs/toolkit";

let authState = { isAuthenticated: false, accessToken: '', email: '' };
const token = localStorage.getItem("token");
const user = localStorage.getItem("user");
if (token && user) {
    authState = {
        isAuthenticated: true,
        user: JSON.parse(user),
        jwt: token
    }
}

export const authSlice = createSlice({
    name: "authSlice",
    initialState: authState,
    reducers: {
        login(state, action) {
            console.log(action)
            state.accessToken = action.payload.access_token;
            state.email = action.payload.email;
            state.isAuthenticated = true;
        },
        logout(state) {
            state.accessToken = "";
            state.email = "";
            state.isAuthenticated = false;
            localStorage.removeItem("access_token");
        }
    }
});

export const authActions = authSlice.actions;