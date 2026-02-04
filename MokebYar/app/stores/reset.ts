import {useLoginStore} from "~/stores/loginStore";
import {usePermissionStore} from "~/stores/permissionStore";
import {useProfileStore} from "~/stores/profileStore";
import {useTokenStore} from "~/stores/tokenStore";
import {useUserStore} from "~/stores/userStore";


export function resetAllStores() {
    useLoginStore().$reset()
    usePermissionStore().$reset()
    useProfileStore().$reset()
    useTokenStore().$reset()
    useUserStore().$reset()
}