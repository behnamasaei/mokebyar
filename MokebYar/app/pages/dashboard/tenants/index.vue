<script setup lang="ts">
import {ref, reactive, onMounted, watch} from 'vue'
import Toast from 'primevue/toast'
import {useToast} from 'primevue/usetoast'
import {useTenantStore} from "~/stores/tenantStore";

/** =====================
 * Types (ABP Swagger)
 * ===================== */
interface TenantDto {
  id: string
  name: string
  isActive: boolean
}

interface PagedResult<T> {
  items: T[]
  totalCount: number
}

/** =====================
 * State
 * ===================== */
const toast = useToast()
const tenantStore = useTenantStore()

const tenants = ref<TenantDto[]>([])
const totalCount = ref(0)
const loading = ref(false)

const page = ref(0)
const rows = ref(10)
const filter = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)

const form = reactive({
  id: '',
  name: ''
})

/** =====================
 * API helpers
 * ===================== */
const api = $fetch.create({
  baseURL: '/api/tenant',
  credentials: 'include'
})

async function fetchTenants() {
  await tenantStore.fetchAsync()
}

async function createTenant() {
  await api('/api/multi-tenancy/tenants', {
    method: 'POST',
    body: {name: form.name}
  })
  toast.add({severity: 'success', summary: 'Tenant created'})
  dialogVisible.value = false
  fetchTenants()
}

async function updateTenant() {
  await api(`/api/multi-tenancy/tenants/${form.id}`, {
    method: 'PUT',
    body: {name: form.name}
  })
  toast.add({severity: 'success', summary: 'Tenant updated'})
  dialogVisible.value = false
  fetchTenants()
}

async function deleteTenant(id: string) {
  await api(`/${id}`, {method: 'DELETE'})
  toast.add({severity: 'success', summary: 'Tenant deleted'})
  fetchTenants()
}

/** =====================
 * UI handlers
 * ===================== */
function openCreate() {
  isEdit.value = false
  form.id = ''
  form.name = ''
  dialogVisible.value = true
}

function openEdit(t: TenantDto) {
  isEdit.value = true
  form.id = t.id
  form.name = t.name
  dialogVisible.value = true
}

onMounted(fetchTenants)
watch([page, rows], fetchTenants)

</script>

<template>
  <Toast/>

  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-800">مدیریت تننت‌ها</h1>
      <Button label="ایجاد تننت" icon="pi pi-plus" @click="openCreate"/>
    </div>

    <!-- Filter -->
    <div class="flex gap-2">
      <InputText v-model="filter" placeholder="جستجو..." class="w-64"/>
      <Button icon="pi pi-search" @click="fetchTenants"/>
    </div>

    <!-- Table -->
    <DataTable
        :value="tenantStore.tenants"
        :loading="loading"
        :rows="rows"
        :totalRecords="tenantStore.totalCount"
        paginator
        lazy
        @page="e => { page = e.page; rows = e.rows }"
        class="rounded-xl shadow"
    >
      <Column field="name" header="نام تننت"/>
      <Column header="عملیات" style="width: 180px">
        <template #body="{ data }">
          <div class="flex gap-2">
            <Button icon="pi pi-pencil" severity="secondary" @click="openEdit(data)"/>
            <Button icon="pi pi-trash" severity="danger" @click="deleteTenant(data.id)"/>
          </div>
        </template>
      </Column>
    </DataTable>
  </div>

  <!-- Dialog -->
  <Dialog v-model:visible="dialogVisible" modal header="تننت" class="w-full max-w-md">
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">نام تننت</label>
        <InputText v-model="form.name" class="w-full"/>
      </div>

      <div class="flex justify-end gap-2">
        <Button label="انصراف" severity="secondary" @click="dialogVisible = false"/>
        <Button
            label="ذخیره"
            @click="isEdit ? updateTenant() : createTenant()"
        />
      </div>
    </div>
  </Dialog>
</template>
