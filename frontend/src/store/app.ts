import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { setLocale, getLocale, type Locale } from '@/i18n'
import storage from '@/utils/storage'
import type { Currency } from '@/utils/currency'

export const useAppStore = defineStore('app', () => {
  const language = ref<Locale>(getLocale())
  const currency = ref<Currency>((storage.get('currency') as Currency) || 'USD')
  const exchangeRate = ref<number>(7.2)

  const currencySymbol = computed(() => {
    return currency.value === 'CNY' ? '¥' : '$'
  })

  function changeLanguage(lang: Locale): void {
    language.value = lang
    setLocale(lang)
  }

  function changeCurrency(curr: Currency): void {
    currency.value = curr
    storage.set('currency', curr)
  }

  function setExchangeRate(rate: number): void {
    exchangeRate.value = rate
  }

  function formatPrice(price: number | string | null | undefined): string {
    if (price === null || price === undefined || price === '') {
      return '-'
    }
    const num = Number(price)
    if (isNaN(num)) {
      return '-'
    }
    if (currency.value === 'CNY') {
      return `¥ ${(num * exchangeRate.value).toFixed(2)}`
    }
    return `$ ${num.toFixed(2)}`
  }

  return {
    language,
    currency,
    exchangeRate,
    currencySymbol,
    changeLanguage,
    changeCurrency,
    setExchangeRate,
    formatPrice
  }
})
