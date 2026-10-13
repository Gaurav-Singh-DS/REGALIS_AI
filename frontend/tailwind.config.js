/** @type {import("tailwindcss").Config} */
  export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          banking: {
            canvas: '#f6f9fc',
            ink: '#0d253d',
            mute: '#64748d',
            border: '#e3e8ee',
            primary: '#2457A7',
          },
          anomaly: {
            red: '#f43f5e',
            glow: 'rgba(244, 63, 94, 0.1)',
          },
          healthy: {
            green: '#10b981',
            glow: 'rgba(16, 185, 129, 0.1)',
          },
        },
      },
    },
    plugins: [],
  }
