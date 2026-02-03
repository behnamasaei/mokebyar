<template>
  <!-- اضافه کردن فونت وزیرمتن برای ظاهر حرفه‌ای -->

  <div class="min-h-screen relative flex items-center justify-center overflow-hidden  dir-rtl">

    <!-- 1. تصویر پس‌زمینه با کیفیت و دراماتیک -->
    <div class="absolute inset-0 z-0">
      <img
          :src="haramImage"
          alt="Holy Shrine Background"
          class="w-full h-full object-cover"
      >
      <!-- 2. لایه گرادینت برای تمرکز روی فرم (Vignette Effect) -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-black/30"></div>
    </div>

    <!-- افکت نورانی پشت کارت (Glow Effect) -->
    <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/20 rounded-full blur-3xl z-0 pointer-events-none"></div>

    <!-- 3. کانتینر اصلی کارت شیشه‌ای -->
    <div class="relative z-10 w-full max-w-lg px-4">

      <div
          class="bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-500 hover:scale-[1.01]">

        <!-- هدر کارت -->
        <div class="px-10 pt-10 pb-6 text-center">
          <!-- آیکون لوگو با افکت درخشش -->
          <div
              class="mx-auto h-20 w-20 bg-gradient-to-br from-emerald-400 to-emerald-700 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-emerald-500/30 rotate-3 hover:rotate-0 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24"
                 stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
          <h2 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-200 to-white drop-shadow-md">
            ورود به حساب
          </h2>
          <p class="mt-3 text-lg text-gray-300 font-light">
            خوش آمدید، لطفا اطلاعات خود را وارد کنید
          </p>
        </div>

        <!-- بدنه فرم -->
        <div class="px-10 pb-10">
          <form @submit.prevent="handleLogin" class="space-y-6">

            <!-- اینپوت نام کاربری -->
            <div class="group">
              <label for="email" class="block text-sm font-medium text-emerald-200 mb-2 mr-1">ایمیل یا شماره
                موبایل</label>
              <div class="relative">
                <div
                    class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-emerald-400 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <input
                    id="email"
                    name="email"
                    type="text"
                    required
                    v-model="formData.email"
                    class="block w-full pr-12 pl-4 py-4 bg-black/30 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-300 text-base outline-none"
                    placeholder="مثال: user@gmail.com"
                >
              </div>
            </div>

            <!-- اینپوت رمز عبور -->
            <div class="group">
              <div class="flex items-center justify-between mb-2 mr-1">
                <label for="password" class="block text-sm font-medium text-emerald-200">رمز عبور</label>
                <a href="#" class="text-sm font-medium text-emerald-400 hover:text-emerald-300 transition-colors">رمز را
                  فراموش کردید؟</a>
              </div>
              <div class="relative">
                <div
                    class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-400 group-focus-within:text-emerald-400 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                </div>
                <input
                    id="password"
                    name="password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    v-model="formData.password"
                    class="block w-full pr-12 pl-12 py-4 bg-black/30 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all duration-300 text-base outline-none"
                    placeholder="••••••••"
                >
                <!-- دکمه نمایش پسورد -->
                <div
                    class="absolute inset-y-0 left-0 pl-4 flex items-center cursor-pointer text-gray-400 hover:text-white transition-colors"
                    @click="showPassword = !showPassword">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                          v-if="!showPassword"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- چک باکس -->
            <div class="flex items-center mt-2">
              <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  v-model="formData.remember"
                  class="h-5 w-5 text-emerald-600 focus:ring-emerald-500 border-gray-500 rounded bg-white/10"
              >
              <label for="remember-me" class="mr-3 block text-sm text-gray-300 cursor-pointer select-none">
                مرا به خاطر بسپار
              </label>
            </div>

            <!-- دکمه ورود با گرادینت -->
            <button
                type="submit"
                :disabled="isLoading"
                class="w-full flex justify-center py-4 px-4 border border-transparent rounded-xl shadow-lg text-lg font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-emerald-500 transition-all duration-300 transform hover:-translate-y-1 disabled:opacity-50 disabled:transform-none disabled:cursor-not-allowed"
            >
              <span v-if="!isLoading">ورود به حساب کاربری</span>
              <!-- لودینگ -->
              <svg v-else class="animate-spin -ml-1 mr-3 h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg"
                   fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </button>
          </form>
        </div>

        <!-- فوتر -->
        <div class="px-10 py-6 bg-black/20 border-t border-white/5 text-center">
          <p class="text-sm text-gray-400">
            حساب کاربری ندارید؟
            <a href="#" class="font-bold text-emerald-400 hover:text-emerald-300 transition-colors">ثبت نام رایگان</a>
          </p>
        </div>
      </div>

      <p class="mt-6 text-center text-sm text-gray-400/80">
        طراحی شده با عشق و احترام
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import haramImage from '../../../public/images/haram1.jpeg'
import {reactive, ref} from 'vue';
import type {TokenResponse} from '~/types/TokenResponse.ts'

const isLoading = ref(false);
const showPassword = ref(false);

const formData = reactive({
  email: 'admin',
  password: '1q2w3E*',
  remember: false
});


const handleLogin = async () => {
  isLoading.value = true;

  const {data: tokenRes, error, status} = await useFetch<TokenResponse>(
      '/api/auth/token',
      {
        method: 'POST',
        body: {
          username: formData.email,
          password: formData.password
        },
      }
  )

  console.log(tokenRes.value.access_token)
};
</script>

<style>
/* بدون استایل اضافی برای کامپوننت، فقط فونت لود شده است */
</style>