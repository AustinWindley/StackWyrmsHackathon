import { BrowserRouter, createBrowserRouter, Routes, Route, Navigate, RouterProvider } from "react-router"
import Home from "./Home"
import Stocks from "./Stocks"
import Graphs from "./Graphs"
import Login from "./account/Login"
import Profile from "./account/Profile"
import Register from "./account/Register"
export default function App() {
  const router = createBrowserRouter([{
    path: '/Hackathon/',
    children: [
      {index: true, element: <Navigate to={"home"} />},
      {path: "home", element: <Home />},
      {path: "stocks", element: <Stocks />},
      {path: "graphs", element: <Graphs />},
      {path: "login", element: <Login />},
      {path: "register", element: <Register />},
      {path: "profile", element: <Profile />},
      {path: "logout", element: <Navigate to="login" replace />}
    ]
  }])
  return (
    // <BrowserRouter>
    //   <Routes>
    //     <Route path="/Hackathon/" element={<Home />} />
    //     <Route path="/Hackathon/stocks" element={<Stocks />} />
    //     <Route path="/Hackathon/graphs" element={<Graphs />} />
    //     <Route path="/Hackathon/login" element={<Login />} />
    //     <Route path="/Hackathon/register" element={<Register />} />
    //     <Route path="/Hackathon/profile" element={<Profile />} />
    //     <Route path="/Hackathon/logout" element={<Navigate to="/login" replace />} />
    //     {/* <Route path="*" element={<Navigate to="/" replace />} /> */}
    //   </Routes>
    // </BrowserRouter>
    <RouterProvider router={router} />
  )
}