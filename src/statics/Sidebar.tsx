import { Paper, Box, Tabs, Tab } from "@mui/material"

interface SidebarProps {
    currentTab: string
    onTabChange: (tab: string) => void
}

const sidebarTabs = ["Budget", "Transactions", "Investments", "Update Finances"]

export default function Sidebar({ currentTab, onTabChange }: SidebarProps) {
    const tabIndex = sidebarTabs.indexOf(currentTab)

    return (
        <Paper elevation={5} sx={{ position: "fixed", top: 64, left: 0, height: "calc(100vh - 64px)", width: 200, zIndex: 1000 }}>
            <Box bgcolor="#f5f5f5" sx={{ height: "100%" }}>
                <Tabs
                    orientation="vertical"
                    value={tabIndex >= 0 ? tabIndex : 0}
                    onChange={(_, newValue) => onTabChange(sidebarTabs[newValue])}
                    sx={{ pt: 2 }}
                >
                    {sidebarTabs.map((label) => (
                        <Tab key={label} label={label} />
                    ))}
                </Tabs>
            </Box>
        </Paper>
    )
}