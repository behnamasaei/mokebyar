import type {Profile} from "~/types/Profile";

export default defineEventHandler(async (event) => {
    const {api} = useRuntimeConfig()

    const cookie = getHeader(event, 'cookie')

    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No cookie received by Nuxt'
        })
    }

    return await $fetch<Profile>(`${api.serverUrl}/api/account/my-profile`, {
        method: 'GET',
        headers: {
            cookie
        }
    })
})
