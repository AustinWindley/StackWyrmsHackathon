import { BrowserRouter, createBrowserRouter, Routes, Route, Navigate } from "react-router"
import Home from "./Home"
import Stocks from "./Stocks"
import Graphs from "./Graphs"
import Login from "./account/Login"
import Profile from "./account/Profile"
import Register from "./account/Register"
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/stocks" element={<Stocks />} />
        <Route path="/graphs" element={<Graphs />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/logout" element={<Navigate to="/login" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}