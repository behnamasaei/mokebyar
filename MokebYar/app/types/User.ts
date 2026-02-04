export interface User {
    "id": string,
    "userName": string,
    "email": string,
    "name": string,
    "surname": string | null,
    "phoneNumber": string | null,
    "isActive": boolean,
    "emailConfirmed": boolean,
    "phoneNumberConfirmed": boolean,
    "creationTime": string | Date,
    "roles": [
        string
    ],
    "claims": unknown[],
    "extraProperties": object
}