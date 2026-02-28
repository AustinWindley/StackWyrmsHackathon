import { AppBar, Box, Typography, Avatar, Toolbar, IconButton, Paper, Tabs, Tab } from "@mui/material"
import Slide from "@mui/material/Slide"
import MenuIcon from "@mui/icons-material/Menu"
import { useNavigate } from "react-router"
import { useState, useRef, useEffect } from "react"

interface HeaderProps {
    pageName?: string
}

export default function Header({ pageName = "Hatchling" }: HeaderProps) {
    const [navShown, setNavShown] = useState(false)
    const [profileShown, setProfileShown] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const containerRef = useRef<HTMLElement>(null)
    const nav = useNavigate()

    useEffect(() => {
        fetch("/api/dashboard")
            .then(res => {
                setIsLoggedIn(res.ok)
            })
            .catch(() => setIsLoggedIn(false))
    }, [])

    const handleNavMenu = () => {
        if (profileShown) setProfileShown(false)
        setNavShown(!navShown)
    }

    const handleProfileMenu = () => {
        if (navShown) setNavShown(false)
        setProfileShown(!profileShown)
    }

    const handleLogout = async () => {
        await fetch("/api/logout")
        setIsLoggedIn(false)
        nav("/login")
    }

    const header = (
        <AppBar
            ref={containerRef}
            sx={{ zIndex: 2000, bgcolor: "#2e3b4e" }}
            position="fixed">
            <Toolbar sx={{ justifyContent: "space-between" }}>
                <Box display="flex" alignItems="center">
                    <IconButton onClick={handleNavMenu} sx={{ color: "white" }}>
                        <MenuIcon />
                    </IconButton>
                    <Typography
                        variant="h6"
                        sx={{ ml: 1, cursor: "pointer" }}
                        onClick={() => nav("/")}
                    >
                        Hatchling
                    </Typography>
                </Box>
                <Typography variant="h6">{pageName}</Typography>
                <Box display="flex" alignItems="center">
                    <IconButton onClick={handleProfileMenu}>
                        <Avatar sx={{ bgcolor: isLoggedIn ? "#4caf50" : "grey" }} />
                    </IconButton>
                </Box>
            </Toolbar>
        </AppBar>
    )

    const pages = (
        <Slide in={navShown} container={containerRef.current} timeout={300}>
            <Paper elevation={5}>
                <Box bgcolor="#f5f5f5" sx={{ zIndex: 1500 }} position="fixed" width="100vw" mt={8}>
                    <Tabs>
                        <Tab label="Home" onClick={() => { setNavShown(false); nav("/") }} />
                        <Tab label="Stocks" onClick={() => { setNavShown(false); nav("/stocks") }} />
                        <Tab label="Graphs" onClick={() => { setNavShown(false); nav("/graphs") }} />
                        {isLoggedIn && <Tab label="Profile" onClick={() => { setNavShown(false); nav("/profile") }} />}
                    </Tabs>
                </Box>
            </Paper>
        </Slide>
    )

    const profile = (
        <Slide in={profileShown} container={containerRef.current} timeout={300}>
            <Paper elevation={5}>
                <Box bgcolor="#f5f5f5" sx={{ zIndex: 1500 }} position="fixed" width="100vw" mt={8}>
                    <Tabs>
                        {!isLoggedIn && <Tab label="Login" onClick={() => { setProfileShown(false); nav("/login") }} />}
                        {!isLoggedIn && <Tab label="Register" onClick={() => { setProfileShown(false); nav("/register") }} />}
                        {isLoggedIn && <Tab label="Profile" onClick={() => { setProfileShown(false); nav("/profile") }} />}
                        {isLoggedIn && <Tab label="Logout" onClick={() => { setProfileShown(false); handleLogout() }} />}
                    </Tabs>
                </Box>
            </Paper>
        </Slide>
    )

    return (
        <Box>
            {header}
            {pages}
            {profile}
        </Box>
    )
}