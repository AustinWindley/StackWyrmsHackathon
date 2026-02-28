import { Paper, Box, Typography, Grid, TextField, Button } from "@mui/material"
import { useForm } from "react-hook-form"
import { useNavigate } from "react-router"
import Header from "../statics/Header.tsx"

export default function Register() {
const nav = useNavigate()

    async function sendFormData(formData: FormData) {
        try {
            const response = await fetch("/api/register", {
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
            if (res.status === 409) {
                const errorData = await res.json()
                if (errorData.error === "Account already exists") {
                    alert("Login failed: Account already exists")
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
            <Header pageName={"Register"}/>
            <Grid maxWidth={"45vw"} justifyContent={"center"}>
                <Paper elevation={5}>
                    <Box 
                        component={"form"}
                        action={"/api/register"} 
                        onSubmit={async (event) => {
                            const success = await handleSubmit(event)
                            if (success) {
                                nav("/")
                            }
                        }}
                        bgcolor={"lightgray"} 
                        width={"45vw"} 
                        height={"50vh"}>
                            <TextField
                                placeholder="Enter Username"
                                label="Username"
                                name="username"
                                type="text"
                                fullWidth
                                required
                                margin="normal" />
                            <TextField
                                placeholder="Enter Email"
                                label="Email"
                                name="email"
                                type="email"
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
                            <Button type="submit" variant="contained" fullWidth>
                                Sign In
                            </Button>
                    </Box>
                </Paper>
            </Grid>
        </>
    )

}