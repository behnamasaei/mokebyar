import type {PermissionResponse} from '~/types/Permission'

export default defineEventHandler(async (event) => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'

    const {api} = useRuntimeConfig()

    const {providerName, providerKey} = getQuery(event) as {
        providerName?: string
        providerKey?: string
    }

    if (!providerKey) {
        throw createError({
            statusCode: 400,
            statusMessage: 'providerKey is required'
        })
    }

    const cookie = getHeader(event, 'cookie')

    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No cookie received by Nuxt'
        })
    }

    return await $fetch<PermissionResponse>(
        `${api.serverUrl}/api/permission-management/permissions`,
        {
            method: 'GET',
            query: {
                providerName: providerName ?? 'U', // U=user, R=role, T=tenant, C=client
                providerKey: providerKey
            },
            headers: {
                cookie
            }
        }
    )
})
