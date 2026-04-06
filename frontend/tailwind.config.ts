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
        background: "#EDE6DA", // refined ivory
        surface: "#F5F0E8",    // bone white
        "surface-2": "#EAE3D6", // deeper ivory for depth
        border: "#CCC5B6",      // soft parchment border
        accent: {
          DEFAULT: "#1C1917",   // deep charcoal for high-contrast accents
          hover: "#000000",
          light: "#44403C",
        },
        cyan: {
          DEFAULT: "#1C1917",
          light: "#44403C",
        },
        text: {
          primary: "#1C1917",   // deep charcoal readability
          secondary: "#44403C",
          muted: "#78716C",
        },
        star: "#F59E0B",
        success: "#65A30D",
        error: "#DC2626",
        warning: "#D97706",
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
