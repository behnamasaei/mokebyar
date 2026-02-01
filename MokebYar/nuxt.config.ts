// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: {
        enabled: true,

    },
    devServer:{
        https: {
            key: './localhost+2-key.pem',
            cert: './localhost+2.pem'
        },
        port: 3000,
    }
})
