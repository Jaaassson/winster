import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import storage from '@/utils/storage'
import type { UserInfo } from '@/types'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(storage.get('token') || '')
  const userInfo = ref<UserInfo | null>(storage.getJSON<UserInfo>('userInfo'))

  const isLoggedIn = computed(() => !!token.value)

  function login(newToken: string, user: UserInfo): void {
    token.value = newToken
    userInfo.value = user
    storage.set('token', newToken)
    storage.setJSON('userInfo', user)
  }

  function logout(): void {
    token.value = ''
    userInfo.value = null
    storage.remove('token')
    storage.remove('userInfo')
  }

  function updateUserInfo(user: Partial<UserInfo>): void {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...user }
      storage.setJSON('userInfo', userInfo.value)
    }
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    login,
    logout,
    updateUserInfo
  }
})
