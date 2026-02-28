import { StrictMode } from "react"
import App from "./App"
import { createRoot } from "react-dom/client"
import * as serviceWorkerRegistration from "./serviceWorkerRegistration"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
)

// Register the service worker for offline support in production builds.
// Change to serviceWorkerRegistration.unregister() to disable.
serviceWorkerRegistration.register()
