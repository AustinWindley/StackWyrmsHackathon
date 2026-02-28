import { Paper, Box, Typography, Grid } from "@mui/material"
import Header from "../statics/Header.tsx"

export default function Login() {
    // const {
    //     reg
    // }

    // const onSubmit = (data) => {
    //     const userData = JSON.parse(localStorage.get)
    //     localStorage.setItem(data.username, JSON.stringify({
            
    //     }))
    // }

    return (
        <>
            <Header pageName={"Login"}/>
            <Grid maxWidth={"45vw"} justifyContent={"center"}>
                <Paper elevation={5}>
                    <Box 
                        component={"form"} 
                        bgcolor={"lightgray"} 
                        width={"45vw"} 
                        height={"50vh"}>
                            <form method="POST">
                                <input
                                    type="username"
                                    placeholder="Username"
                                />
                                <input
                                    type="password"
                                    placeholder="Password"
                                />
                                <button type="submit">Log In</button>
                            </form>
                    </Box>
                </Paper>
            </Grid>
        </>
    )

}