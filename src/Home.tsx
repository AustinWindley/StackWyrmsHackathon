import { Grid, Box, Typography } from "@mui/material"
import Header from "./statics/Header.tsx"
export default function Home() {
    return (
        <Box>
            <Header pageName="Home"/>
            <Grid container mt={8}>
                <Grid alignItems={"center"} justifyContent={"center"} width={"100vw"}>
                    <Typography variant="h1" align="center" mt={10}>Hatchling</Typography>
                </Grid>
                <Grid width={"100vw"}>
                    <Typography variant="body1" align="center" mt={10}>Temp body</Typography>
                </Grid>
            </Grid>

        </Box>
    )
}