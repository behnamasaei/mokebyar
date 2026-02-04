import {defineStore} from 'pinia'
import type {TokenResponse} from '~/types/TokenResponse'
import type {Profile} from "~/types/Profile";

export const useLoginStore = defineStore('loginStore', {
    state: () => ({
        isLoading: false as boolean,
    }),

    actions: {
        async fetchAsync(usernameOrEmail: string, password: string): Promise<unknown> {
            try {
                this.isLoading = true
                const res = await $fetch<unknown>('/api/auth/login', {
                    method: 'POST',
                    body: {
                        username: usernameOrEmail,
                        password: password,
                    },
                    credentials: 'include'
                })
                return res
            } catch (error) {
                console.error('Login failed:', error)
                throw error
            } finally {
                this.isLoading = false
            }
        },
    },
})
