// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
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
    modules: ['@primevue/nuxt-module', '@nuxtjs/tailwindcss'],
    plugins: [
        '~/plugins/vue-query.client'
    ],
    primevue: {
        options: {
            theme: {
                preset: Aura
            }
        }
    },
    devServer: {
        https: {
            key: './localhost+2-key.pem',
            cert: './localhost+2.pem'
        },
        port: 3000,
    }
})