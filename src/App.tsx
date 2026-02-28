import { BrowserRouter, createBrowserRouter, Routes, Route } from "react-router"
import Home from "./Home.tsx"
import Stocks from "./Stocks.tsx"
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/stocks" element={<Stocks />} /> 
        {/* TODO: Implement Error Page */}
        {/* <Route path="*" element={<ErrorPage />} /> */}
      </Routes>
    </BrowserRouter>
  )
}


