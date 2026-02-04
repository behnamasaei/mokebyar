import type {User} from "~/types/User";

export default defineEventHandler(async (event) => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'

    const {api} = useRuntimeConfig()

    const cookie = getHeader(event, 'cookie')

    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No cookie received by Nuxt'
        })
    }

    return await $fetch<User>(`${api.serverUrl}/api/app/identity/current-user`, {
        method: 'GET',
        headers: {
            cookie
        }
    })
})
