import { defineStore } from 'pinia'
import { ref } from 'vue'
import i18n from '@/i18n'
import storage from '@/utils/storage'

export const useLangStore = defineStore('lang', () => {
  const lang = ref<string>(i18n.global.locale.value || 'zh')
  function set(l: string) {
    lang.value = l
    ;(i18n.global.locale as any).value = l
    storage.set('locale', l)
  }
  return { lang, set }
})
