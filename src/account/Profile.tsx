import Header from "../statics/Header.tsx"
import { useState, useEffect } from "react"
import { DataGrid } from "@mui/x-data-grid"
import Sidebar from "../statics/Sidebar.tsx"
import { Grid, Box } from "@mui/material"

export default function Profile() {
    const [budgetData, setBudgetData] = useState([])
    const [pageState, setPageState] = useState("Budget")
    useEffect(() => {
        fetch("/api/dashboard", {
            headers: {"Accept": "application/json"}
        }).then(
            res =>{ console.log(res); res.json()}
        ).then(
            data => {setBudgetData(data);
                console.log(data)
            }
        )
    }, [])
    
    return (
        <>
            <Header pageName={"Profile"}/>
            <Grid container>
                <Box>
                    <Sidebar />
                </Box>
                
            </Grid>
        </>
    )
    
}