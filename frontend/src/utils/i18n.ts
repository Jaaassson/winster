import { getLocale } from '@/i18n'

export function parseI18nField(value: any): Record<string, string> {
  if (!value) return {}
  if (typeof value === 'object') return value
  try {
    return JSON.parse(value)
  } catch {
    return { 'en': value, 'zh': value }
  }
}

export function getI18nValue(value: any, locale?: string): string {
  const parsed = parseI18nField(value)
  const lang = locale || getLocale()
  const langMap: Record<string, string> = {
    'en': 'en-US',
    'zh': 'zh-CN'
  }
  const key = langMap[lang] || lang
  return parsed[key] || parsed[lang] || parsed['en-US'] || parsed['zh-CN'] || value || ''
}
