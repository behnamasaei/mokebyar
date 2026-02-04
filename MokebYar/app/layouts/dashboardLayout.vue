<template>
  <div class="h-full">
    <div class="card dock-demo">
      <Toast position="top-center" group="tc"/>

      <Menubar :model="menubarItems">
        <template #start>
          <i class="pi pi-apple px-2"></i>
        </template>
        <template #end>
          <i class="pi pi-video px-2"/>
          <i class="pi pi-wifi px-2"/>
          <i class="pi pi-volume-up px-2"/>
          <span class="px-2">
            {{ formattedNow }}
          </span>
          <i class="pi pi-search px-2"/>
          <i class="pi pi-bars px-2"/>
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


const toast = useToast();
const now = ref(DateTime.now().setZone("Asia/Tehran"));
const timer = ref<number | null>(null)
const menubarItems = ref([
  {
    label: 'Finder',
    class: 'menubar-root'
  },
  {
    label: 'File',
    items: [
      {
        label: 'New',
        icon: 'pi pi-fw pi-plus',
        items: [
          {
            label: 'Bookmark',
            icon: 'pi pi-fw pi-bookmark'
          },
          {
            label: 'Video',
            icon: 'pi pi-fw pi-video'
          },

        ]
      },
      {
        label: 'Delete',
        icon: 'pi pi-fw pi-trash'
      },
      {
        separator: true
      },
      {
        label: 'Export',
        icon: 'pi pi-fw pi-external-link'
      }
    ]
  },
  {
    label: 'Edit',
    items: [
      {
        label: 'Left',
        icon: 'pi pi-fw pi-align-left'
      },
      {
        label: 'Right',
        icon: 'pi pi-fw pi-align-right'
      },
      {
        label: 'Center',
        icon: 'pi pi-fw pi-align-center'
      },
      {
        label: 'Justify',
        icon: 'pi pi-fw pi-align-justify'
      },

    ]
  },
  {
    label: 'Users',
    items: [
      {
        label: 'New',
        icon: 'pi pi-fw pi-user-plus',
      },
      {
        label: 'Delete',
        icon: 'pi pi-fw pi-user-minus',

      },
      {
        label: 'Search',
        icon: 'pi pi-fw pi-users',
        items: [
          {
            label: 'Filter',
            icon: 'pi pi-fw pi-filter',
            items: [
              {
                label: 'Print',
                icon: 'pi pi-fw pi-print'
              }
            ]
          },
          {
            icon: 'pi pi-fw pi-bars',
            label: 'List'
          }
        ]
      }
    ]
  },
  {
    label: 'Events',
    items: [
      {
        label: 'Edit',
        icon: 'pi pi-fw pi-pencil',
        items: [
          {
            label: 'Save',
            icon: 'pi pi-fw pi-calendar-plus'
          },
          {
            label: 'Delete',
            icon: 'pi pi-fw pi-calendar-minus'
          }
        ]
      },
      {
        label: 'Archive',
        icon: 'pi pi-fw pi-calendar-times',
        items: [
          {
            label: 'Remove',
            icon: 'pi pi-fw pi-calendar-minus'
          }
        ]
      }
    ]
  },
  {
    label: 'Quit'
  }
]);

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

  const { jy, jm, jd } = jalaali.toJalaali(
      now.value.year,
      now.value.month,
      now.value.day
  )

  return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')} ${now.value.toFormat('HH:mm:ss')}`
})


</script>

<style scoped>

</style>
