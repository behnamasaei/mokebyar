import {
    QueryClient,
    VueQueryPlugin,
    useQueryClient
} from '@tanstack/vue-query'

export default defineNuxtPlugin((nuxtApp) => {
    const queryClient = new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
                refetchOnWindowFocus: false
            },
            mutations: {
                retry: false
            }
        }
    })

    nuxtApp.vueApp.use(VueQueryPlugin, {
        queryClient
    })

    // 👇 VERY IMPORTANT for Nuxt 4
    nuxtApp.provide('queryClient', queryClient)
})
