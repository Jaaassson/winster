import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>((typeof localStorage !== 'undefined' && localStorage.getItem('token')) || '')
  const username = ref<string>((typeof localStorage !== 'undefined' && localStorage.getItem('username')) || '')

  function set(t: string, u: string) {
    token.value = t
    username.value = u
    localStorage.setItem('token', t)
    localStorage.setItem('username', u)
  }
  function clear() {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }
  function isLoggedIn() {
    return !!token.value
  }
  return { token, username, set, clear, isLoggedIn }
})