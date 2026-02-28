import Header from "../statics/Header.tsx"
import { useState, useEffect } from "react"
import { DataGrid } from "@mui/x-data-grid"
import Sidebar from "../statics/Sidebar.tsx"
import { Grid, Box } from "@mui/material"

export default function Profile() {
    const [data, setData] = useState([])

    const [pageState, setPageState] = useState("Budget")
    useEffect(() => {
        fetch("/api/dashboard", {
            // headers: {"Accept": "application/json"}
        }).then(
            res => res.json()
        ).then(
            data => {setData(data);
                console.log(data)
            }
        )
    }, [])

    let finance_data = data["finances_full"]
    let stocks = data["stocks"]
    let transactions = data["transactions"]
    // console.log(finance_data)
    // console.log(stocks)
    // console.log(transactions)
    // const columns: GridColDef[] = [
    //     finance_data.map((col) => (

    //     ))
    // ]
    // finance_data.map((event) => (
    //     console.log(event)
    // ))

    
    return (
        <>
            <Header pageName={"Profile"}/>
            <Grid container mt={8}>
                <Box>
                    <Sidebar />
                </Box>
            </Grid>
        </>
    )
    
}