/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Poppins", "sans-serif"],
        body: ["Inter", "sans-serif"]
      },
      colors: {
        ink: "#101828",
        mist: "#eef2ff",
        sand: "#fff8ef",
        brand: "#0f766e",
        coral: "#f97316"
      },
      boxShadow: {
        card: "0 20px 60px rgba(15, 23, 42, 0.08)"
      }
    }
  },
  plugins: []
};

