import { Box, Typography, Container } from "@mui/material"
import Header from "./statics/Header"

export default function Home() {
    return (
        <>
            <Header pageName="Home" />
            <Container maxWidth="md" sx={{ pt: 12, textAlign: "center" }}>
                <Typography variant="h2" gutterBottom>Hatchling</Typography>
                <Typography variant="h5" color="text.secondary" gutterBottom>
                    By FinTech
                </Typography>
                <Typography variant="body1" sx={{ mt: 2 }}>
                    Helping recent graduates and young professionals take control of their finances and investments. Track your spending, manage your stock portfolio, and visualize your financial health all in one place.
                </Typography>
                <Typography variant="body1" sx={{ mt: 2 }}>
                    Sign up today to start your financial journey with Hatchling!
                </Typography>
            </Container>
        </>
    )
}