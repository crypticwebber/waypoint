/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#12181B",
          soft: "#1B2327",
          softer: "#232D32",
        },
        paper: {
          DEFAULT: "#F1F2EE",
          dim: "#E6E8E1",
        },
        amber: {
          DEFAULT: "#E8A33D",
          dim: "#C98A2E",
          bright: "#F2B863",
        },
        teal: {
          DEFAULT: "#2E7D6B",
          dim: "#25655A",
          bright: "#3C9E88",
        },
        coral: {
          DEFAULT: "#D9695A",
          dim: "#B85448",
        },
        mist: "#8A9290",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
    },
  },
  plugins: [],
};
