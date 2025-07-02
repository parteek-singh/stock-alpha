import { useEffect, useState } from 'react'
import App from '../../App'
import './BackendStatusLoader.css'

export default function BackendStatusLoader() {
  const [ready, setReady] = useState(false)
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch(import.meta.env.VITE_API_URL + "/ping")
        if (res.ok) setReady(true)
        else throw new Error("Backend not ready")
      } catch (err) {
        console.log("Backend not ready, retrying..."+ err)
        setTimeout(() => {
          setRetryCount((c) => c + 1)
        }, 2000) // retry after 2 seconds
      }
    }

    if (!ready) checkBackend()
  }, [retryCount])

  if (!ready) {
    return (
      <div className="loading-screen">
        <h2>🚀 Starting backend, please wait...</h2>
        <p>Retry attempt: {retryCount}</p>
      </div>
    )
  }

  return (
    <div>
      <App />
    </div>
  )
}
