export type Currency = 'USD' | 'CNY'

const exchangeRate = 7.2

export function formatPrice(price: number | string | null | undefined, currency: Currency = 'USD'): string {
  if (price === null || price === undefined || price === '') {
    return '-'
  }
  const num = Number(price)
  if (isNaN(num)) {
    return '-'
  }
  if (currency === 'CNY') {
    return `¥ ${(num * exchangeRate).toFixed(2)}`
  }
  return `$ ${num.toFixed(2)}`
}

export function getCurrencySymbol(currency: Currency = 'USD'): string {
  return currency === 'CNY' ? '¥' : '$'
}

export function setExchangeRate(rate: number): void {
  ;(exchangeRate as any) = rate
}

export function getExchangeRate(): number {
  return exchangeRate
}
