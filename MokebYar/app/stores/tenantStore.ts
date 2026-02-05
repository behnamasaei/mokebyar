import {defineStore} from 'pinia'
import type {Tenant} from '~/types/Tenant'
import type {InputPagedAndSortResult} from '~/types/InputPagedAndSortResult'
import type {PagedResult} from '~/types/PagedResult'

export const useTenantStore = defineStore('tenantStore', {
    state: () => ({
        isLoading: false,
        tenants: [] as Tenant[],
        totalCount: 0
    }),

    actions: {
        async fetchAsync(
            input: InputPagedAndSortResult
        ): Promise<PagedResult<Tenant>> {
            this.isLoading = true
            try {
                const res = await $fetch<PagedResult<Tenant>>(
                    '/api/tenant/tenants',
                    {
                        method: 'GET',
                        query: input
                    }
                )

                this.tenants = res.items
                this.totalCount = res.totalCount

                return res
            } catch (error) {
                console.error('Fetch tenants failed:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        }
    },
    persist: true
})
