import { createI18n } from 'vue-i18n'
import enUS from './en-US'
import zhCN from './zh-CN'
import storage from '@/utils/storage'

export type Locale = 'en' | 'zh'

const savedLocale = (storage.get('locale') as Locale) || 'zh'

const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: {
    en: enUS,
    zh: zhCN
  }
})

export function setLocale(locale: Locale): void {
  i18n.global.locale.value = locale
  storage.set('locale', locale)
}

export function getLocale(): Locale {
  return i18n.global.locale.value as Locale
}

export default i18n
