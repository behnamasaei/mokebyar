import { parse } from 'cookie'

export default defineEventHandler(async (event) => {
    const {api} = useRuntimeConfig()

    const cookie = getHeader(event, 'cookie')
    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No authentication cookie'
        })
    }

    const {id} = event.context.params as { id: string }

    if (!id) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Tenant id is required'
        })
    }


    const csrfToken = getCookie(event, 'XSRF-TOKEN')

    if (!csrfToken) {
        throw createError({
            statusCode: 400,
            statusMessage: 'Missing CSRF token'
        })
    }
    return await $fetch(
        `${api.serverUrl}/api/multi-tenancy/tenants/${id}`,
        {
            method: 'DELETE',
            headers: {
                cookie,
                RequestVerificationToken: csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        }
    )
})
