<template>
  <div class="h-full">
    <div class="card dock-demo">
      <Toast position="top-center" group="tc"/>

      <Menubar :model="menubarItems">
        <template #start>
          <i class="pi pi-apple px-2"></i>
        </template>
        <template #end>
          <span class="px-2 ltr-text">
            {{ formattedNow }}
          </span>
          <i class="pi pi-calendar-clock px-2"/>
        </template>
      </Menubar>

      <slot/>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount} from 'vue';
import {useToast} from 'primevue/usetoast';
import {DateTime} from "luxon";
import jalaali from "jalaali-js";


const router = useRouter();
const toast = useToast();
const permissionStore = usePermissionStore();
const now = ref(DateTime.now().setZone("Asia/Tehran"));
const timer = ref<number | null>(null)

const menubarItems = computed(() => {
  const items = []

  const permissions = permissionStore.permissions

  if (permissions?.groups?.some(x => x.name === 'AbpTenantManagement')) {
    items.push({
      label: 'مستاجران',
      class: 'menubar-root',
      icon: 'pi pi-building-columns',
      command: () => {
        router.push('/dashboard/tenants')
      }
    })
  }

  return items
})

onMounted(() => {
  timer.value = window.setInterval(() => {
    now.value = DateTime.now().setZone("Asia/Tehran")
  }, 1000)


})

onBeforeUnmount(() => {
  if (timer.value !== null) {
    window.clearInterval(timer.value)
  }
})

const formattedNow = computed(() => {
  if (!now.value) return ''

  const {jy, jm, jd} = jalaali.toJalaali(
      now.value.year,
      now.value.month,
      now.value.day
  )

  return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')} ${now.value.toFormat('HH:mm:ss')}`
})


</script>

<style scoped>

</style>
