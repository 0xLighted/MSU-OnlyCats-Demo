/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
        colors: {
            'proj-white': '#F6F1F1',
            'proj-blue': '#00AFF0',
            'proj-light-blue': '#bae6fd',
            'proj-orange': '#FBA834',
        },
        fontFamily: {
            'Sriracha': ['Sriracha', 'cursive'],
            'comfortaa': ['Comfortaa', 'sans-serif'],
            "great-vibes": ["Great Vibes", 'cursive']
        },
        animation: {
            'infinite-scroll': 'infinite-scroll 25s linear infinite',
        },
        keyframes: {
            'infinite-scroll': {
                from: { transform: 'translateX(0)' },
                to: { transform: 'translateX(-100%)' },
            }
        }
    },
  },
  plugins: [],
}

