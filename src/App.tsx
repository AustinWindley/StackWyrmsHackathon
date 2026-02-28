import { BrowserRouter, createBrowserRouter, Routes, Route } from "react-router"
import Home from "./Home.tsx"
import Stocks from "./Stocks.tsx"
import Graphs from "./Graphs.tsx"
import Login from "./account/Login.tsx"
import Profile from "./account/Profile.tsx"
import Register from "./account/Register.tsx"
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
        {/* TODO: Implement Error Page */}
        {/* <Route path="*" element={<ErrorPage />} /> */}
      </Routes>
    </BrowserRouter>
  )
}