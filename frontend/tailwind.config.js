/** @type {import('tailwindcss').Config} */
export default {
  content: ["./indexedDB.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "asseco-blue": "#4ec2ed",
        "hack-purple": "#bc5cf2",
        "hack-lily": "#ECCBFF",
        "hack-grey": "#070F34",
      },
    },
  },
  plugins: [],
};
