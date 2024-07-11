/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-to-r-from-orange-to-pink': 'linear-gradient(to right, #f97316, #ec4899, #db2777)',
      }
    },
  },
  plugins: [],
}

