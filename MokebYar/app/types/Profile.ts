export interface Profile {
    "userName": string,
    "email": string,
    "name": string,
    "surname": string | null,
    "phoneNumber": string | null,
    "isExternal": boolean,
    "hasPassword": boolean,
    "concurrencyStamp": string,
    "extraProperties": object
}