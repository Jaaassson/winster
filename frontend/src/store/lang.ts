import { defineStore } from 'pinia'
import { ref } from 'vue'
import i18n from '@/i18n'
import storage from '@/utils/storage'
import { useCurrencyStore } from '@/store/currency'

export const useLangStore = defineStore('lang', () => {
  const lang = ref<string>(i18n.global.locale.value || 'zh')
  function set(l: string) {
    lang.value = l
    ;(i18n.global.locale as any).value = l
    storage.set('locale', l)
    // 联动货币：中文 -> CNY，英文 -> USD
    const currencyStore = useCurrencyStore()
    if (l === 'zh') {
      currencyStore.set('CNY')
    } else if (l === 'en') {
      currencyStore.set('USD')
    }
  }
  return { lang, set }
})
