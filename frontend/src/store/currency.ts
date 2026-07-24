import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useLangStore } from '@/store/lang'

export const useCurrencyStore = defineStore('currency', () => {
  const currency = ref<string>((typeof localStorage !== 'undefined' && localStorage.getItem('currency')) || 'CNY')
  const rate = ref<number>(7.2)

  function set(c: string) {
    currency.value = c
    localStorage.setItem('currency', c)
    // 联动语言：CNY -> 中文，USD -> 英文
    const langStore = useLangStore()
    if (c === 'CNY') {
      langStore.set('zh')
    } else if (c === 'USD') {
      langStore.set('en')
    }
  }
  function setRate(r: number) {
    rate.value = r
  }
  function format(price: number | string | null | undefined, sourceCurrency: string = 'USD'): string {
    if (price === null || price === undefined || price === '') return '-'
    const n = Number(price)
    if (Number.isNaN(n)) return '-'
    if (currency.value === sourceCurrency) {
      return currency.value === 'CNY' ? `¥ ${n.toFixed(2)}` : `$ ${n.toFixed(2)}`
    }
    if (currency.value === 'CNY' && sourceCurrency === 'USD') {
      return `¥ ${(n * rate.value).toFixed(2)}`
    }
    if (currency.value === 'USD' && sourceCurrency === 'CNY') {
      return `$ ${(n / rate.value).toFixed(2)}`
    }
    return currency.value === 'CNY' ? `¥ ${n.toFixed(2)}` : `$ ${n.toFixed(2)}`
  }
  const symbol = computed(() => (currency.value === 'CNY' ? '¥' : '$'))
  return { currency, rate, set, setRate, format, symbol }
})