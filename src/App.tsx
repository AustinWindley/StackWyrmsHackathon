import { BrowserRouter, createBrowserRouter, Routes, Route } from "react-router"
import Home from "./Home.tsx"
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

      </Routes>
    </BrowserRouter>
  )
}


