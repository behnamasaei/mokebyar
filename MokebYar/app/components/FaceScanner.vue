
<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-slate-100 p-2 sm:p-4 font-sans text-slate-800">

    <!-- Main Card Container -->
    <div class="bg-white w-full max-w-md rounded-2xl shadow-xl overflow-hidden border border-slate-200 flex flex-col">

      <!-- Header -->
      <div class="bg-slate-900 p-4 flex justify-between items-center shrink-0">
        <h1 class="text-white font-bold text-lg flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
          </svg>
          سیستم تشخیص چهره
        </h1>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full" :class="isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-500'"></span>
        </div>
      </div>

      <!-- Tabs Switcher -->
      <div class="flex p-1 bg-slate-100 m-4 rounded-lg">
        <button
            @click="currentTab = 'recognize'"
            :class="['flex-1 py-2 text-sm font-medium rounded-md transition-all duration-200', currentTab === 'recognize' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']"
        >
          احراز هویت
        </button>
        <button
            @click="currentTab = 'register'"
            :class="['flex-1 py-2 text-sm font-medium rounded-md transition-all duration-200', currentTab === 'register' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']"
        >
          افزودن فرد
        </button>
      </div>

      <!-- Content Body -->
      <div class="px-4 pb-4 flex flex-col gap-4 flex-grow">

        <!-- Name Input (Only for Register) -->
        <transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100" leave-to-class="opacity-0">
          <div v-if="currentTab === 'register'" class="relative">
            <input
                v-model="newUserName"
                type="text"
                placeholder="نام و نام خانوادگی"
                class="w-full pl-4 pr-10 py-3 rounded-lg border border-slate-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all text-sm"
                :disabled="loading"
            />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 text-slate-400">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </div>
          </div>
        </transition>

        <!-- Camera Viewport -->
        <div class="relative w-full aspect-[3/4] sm:aspect-video bg-black rounded-xl overflow-hidden shadow-inner border border-slate-300">

          <video
              ref="videoRef"
              autoplay
              muted
              playsinline
              :class="['w-full h-full object-cover', { 'scale-x-[-1]': isFrontCamera }]"
          ></video>

          <!-- Camera Switch Button -->
          <button
              @click="switchCamera"
              class="absolute top-3 left-3 p-2 bg-black/40 hover:bg-black/60 text-white rounded-full backdrop-blur-md transition-all z-20 disabled:opacity-50"
              :disabled="loading || !streamActive"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </button>

          <!-- Face Guide Overlay -->
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40">
            <div class="w-48 h-64 border-2 border-dashed border-white rounded-3xl"></div>
          </div>

          <!-- Loading Spinner -->
          <div v-if="loading" class="absolute inset-0 flex flex-col items-center justify-center bg-black/70 backdrop-blur-sm text-white z-10">
            <svg class="animate-spin h-10 w-10 text-blue-400 mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-sm font-medium tracking-wide">{{ currentTab === 'register' ? 'در حال ثبت...' : 'در حال اسکن...' }}</span>
          </div>

          <!-- Camera Off State -->
          <div v-if="!streamActive && !loading" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-800 text-slate-400">
            <p class="text-xs">در انتظار دوربین...</p>
          </div>
        </div>

        <!-- Result/Status Card -->
        <transition enter-active-class="transition ease-out duration-300" enter-from-class="transform opacity-0 translate-y-2" enter-to-class="transform opacity-100 translate-y-0" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
          <div v-if="result" class="border rounded-lg p-4 flex items-center justify-between shadow-sm" :class="getStatusClass">
            <div class="flex items-center gap-3">
              <div class="p-2 rounded-full" :class="getIconBgClass">

                <!-- Icon: Recognize Mode -->
                <svg v-if="currentTab === 'recognize'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path v-if="result.name !== 'Unknown'" stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>

                <!-- Icon: Register Mode -->
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>

              </div>
              <div>
                <p class="font-bold text-slate-800">{{ displayResultText }}</p>
                <p class="text-xs text-slate-500">{{ currentTab === 'register' ? 'عملیات ثبت' : 'اطلاعات دریافت شد' }}</p>
              </div>
            </div>
            <div v-if="currentTab === 'recognize' && result.name !== 'Unknown'" class="text-left">
              <span class="text-xs font-bold px-2 py-1 rounded bg-slate-200 text-slate-700">
                {{ ((1 - result.distance) * 100).toFixed(0) }}%
              </span>
            </div>
          </div>
        </transition>

        <!-- Error Message -->
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-xs flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {{ error }}
        </div>

        <!-- Main Action Button -->
        <button
            @click="handleMainAction"
            :disabled="loading || !isConnected || !streamActive || (currentTab === 'register' && !newUserName)"
            class="group relative w-full flex justify-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            :class="currentTab === 'register' ? 'bg-emerald-600 hover:bg-emerald-700 focus:ring-emerald-500 shadow-emerald-500/30' : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 shadow-blue-500/30'"
        >
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
             <svg v-if="!loading" class="h-5 w-5 opacity-70" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path v-if="currentTab === 'register'" stroke-linecap="round" stroke-linejoin="round" d="M19 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM4 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0110.374 21c-2.331 0-4.512-.645-6.374-1.766z" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" d="M3.75 4.875c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5A1.125 1.125 0 013.75 9.375v-4.5z" />
            </svg>
          </span>
          {{ getButtonText }}
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const videoRef = ref(null)
const loading = ref(false)
const result = ref(null)
const error = ref(null)
const isConnected = ref(false)
const streamActive = ref(false)
const isFrontCamera = ref(true) // برای کنترل آینه‌ای شدن تصویر
const currentTab = ref('recognize')
const newUserName = ref('')

// مدیریت دوربین‌ها
const videoDevices = ref([]) // لیست تمام دوربین‌ها
const currentCameraIndex = ref(0) // ایندکس دوربین فعلی

let socket = null
let mediaStream = null

// --- Dynamic WebSocket URL ---
const wsUrl = computed(() => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const hostname = window.location.hostname === 'localhost' ? 'localhost' : window.location.hostname
  return `${protocol}//${hostname}:8765`
})

// --- Computed UI Helpers ---
const getButtonText = computed(() => {
  if (loading.value) return 'در حال پردازش...'
  if (!isConnected.value) return 'در انتظار اتصال به سرور...'
  if (currentTab.value === 'register') return `ثبت چهره برای ${newUserName.value || '...'}`
  return 'اسکن و احراز هویت'
})

const displayResultText = computed(() => {
  if (currentTab.value === 'register') {
    return result.value?.message || 'آماده'
  }
  return result.value?.name || 'ناشناس'
})

const getStatusClass = computed(() => {
  if (currentTab.value === 'register') return 'border-emerald-200 bg-emerald-50'
  return result.value?.name !== 'Unknown' ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
})

const getIconBgClass = computed(() => {
  if (currentTab.value === 'register') return 'bg-emerald-200 text-emerald-700'
  return result.value?.name !== 'Unknown' ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'
})

// --- Lifecycle ---
onMounted(async () => {
  await getVideoDevices()
  await startCamera()
  connectSocket()
})

onUnmounted(() => {
  stopCamera()
  if (socket) socket.close()
})

// --- Camera Management ---
const getVideoDevices = async () => {
  try {
    // 1. درخواست دسترسی موقت برای دریافت لیست دستگاه‌ها
    const initialStream = await navigator.mediaDevices.getUserMedia({ video: true })
    initialStream.getTracks().forEach(track => track.stop())

    // 2. دریافت لیست دستگاه‌ها
    const devices = await navigator.mediaDevices.enumerateDevices()
    videoDevices.value = devices.filter(d => d.kind === 'videoinput')

    // 3. تلاش برای پیدا کردن دوربین جلو به عنوان پیش‌فرض
    if (videoDevices.value.length > 0) {
      const frontCamIndex = videoDevices.value.findIndex(d =>
          d.label.toLowerCase().includes('front') || d.label.toLowerCase().includes('user')
      )
      if (frontCamIndex !== -1) {
        currentCameraIndex.value = frontCamIndex
      } else {
        currentCameraIndex.value = 0
      }
    }
  } catch (err) {
    console.error("Error enumerating devices:", err)
  }
}

const switchCamera = async () => {
  if (videoDevices.value.length <= 1) return

  stopCamera()
  loading.value = true

  // تغییر ایندکس به بعدی (چرخشی)
  currentCameraIndex.value = (currentCameraIndex.value + 1) % videoDevices.value.length

  // تشخیص اینکه دوربین جلو است یا عقب (برای آینه‌ای کردن)
  const currentDevice = videoDevices.value[currentCameraIndex.value]
  isFrontCamera.value = !currentDevice.label.toLowerCase().includes('back') &&
      !currentDevice.label.toLowerCase().includes('environment')

  await startCamera()
}

const startCamera = async () => {
  loading.value = true
  error.value = null

  // تاخیر کوچک برای اطمینان از قطع شدن استریم قبلی
  setTimeout(async () => {
    try {
      if (videoDevices.value.length === 0) {
        throw new Error("هیچ دوربینی یافت نشد.")
      }

      const deviceId = videoDevices.value[currentCameraIndex.value].deviceId
      const constraints = {
        video: {
          deviceId: { exact: deviceId },
          width: { ideal: 640 },
          height: { ideal: 480 }
        }
      }

      mediaStream = await navigator.mediaDevices.getUserMedia(constraints)

      if (videoRef.value) {
        videoRef.value.srcObject = mediaStream
        streamActive.value = true
      }
    } catch (err) {
      console.error("Camera Error:", err)
      error.value = "خطا در راه‌اندازی دوربین."
    } finally {
      loading.value = false
    }
  }, 300)
}

const stopCamera = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
    streamActive.value = false
  }
}

// --- WebSocket Logic ---
const connectSocket = () => {
  try {
    socket = new WebSocket(wsUrl.value)
    socket.onopen = () => {
      isConnected.value = true
      error.value = null
    }
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.status === 'success') {
        result.value = data
        if (currentTab.value === 'register') {
          setTimeout(() => {
            if(result.value?.message?.includes('موفق')) {
              newUserName.value = ''
            }
          }, 2000)
        }
      } else {
        error.value = data.message || "خطای نامشخص"
      }
      loading.value = false
    }
    socket.onerror = () => {
      isConnected.value = false
      error.value = "خطا در اتصال به سرور"
      loading.value = false
    }
    socket.onclose = () => isConnected.value = false
  } catch (e) {
    error.value = "خطا در برقراری ارتباط"
    isConnected.value = false
  }
}

// --- Main Action Logic ---
const handleMainAction = () => {
  if (!socket || socket.readyState !== WebSocket.OPEN) return
  if (!videoRef.value || !streamActive.value) return

  loading.value = true
  result.value = null
  error.value = null

  setTimeout(() => {
    try {
      const canvas = document.createElement('canvas')
      canvas.width = videoRef.value.videoWidth
      canvas.height = videoRef.value.videoHeight
      const ctx = canvas.getContext('2d')

      // اگر دوربین جلو است، تصویر را آینه‌ای ترسیم کنیم تا در خروجی درست باشد
      if (isFrontCamera.value) {
        ctx.translate(canvas.width, 0)
        ctx.scale(-1, 1)
      }

      ctx.drawImage(videoRef.value, 0, 0, canvas.width, canvas.height)

      const base64Image = canvas.toDataURL('image/jpeg', 0.8)

      if (currentTab.value === 'register') {
        socket.send(JSON.stringify({
          action: 'register',
          name: newUserName.value,
          image: base64Image
        }))
      } else {
        socket.send(JSON.stringify({
          action: 'recognize_image',
          image: base64Image
        }))
      }
    } catch (e) {
      error.value = "خطا در پردازش تصویر"
      loading.value = false
    }
  }, 100)
}
</script>