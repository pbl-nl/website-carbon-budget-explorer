/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {}
	},
	plugins: [require('@tailwindcss/forms'), require('daisyui'), require('@tailwindcss/typography')],
	daisyui: {
		themes: [
			{
				mytheme: {
					primary: '#1e3a8a',
					secondary: '#7b92b2',
					accent: '#67cba0',
					neutral: '#181a2a',
					'base-100': '#ffffff',
					info: '#3abff8',
					success: '#36d399',
					warning: '#fbbd23',
					error: '#f87272',
					'--rounded-box': '0.5rem'
				}
			}
		]
	}
};
