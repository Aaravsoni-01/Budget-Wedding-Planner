/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rose-gold': '#B76E79',
        'blush': '#FFE5E5',
        'ivory': '#FFFFF0',
        'champagne': '#F7E7CE',
      },
      fontFamily: {
        'serif': ['Georgia', 'serif'],
        'elegant': ['Playfair Display', 'serif'],
      },
    },
  },
  plugins: [],
}
