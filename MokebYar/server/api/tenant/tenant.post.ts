import {parse} from 'cookie'

export default defineEventHandler(async (event) => {
    const {api} = useRuntimeConfig()

    const cookie = getHeader(event, 'cookie')
    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No authentication cookie'
        })
    }

    const csrfToken = getCookie(event, 'XSRF-TOKEN')
    if (!csrfToken) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Missing CSRF token'
        })
    }

    const body = await readBody(event)

    return await $fetch(
        `${api.serverUrl}/api/multi-tenancy/tenants`,
        {
            method: 'POST',
            headers: {
                cookie,
                RequestVerificationToken: csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: body
        }
    )
})
