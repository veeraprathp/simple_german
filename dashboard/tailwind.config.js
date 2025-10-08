/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0fe',
          200: '#d6e1fd',
          300: '#b3c9fb',
          400: '#8aa7f8',
          500: '#667eea',
          600: '#4f5cd1',
          700: '#3d46b0',
          800: '#2e3690',
          900: '#252d76',
        },
        secondary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#764ba2',
          600: '#5e3a82',
          700: '#4a2d66',
          800: '#36204a',
          900: '#2a1838',
        },
      },
    },
  },
  plugins: [],
}
