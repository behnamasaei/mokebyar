export default defineNitroPlugin(() => {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'
})
