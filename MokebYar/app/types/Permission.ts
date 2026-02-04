export interface PermissionResponse {
    entityDisplayName: string
    groups: PermissionGroup[]
}


export interface PermissionGroup {
    name: string
    displayName: string
    displayNameKey: string | null
    displayNameResource: string | null
    permissions: PermissionDefinition[]
}


export interface PermissionDefinition {
    name: string
    displayName: string
    parentName: string | null
    isGranted: boolean
    allowedProviders: string[]
    grantedProviders: GrantedProvider[]
}


export interface GrantedProvider {
    providerName: string
    providerKey: string
}
