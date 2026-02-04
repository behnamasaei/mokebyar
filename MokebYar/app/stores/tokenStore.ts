import {defineStore} from 'pinia'
import type {TokenResponse} from '~/types/TokenResponse'

export const useTokenStore = defineStore('tokenStore', {
    state: () => ({
        isLoading: false as boolean,
        accessToken: '' as string,
        tokenType: '' as string,
        expiresIn: 0 as number,
    }),

    actions: {
        async fetchAsync(usernameOrEmail: string, password: string): Promise<TokenResponse> {
            try {
                this.isLoading = true
                const res = await $fetch<TokenResponse>('/api/auth/token', {
                    method: 'POST',
                    body: {
                        username: usernameOrEmail,
                        password,
                    },
                })

                // persist tokens
                this.accessToken = res.access_token
                this.tokenType = res.token_type
                this.expiresIn = res.expires_in

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
