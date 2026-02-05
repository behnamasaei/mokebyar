// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
    app: {
        head: {
            title: 'Nuxt', // default fallback title
            htmlAttrs: {
                lang: 'fa-IR',
                dir: 'rtl'
            },
            link: [
                {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'},
            ],
        },
    },
    compatibilityDate: '2025-07-15',
    runtimeConfig: {
        api: {
            serverUrl: 'https://localhost:44319',
            clientId: 'MokebyarCore_App'
        }
    },
    devtools: {
        enabled: true,
    },
    css: [
        '~/assets/main.scss'
    ],
    modules: [
        '@primevue/nuxt-module',
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt',
        'pinia-plugin-persistedstate/nuxt'],
    plugins: [
        '~/plugins/vue-query.client',
        '~/plugins/pinia-persist.client.ts'
    ],
    routeRules: {
        '/dashboard/*': { appLayout: 'dashboard-layout' },
    },
    primevue: {
        options: {
            theme: {
                preset: Aura
            }
        }
    },
    devServer: {
        host: 'localhost',
        https: {
            key: './localhost+2-key.pem',
            cert: './localhost+2.pem'
        },
        port: 3000,
    },
})