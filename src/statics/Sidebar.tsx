import { Grid, Paper, Box, Tabs, Tab } from "@mui/material"
import { useNavigate } from "react-router"
import { useState } from "react"

export default function Sidebar() {
    const nav = useNavigate()

    const sidebar = (
        <Paper elevation={5}>
            <Box 
                mt={8}
                bgcolor={"lightgray"} 
                sx={{height: "100vh", zIndex: 1500}} 
                position={"fixed"} maxWidth={"30vw"} 
                display={"flex"}
                justifyContent={"start"}
                flexDirection={"column"}>
                <Tabs centered orientation="vertical">
                    <Tab label="Budget" />
                    <Tab label="Investments" />
                    <Tab label="Loan Calculator" />
                    <Tab label="Score Estimate" />
                </Tabs>
            </Box>
        </Paper>
    )

    return (
        <Grid>
            {sidebar}
        </Grid>
    )
}