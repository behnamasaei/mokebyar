import {defineStore} from 'pinia'
import type {User} from "~/types/User";

export const useUserStore = defineStore('userStore', {
    state: () => ({
        isLoading: false as boolean,
        user: {} as User,
    }),

    actions: {
        async fetchCurrentUserAsync(): Promise<User> {
            try {
                this.isLoading = true
                const res = await $fetch<User>('/api/auth/currentUser', {
                    method: 'GET',
                    credentials: 'include',
                })
                this.user = res
                return res
            } catch (error) {
                console.error('Login failed:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },
    },
    persist: true
})
