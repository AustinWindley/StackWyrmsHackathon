// Profile page — the main dashboard after logging in.
// Shows budget, transactions, investments, and a form to update finances.
import Header from "../statics/Header"
import Sidebar from "../statics/Sidebar"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import {
    Box, Grid, Typography, Paper, TextField, Button,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    IconButton, Alert, CircularProgress, Container,
} from "@mui/material"
import DeleteIcon from "@mui/icons-material/Delete"
import { BarChart } from "@mui/x-charts/BarChart"

interface Transaction {
    id: number
    transaction_name: string
    transaction_date: string
    amount: number
}

interface Stock {
    stock_name: string
    stock_symbol: string
    current_price: number
    count: number
}

interface FinanceLabel {
    label: string
    value: number
}

interface FinancesFull {
    hourly_income: number
    hours_per_week: number
    rent: number
    groceries: number
    utilities: number
    transportation: number
    entertainment: number
    subscriptions: number
    other: number
}

interface DashboardData {
    username: string
    transactions: Transaction[]
    stocks: Stock[]
    finance_data: FinanceLabel[] | null
    finances_full: FinancesFull | null
}

export default function Profile() {
    const nav = useNavigate()
    const [data, setData] = useState<DashboardData | null>(null)
    const [loading, setLoading] = useState(true)
    const [pageState, setPageState] = useState("Budget")
    const [error, setError] = useState<string | null>(null)
    const [success, setSuccess] = useState<string | null>(null)

    // stuff for the "add transaction" form
    const [txName, setTxName] = useState("")
    const [txAmount, setTxAmount] = useState("")

    // keeps track of the finance fields so the form stays in sync
    const [finances, setFinances] = useState<FinancesFull>({
        hourly_income: 0, hours_per_week: 0, rent: 0, groceries: 0,
        utilities: 0, transportation: 0, entertainment: 0, subscriptions: 0, other: 0,
    })

    // grabs everything from the backend — transactions, stocks, finances, the works
    const fetchDashboard = () => {
        setLoading(true)
        fetch("/api/dashboard")
            .then(res => {
                // not logged in? bounce to login
                if (res.status === 401) {
                    nav("/login")
                    return null
                }
                return res.json()
            })
            .then(data => {
                if (data) {
                    setData(data)
                    // pre-fill the finance form so users see their current values
                    if (data.finances_full) {
                        setFinances(data.finances_full)
                    }
                }
                setLoading(false)
            })
            .catch(() => {
                setError("Failed to load dashboard data.")
                setLoading(false)
            })
    }

    // load data on first render
    useEffect(() => {
        fetchDashboard()
    }, [])

    // wipe both error and success banners
    const clearMessages = () => { setError(null); setSuccess(null) }

    // --- Add Transaction ---
    // fires the form off to the backend, then refreshes the dashboard
    const handleAddTransaction = async (e: React.FormEvent) => {
        e.preventDefault()
        clearMessages()
        if (!txName.trim() || !txAmount.trim()) {
            setError("Transaction name and amount are required.")
            return
        }
        const formData = new FormData()
        formData.append("transaction_name", txName.trim())
        formData.append("amount", txAmount.trim())
        try {
            const res = await fetch("/api/add_transaction", { method: "POST", body: formData })
            const result = await res.json()
            if (res.ok) {
                setSuccess(result.message)
                setTxName("")
                setTxAmount("")
                fetchDashboard()
            } else {
                setError(result.error || "Failed to add transaction.")
            }
        } catch {
            setError("Network error.")
        }
    }

    // --- Delete Transaction ---
    // bye bye transaction
    const handleDeleteTransaction = async (transactionId: number) => {
        clearMessages()
        const formData = new FormData()
        formData.append("transaction_id", String(transactionId))
        try {
            const res = await fetch("/api/delete_transaction", { method: "POST", body: formData })
            const result = await res.json()
            if (res.ok) {
                setSuccess(result.message)
                fetchDashboard()
            } else {
                setError(result.error || "Failed to delete transaction.")
            }
        } catch {
            setError("Network error.")
        }
    }

    // --- Update Finances ---
    // pushes the whole finance form to the backend in one go
    const handleUpdateFinances = async (e: React.FormEvent) => {
        e.preventDefault()
        clearMessages()
        const formData = new FormData()
        for (const [key, value] of Object.entries(finances)) {
            formData.append(key, String(value))
        }
        try {
            const res = await fetch("/api/update_finances", { method: "POST", body: formData })
            const result = await res.json()
            if (res.ok) {
                setSuccess(result.message)
                fetchDashboard()
            } else {
                setError(result.error || "Failed to update finances.")
            }
        } catch {
            setError("Network error.")
        }
    }

    if (loading) {
        return (
            <>
                <Header pageName="Profile" />
                <Box display="flex" justifyContent="center" alignItems="center" mt={16}>
                    <CircularProgress />
                </Box>
            </>
        )
    }

    // --- Budget Tab ---
    // weekly income calculated from hourly rate * hours
    const weeklyIncome = data?.finances_full
        ? data.finances_full.hourly_income * data.finances_full.hours_per_week
        : 0
    // monthly is roughly 4.33 weeks (52 / 12)
    const monthlyIncome = weeklyIncome * 4.33
    // total monthly expenses — just add up all the expense categories
    const totalExpenses = data?.finances_full
        ? data.finances_full.rent + data.finances_full.groceries +
          data.finances_full.utilities + data.finances_full.transportation +
          data.finances_full.entertainment + data.finances_full.subscriptions +
          data.finances_full.other
        : 0

    const budgetView = (
        <Box>
            <Typography variant="h5" gutterBottom>Budget Overview</Typography>

            {/* the bar chart — income vs expenses at a glance */}
            {data?.finances_full && (
                <Paper sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Monthly Income vs Expenses</Typography>
                    <BarChart
                        xAxis={[{ scaleType: "band", data: ["Monthly"] }]}
                        series={[
                            { data: [Math.round(monthlyIncome * 100) / 100], label: "Income", color: "#4caf50" },
                            { data: [Math.round(totalExpenses * 100) / 100], label: "Expenses", color: "#f44336" },
                        ]}
                        height={300}
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        {monthlyIncome >= totalExpenses
                            ? `Nice! You're saving about $${(monthlyIncome - totalExpenses).toFixed(2)}/mo`
                            : `Heads up — you're spending $${(totalExpenses - monthlyIncome).toFixed(2)}/mo more than you earn`}
                    </Typography>
                </Paper>
            )}

            {/* expense breakdown table */}
            {data?.finance_data && data.finance_data.length > 0 ? (
                <TableContainer component={Paper} sx={{ mb: 3 }}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell><strong>Category</strong></TableCell>
                                <TableCell align="right"><strong>Amount ($)</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.finance_data.map((row) => (
                                <TableRow key={row.label}>
                                    <TableCell>{row.label}</TableCell>
                                    <TableCell align="right">{row.value.toFixed(2)}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            ) : (
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                    No budget data yet. Head over to "Update Finances" to get started!
                </Typography>
            )}

            {/* quick income summary */}
            {data?.finances_full && (
                <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant="subtitle1">
                        <strong>Income:</strong> ${data.finances_full.hourly_income.toFixed(2)}/hr
                        &times; {data.finances_full.hours_per_week} hrs/wk
                        = <strong>${weeklyIncome.toFixed(2)}/wk</strong>
                        {" "}&asymp; <strong>${monthlyIncome.toFixed(2)}/mo</strong>
                    </Typography>
                </Paper>
            )}
        </Box>
    )

    // --- Transactions Tab ---
    // lists all transactions with the option to add new ones or nuke existing ones
    const transactionsView = (
        <Box>
            <Typography variant="h5" gutterBottom>Transactions</Typography>

            {/* quick form to add a new transaction */}
            <Paper sx={{ p: 2, mb: 3 }}>
                <Typography variant="h6" gutterBottom>Add Transaction</Typography>
                <Box component="form" onSubmit={handleAddTransaction} display="flex" gap={2} flexWrap="wrap" alignItems="center">
                    <TextField
                        label="Name"
                        value={txName}
                        onChange={(e) => setTxName(e.target.value)}
                        required
                        size="small"
                    />
                    <TextField
                        label="Amount"
                        value={txAmount}
                        onChange={(e) => setTxAmount(e.target.value)}
                        required
                        size="small"
                        type="number"
                        helperText="Negative for expenses"
                    />
                    <Button type="submit" variant="contained" size="medium">Add</Button>
                </Box>
            </Paper>

            {/* Transaction List */}
            {data?.transactions && data.transactions.length > 0 ? (
                <TableContainer component={Paper}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell><strong>Name</strong></TableCell>
                                <TableCell><strong>Date</strong></TableCell>
                                <TableCell align="right"><strong>Amount ($)</strong></TableCell>
                                <TableCell align="center"><strong>Delete</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.transactions.map((tx) => (
                                <TableRow key={tx.id}>
                                    <TableCell>{tx.transaction_name}</TableCell>
                                    <TableCell>{tx.transaction_date}</TableCell>
                                    <TableCell
                                        align="right"
                                        sx={{ color: tx.amount < 0 ? "error.main" : "success.main" }}
                                    >
                                        {tx.amount.toFixed(2)}
                                    </TableCell>
                                    <TableCell align="center">
                                        <IconButton
                                            size="small"
                                            color="error"
                                            onClick={() => handleDeleteTransaction(tx.id)}
                                        >
                                            <DeleteIcon fontSize="small" />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            ) : (
                <Typography color="text.secondary">No transactions yet.</Typography>
            )}
        </Box>
    )

    // --- Investments Tab ---
    // shows the stock portfolio — name, symbol, price, shares, total value
    const investmentsView = (
        <Box>
            <Typography variant="h5" gutterBottom>Stock Portfolio</Typography>
            {data?.stocks && data.stocks.length > 0 ? (
                <TableContainer component={Paper}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell><strong>Name</strong></TableCell>
                                <TableCell><strong>Symbol</strong></TableCell>
                                <TableCell align="right"><strong>Price ($)</strong></TableCell>
                                <TableCell align="right"><strong>Shares</strong></TableCell>
                                <TableCell align="right"><strong>Total ($)</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {data.stocks.map((s) => (
                                <TableRow key={s.stock_symbol}>
                                    <TableCell>{s.stock_name}</TableCell>
                                    <TableCell>{s.stock_symbol}</TableCell>
                                    <TableCell align="right">{s.current_price.toFixed(2)}</TableCell>
                                    <TableCell align="right">{s.count}</TableCell>
                                    <TableCell align="right">{(s.current_price * s.count).toFixed(2)}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            ) : (
                <Typography color="text.secondary">No stocks in your portfolio.</Typography>
            )}
        </Box>
    )

    // --- Update Finances Tab ---
    // friendly labels so the form doesn't look like a database dump
    const financeLabels: Record<string, string> = {
        hourly_income: "Hourly Income",
        hours_per_week: "Hours per Week",
        rent: "Rent",
        groceries: "Groceries",
        utilities: "Utilities",
        transportation: "Transportation",
        entertainment: "Entertainment",
        subscriptions: "Subscriptions",
        other: "Other",
    }

    const updateFinancesView = (
        <Box>
            <Typography variant="h5" gutterBottom>Update Finances</Typography>
            <Paper sx={{ p: 3 }}>
                <Box component="form" onSubmit={handleUpdateFinances}>
                    <Grid container spacing={2}>
                        {Object.entries(finances).map(([key, value]) => (
                            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={key}>
                                <TextField
                                    label={financeLabels[key] || key}
                                    value={value}
                                    onChange={(e) =>
                                        setFinances(prev => ({ ...prev, [key]: parseFloat(e.target.value) || 0 }))
                                    }
                                    type="number"
                                    fullWidth
                                    size="small"
                                />
                            </Grid>
                        ))}
                    </Grid>
                    <Button type="submit" variant="contained" sx={{ mt: 3 }}>
                        Save Finances
                    </Button>
                </Box>
            </Paper>
        </Box>
    )

    // picks which tab content to render based on sidebar selection
    const currentView = () => {
        switch (pageState) {
            case "Budget": return budgetView
            case "Transactions": return transactionsView
            case "Investments": return investmentsView
            case "Update Finances": return updateFinancesView
            default: return budgetView
        }
    }

    return (
        <>
            <Header pageName="Profile" />
            <Box display="flex">
                <Sidebar currentTab={pageState} onTabChange={setPageState} />
                <Box component="main" sx={{ ml: "200px", mt: 10, p: 3, width: "100%" }}>
                    {data?.username && (
                        <Typography variant="h4" gutterBottom>
                            Welcome, {data.username}
                        </Typography>
                    )}
                    {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>{error}</Alert>}
                    {success && <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>{success}</Alert>}
                    {currentView()}
                </Box>
            </Box>
        </>
    )
}
