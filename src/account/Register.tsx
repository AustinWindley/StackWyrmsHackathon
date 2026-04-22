import { Paper, Box, Typography, TextField, Button, Container, Alert } from "@mui/material"
import { useNavigate } from "react-router"
import { useState } from "react"
import Header from "../statics/Header"

export default function Register() {
    const nav = useNavigate()
    const [error, setError] = useState<string | null>(null)

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError(null)
        const formData = new FormData(event.currentTarget)
        try {
            const res = await fetch("/Hackathon/api/register", {
                method: "POST",
                body: formData,
            })
            const data = await res.json()
            if (res.ok) {
                nav("/Hackathon/login")
            } else {
                setError(data.error || "Registration failed.")
            }
        } catch (err) {
            setError("Network error. Please try again.")
        }
    }

    return (
        <>
            <Header pageName="Register" />
            <Container maxWidth="sm" sx={{ mt: 12 }}>
                <Paper elevation={6} sx={{ p: 4 }}>
                    <Typography variant="h4" gutterBottom align="center">Create Account</Typography>
                    {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                    <Box component="form" onSubmit={handleSubmit}>
                        <TextField
                            placeholder="Enter Username"
                            label="Username"
                            name="username"
                            type="text"
                            fullWidth
                            required
                            margin="normal"
                        />
                        <TextField
                            placeholder="Enter Email"
                            label="Email"
                            name="email"
                            type="email"
                            fullWidth
                            required
                            margin="normal"
                        />
                        <TextField
                            placeholder="Enter Password"
                            label="Password"
                            name="password"
                            type="password"
                            fullWidth
                            required
                            margin="normal"
                        />
                        <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                            Register
                        </Button>
                    </Box>
                    <Typography variant="body2" align="center" sx={{ mt: 2 }}>
                        Already have an account?{" "}
                        <Button size="small" onClick={() => nav("/Hackathon/login")}>Sign In</Button>
                    </Typography>
                </Paper>
            </Container>
        </>
    )
}
