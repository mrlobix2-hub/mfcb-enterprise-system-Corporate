import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './lib/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: '#081421',
        panel: '#10253B',
        border: '#24384E',
        accent: '#B0BAC5',
        muted: '#8DA0B3',
      },
      boxShadow: {
        glow: '0 12px 30px rgba(0, 0, 0, 0.25)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

export default config;
