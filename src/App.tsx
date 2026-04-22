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
        <Route path="/Hackathon/" element={<Home />} />
        <Route path="/Hackathon/stocks" element={<Stocks />} />
        <Route path="/Hackathon/graphs" element={<Graphs />} />
        <Route path="/Hackathon/login" element={<Login />} />
        <Route path="/Hackathon/register" element={<Register />} />
        <Route path="/Hackathon/profile" element={<Profile />} />
        <Route path="/Hackathon/logout" element={<Navigate to="/login" replace />} />
        {/* <Route path="*" element={<Navigate to="/" replace />} /> */}
      </Routes>
    </BrowserRouter>
  )
}