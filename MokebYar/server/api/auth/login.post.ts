export default defineEventHandler(async (event) => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'

    const body = await readBody(event)
    const { api } = useRuntimeConfig()

    const res = await $fetch.raw(`${api.serverUrl}/api/account/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            userNameOrEmailAddress: body.username,
            password: body.password,
            rememberMe: true,
        },
        credentials: 'include'
    })

    const setCookie = res.headers.get('set-cookie')

    if (setCookie) {
        event.node.res.setHeader('Set-Cookie', setCookie)
    }

    return res._data
})
