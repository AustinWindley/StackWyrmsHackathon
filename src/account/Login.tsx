/* Based on tutorial from https://www.geeksforgeeks.org/reactjs/react-hook-form-create-basic-reactjs-registration-and-login-form/ */

import { Paper, Box, Typography, Grid, TextField, Button, Container } from "@mui/material"
import { useForm } from "react-hook-form"
import { useNavigate } from "react-router"
import Header from "../statics/Header.tsx"


export default function Login() {
    const nav = useNavigate()

    async function sendFormData(formData: FormData) {
        try {
            const response = await fetch("/api/login", {
                method: "POST",
                body: formData
            })
            try {
                const data = await response.clone().json()
                console.log(data)
            } catch (e) {
                console.warn("Failed to parse JSON response", e)
            }
            return response
        } catch (error) {
            return new Response(null, { status: 500, statusText: "Network error" })
            }
    }

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()

        const formData = new FormData(event.currentTarget)

        try {
            const res = await sendFormData(formData)
            if (res.status === 401) {
                const errorData = await res.json()
                if (errorData.error === "Invalid username or password") {
                    alert("Login failed: Invalid username or password")
                    return false
                }  
            }
            return res.ok
        } catch (error) {
            console.error("Error during login: ", error)
            return false
        }
    }
    return (
        <>
            <Header pageName={"Login"}/>
            <Grid container mt={8}>
                <Container>
                    <Paper elevation={10} sx={{padding: 3, marginTop: 8}}>
                        <Box 
                            component={"form"}
                            action={"/api/login"} 
                            onSubmit={async (event) => {
                                const success = await handleSubmit(event)
                                if (success) {
                                    nav("/profile")
                                }
                            }} 
                            //width={"vw"} 
                            height={"50vh"}
                            >
                                <TextField
                                    placeholder="Enter Username"
                                    label="Username"
                                    name="username"
                                    type="text"
                                    fullWidth
                                    required
                                    margin="normal" />
                                <TextField
                                    placeholder="Enter Password"
                                    label="Password"
                                    name="password"
                                    type="password"
                                    fullWidth
                                    required
                                    margin="normal" />
                                <Button type="submit" variant="contained" fullWidth sx={{marginTop:5}}>
                                    Sign In
                                </Button>
                        </Box>
                    </Paper>
                </Container>
                
            </Grid>
        </>
    )

}