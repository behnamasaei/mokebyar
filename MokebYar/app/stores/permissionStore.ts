import {defineStore} from 'pinia'
import type {PermissionResponse} from '~/types/Permission'
import {useUserStore} from "~/stores/userStore";

export const usePermissionStore = defineStore('permissionStore', {
    state: () => ({
        isLoading: false,
        permissions: {} as PermissionResponse
    }),

    actions: {
        async fetchUserPermissionAsync(): Promise<PermissionResponse> {
            try {
                this.isLoading = true

                const userStore = useUserStore()
                const providerName = 'U'
                const providerKey = userStore.user.id

                const res = await $fetch<PermissionResponse>(
                    '/api/auth/userPermission',
                    {
                        method: 'GET',
                        query: {
                            providerName,
                            providerKey
                        },
                        credentials: 'include'
                    }
                )

                this.permissions = res
                return res
            } finally {
                this.isLoading = false
            }
        }
    },
    persist: true
})
