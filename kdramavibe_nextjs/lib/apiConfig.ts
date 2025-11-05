import axios from "axios";

// Create an Axios instance with base URL from environment variable
const api = axios.create({
  baseURL: process.env.BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // optional: 10 seconds timeout
});

export default api;
