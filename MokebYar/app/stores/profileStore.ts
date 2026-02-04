import {defineStore} from 'pinia'
import type {Profile} from "~/types/Profile";

export const useProfileStore = defineStore('profileStore', {
    state: () => ({
        isLoading: true as boolean,
        profile: {} as Profile,
    }),

    actions: {
        async fetchAsync(): Promise<Profile> {
            const tokenStore = useTokenStore()

            try {
                this.isLoading = true
                const res = await $fetch<Profile>('/api/profile/myProfile', {
                    method: 'GET',
                    credentials: 'include'
                })

                // persist tokens
                this.profile = res
                return res
            } catch (error) {
                console.error('Login failed:', error)

                throw error
            } finally {
                this.isLoading = false
            }
        },
    },
    persist: true,
})
