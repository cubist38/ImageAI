import { React, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { authActions } from "../redux/slices/authSlice";
import { useNavigate } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Link from '@mui/material/Link';

const rightLink = {
    fontSize: 16,
    color: 'common.white',
    ml: 3,
  };

const DEFAULT_PAGES = [{
        title: "Issuers",
        href: "/issuers",
    }, {
        title: "Holders",
        href: "/holders"
    }, {
        title: "Verifiers",
        href: "/verifiers"
    }
];

function AppAppBar({ pages = DEFAULT_PAGES, settings = [] }) {
    document.body.style.paddingTop = "64px";

    const authenticatedUser = useSelector(store => store.authSlice.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [anchorElNav, setAnchorElNav] = useState(null);
    const [anchorElUser, setAnchorElUser] = useState(null);

    const handleOpenNavMenu = (event) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    const handleLogout = () => {
        dispatch(authActions.logout());
        navigate("/");
    };

    const hasPages = pages.length > 0;

    return (
        <div>
            <AppBar position="fixed">
                <Toolbar sx={{ justifyContent: 'space-between' }}>
                <Box sx={{ flex: 1 }} />
                <Link
                    variant="h6"
                    underline="none"
                    color="inherit"
                    href="/"
                    sx={{ fontSize: 24 }}
                >
                    {'Image AI'}
                </Link>
                <Box sx={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
                    <Link
                        color="inherit"
                        variant="h6"
                        underline="none"
                        href="/premium-themes/onepirate/sign-in/"
                        sx={rightLink}
                        >
                        {'Log out'}
                    </Link>
                    
                </Box>
                </Toolbar>
            </AppBar>
            <Toolbar />
            </div>
    );
}
export default AppAppBar;
