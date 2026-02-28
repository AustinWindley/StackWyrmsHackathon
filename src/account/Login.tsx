import { Paper, Box, Typography, TextField, Button, Container, Alert } from "@mui/material"
import { useNavigate } from "react-router"
import { useState } from "react"
import Header from "../statics/Header"

export default function Login() {
    const nav = useNavigate()
    const [error, setError] = useState<string | null>(null)

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        setError(null)
        const formData = new FormData(event.currentTarget)
        try {
            const res = await fetch("/api/login", {
                method: "POST",
                body: formData,
            })
            const data = await res.json()
            if (res.ok) {
                nav("/profile")
            } else {
                setError(data.error || "Login failed.")
            }
        } catch (err) {
            setError("Network error. Please try again.")
        }
    }

    return (
        <>
            <Header pageName="Login" />
            <Container maxWidth="sm" sx={{ mt: 12 }}>
                <Paper elevation={6} sx={{ p: 4 }}>
                    <Typography variant="h4" gutterBottom align="center">Sign In</Typography>
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
                            placeholder="Enter Password"
                            label="Password"
                            name="password"
                            type="password"
                            fullWidth
                            required
                            margin="normal"
                        />
                        <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
                            Sign In
                        </Button>
                    </Box>
                    <Typography variant="body2" align="center" sx={{ mt: 2 }}>
                        Don't have an account?{" "}
                        <Button size="small" onClick={() => nav("/register")}>Register</Button>
                    </Typography>
                </Paper>
            </Container>
        </>
    )
}
