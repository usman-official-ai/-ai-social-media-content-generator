/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#12172B", // deep ink-navy background
          light: "#1B2140",
          soft: "#232A4D",
        },
        paper: "#EDEAE2", // warm paper for text/cards on dark bg
        amber: {
          DEFAULT: "#F0A83B", // signal accent
          dim: "#C98A2C",
        },
        teal: "#4FD1C5", // secondary accent
        rule: "#33395C", // hairline rule color on dark bg
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
      backgroundImage: {
        grain: "radial-gradient(circle at 1px 1px, rgba(237,234,226,0.06) 1px, transparent 0)",
      },
    },
  },
  plugins: [],
}

