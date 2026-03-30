import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#f2ece3",
        surface: "#ffffff",
        "surface-2": "#f5f0ea",
        border: "#e5ddd4",
        accent: {
          DEFAULT: "#a01c2c",
          hover: "#821624",
          light: "#c97a84",
        },
        cyan: {
          DEFAULT: "#b8822a",
          light: "#67e8f9",
        },
        text: {
          primary: "#1c1410",
          secondary: "#5c4f45",
          muted: "#9a8c80",
        },
        star: "#f59e0b",
        success: "#a01c2c",
        error: "#ef4444",
        warning: "#f59e0b",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-in-out",
        "slide-up": "slideUp 0.3s ease-out",
        "pulse-slow": "pulse 3s ease-in-out infinite",
        "star-pop": "starPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        starPop: {
          "0%": { transform: "scale(0)" },
          "60%": { transform: "scale(1.3)" },
          "100%": { transform: "scale(1)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
