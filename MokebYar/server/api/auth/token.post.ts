export default defineEventHandler(async (event) => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'
    

    const body = await readBody(event)
    const { api } = useRuntimeConfig()

    const res = await $fetch(`${api.serverUrl}/connect/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            grant_type: 'password',
            client_id: 'MokebyarCore_App',
            username: body.username,
            password: body.password
        }),
        credentials: 'include'
    })

    return res
})
