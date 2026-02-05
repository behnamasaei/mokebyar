import type {PagedResult} from '~/types/PagedResult'
import type {Tenant} from '~/types/Tenant'
import type {InputPagedAndSortResult} from '~/types/InputPagedAndSortResult'

export default defineEventHandler(async (event) => {
    const {api} = useRuntimeConfig()

    const cookie = getHeader(event, 'cookie')
    if (!cookie) {
        throw createError({
            statusCode: 401,
            statusMessage: 'No authentication cookie'
        })
    }

    const query = getQuery(event) as InputPagedAndSortResult

    return await $fetch<PagedResult<Tenant>>(
        `${api.serverUrl}/api/multi-tenancy/tenants`,
        {
            method: 'GET',
            headers: {
                cookie
            },
            query: {
                Filter: query.filter ?? '',
                Sorting: query.sorting ?? '',
                SkipCount: Number(query.skipCount ?? 0),
                MaxResultCount: Number(query.maxResultCount ?? 10)
            }
        }
    )
})
