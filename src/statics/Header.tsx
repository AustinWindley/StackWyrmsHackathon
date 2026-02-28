import { Grid, AppBar, Box, Typography, Button, Avatar, Toolbar, IconButton, Paper } from "@mui/material"
import Slide from "@mui/material/Slide"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import MenuIcon from "@mui/icons-material/Menu"
import { useNavigate } from "react-router"
import { useState, useRef } from "react"


export default function Header(props) {
    const pageName = props.pageName
    const [navShown, setNavShown] = useState(false)
    const [profileShown, setProfileShown] = useState(false)
    const containerRef = useRef<HTMLElement>(null)
    const nav = useNavigate()

    const handleNavMenu = () => {
        if (profileShown) {
            setProfileShown(false)
        }
        setNavShown(!navShown)
    }

    const handleProfileMenu = () => {
        if (navShown) {
            setNavShown(false)
        }
        setProfileShown(!profileShown)
    }

    const header = (
        <Paper elevation={5}>
            <AppBar  
                ref={containerRef} 
                sx={{zIndex: 2000, width:"97.5vw", bgcolor: "darkgray"}}
                position={"fixed"}>
                <Toolbar>
                    <Box display={"flex"}>
                        <IconButton onClick={handleNavMenu}>
                            <MenuIcon />
                        </IconButton>
                    </Box>
                    <Box display={"flex"}>
                        <Typography variant="h5" align="center">{pageName}</Typography>
                    </Box>
                    <Box display={"flex"}>
                        <IconButton onClick={handleProfileMenu}>
                            <Avatar />
                        </IconButton>
                    </Box>
                </Toolbar>
            </AppBar>
        </Paper>
    )

    const pages = (
        <Slide in={navShown} container={containerRef.current} timeout={300}>
            <Paper elevation={5}>
                <Box bgcolor={"lightgray"} sx={{maxHeight: "100vh", zIndex: 1500}} position={"fixed"} width={"100vw"} mt={8}>
                    <Tabs>
                        <Tab label="Stocks" onClick={() => nav("/stocks")} />
                    </Tabs>
                </Box>
            </Paper>
            
        </Slide>
    )

    const profile = (
        <Slide in={profileShown} container={containerRef.current} timeout={300}>
            <Paper elevation={5}>
                <Box bgcolor={"lightgray"} sx={{maxHeight: "100vh", zIndex: 1500}} position={"fixed"} width={"100vw"} mt={8}>
                    <Tabs>
                        <Tab label="Login" onClick={() => nav("/login")} />
                        <Tab label="Register" onClick={() => nav("/register")} />
                        <Tab label="Logout" onClick={() => nav("/logout")} />
                    </Tabs>
                </Box>
            </Paper>
        </Slide>
    )

    return (
        <Grid>
            <Grid>
                {header}
            </Grid>
            <Grid>
                {pages}
            </Grid>
            <Grid>
                {profile}
            </Grid>
        </Grid>
    )
}