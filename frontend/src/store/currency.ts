import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCurrencyStore = defineStore('currency', () => {
  const currency = ref<string>((typeof localStorage !== 'undefined' && localStorage.getItem('currency')) || 'CNY')
  const rate = ref<number>(7.2)

  function set(c: string) {
    currency.value = c
    localStorage.setItem('currency', c)
  }
  function setRate(r: number) {
    rate.value = r
  }
  function format(usd: number | string | null | undefined): string {
    if (usd === null || usd === undefined || usd === '') return '-'
    const n = Number(usd)
    if (currency.value === 'CNY') {
      return `¥ ${(n * rate.value).toFixed(2)}`
    }
    return `$ ${n.toFixed(2)}`
  }
  const symbol = computed(() => (currency.value === 'CNY' ? '¥' : '$'))
  return { currency, rate, set, setRate, format, symbol }
})