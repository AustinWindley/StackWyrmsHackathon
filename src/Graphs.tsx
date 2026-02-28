import { Box, Typography, Container } from "@mui/material"
import Header from "./statics/Header"

export default function Graphs() {
    return (
        <Box>
            <Header pageName="Graphs" />
            <Container maxWidth="md" sx={{ mt: 12 }}>
                <Typography variant="h4" gutterBottom>Graphs</Typography>
                <Typography variant="body1" color="text.secondary">
                    Financial charts and visualizations coming soon.
                </Typography>
            </Container>
        </Box>
    )
}