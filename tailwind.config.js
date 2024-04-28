import defaultTheme from 'tailwindcss/defaultTheme';
import typographyPlugin from '@tailwindcss/typography';


module.exports = {
    darkMode: ["class"],
    content: [
        './playbase/templates/**/*.html',
        './playbase/**/*.py',
        './components/**/*.py',
        './components/**/*.html'
    ],
    theme: {
        extend: {
            colors: {
                primary: 'var(--aw-color-primary)',
                secondary: 'var(--aw-color-secondary)',
                accent: 'var(--aw-color-accent)',
                default: 'var(--aw-color-text-default)',
                muted: 'var(--aw-color-text-muted)',
            },
            fontFamily: {
                sans: ['var(--aw-font-sans, ui-sans-serif)', ...defaultTheme.fontFamily.sans],
                serif: ['var(--aw-font-serif, ui-serif)', ...defaultTheme.fontFamily.serif],
                heading: ['var(--aw-font-heading, ui-sans-serif)', ...defaultTheme.fontFamily.sans],
            },
        },
    },
    plugins: [
        require("tailwindcss-animate"),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
}
