import { Box, Typography, Container } from "@mui/material"
import Header from "./statics/Header"

export default function Stocks() {
    return (
        <Box>
            <Header pageName="Stocks" />
            <Container maxWidth="md" sx={{ mt: 12 }}>
                <Typography variant="h4" gutterBottom>Stock Page</Typography>
                <Typography variant="body1" color="text.secondary">
                    Stock browsing and lookup coming soon.
                </Typography>
            </Container>
        </Box>
    )
}