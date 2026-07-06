<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { siteConfigApi } from '@/api'
import { getI18nValue } from '@/utils/i18n'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()
const mobileMenuOpen = ref(false)
const siteConfig = ref<any>({})

onMounted(async () => {
  try {
    const r = await siteConfigApi.get()
    siteConfig.value = r.data
    if (r.data?.rate_usd_to_cny) currencyStore.setRate(Number(r.data.rate_usd_to_cny))
  } catch (e) {}
})

const siteName = computed(() => getI18nValue(siteConfig.value.site_name) || 'WINSTER')
const companyName = computed(() => getI18nValue(siteConfig.value.company_name))
const address = computed(() => getI18nValue(siteConfig.value.address))

function goInquiry() { router.push('/inquiry') }
function toggleLang() { langStore.set(langStore.lang === 'en' ? 'zh' : 'en') }
function toggleCurrency() { currencyStore.set(currencyStore.currency === 'USD' ? 'CNY' : 'USD') }
</script>

<template>
  <div class="front-layout">
    <header class="topbar">
      <div class="container topbar-inner">
        <div class="logo" @click="router.push('/')">
          <span class="logo-text">{{ siteName }}</span>
        </div>
        <nav class="nav-desktop">
          <router-link to="/" :class="{active: route.path==='/'}">{{ t('nav.home') }}</router-link>
          <router-link to="/products" :class="{active: route.path.startsWith('/products')}">{{ t('nav.products') }}</router-link>
          <router-link to="/news" :class="{active: route.path.startsWith('/news') && !route.path.startsWith('/admin')}">{{ t('nav.news') }}</router-link>
          <router-link to="/about" :class="{active: route.path==='/about'}">{{ t('nav.about') }}</router-link>
          <router-link to="/contact" :class="{active: route.path==='/contact'}">{{ t('nav.contact') }}</router-link>
        </nav>
        <div class="actions">
          <button class="act-btn" @click="toggleLang">{{ langStore.lang === 'en' ? '中文' : 'EN' }}</button>
          <button class="act-btn" @click="toggleCurrency">{{ currencyStore.currency }}</button>
          <button class="inquiry-btn" @click="goInquiry">{{ t('nav.inquiry') }}</button>
          <button class="menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">☰</button>
        </div>
      </div>
      <div v-if="mobileMenuOpen" class="nav-mobile">
        <router-link to="/" @click="mobileMenuOpen=false">{{ t('nav.home') }}</router-link>
        <router-link to="/products" @click="mobileMenuOpen=false">{{ t('nav.products') }}</router-link>
        <router-link to="/news" @click="mobileMenuOpen=false">{{ t('nav.news') }}</router-link>
        <router-link to="/about" @click="mobileMenuOpen=false">{{ t('nav.about') }}</router-link>
        <router-link to="/contact" @click="mobileMenuOpen=false">{{ t('nav.contact') }}</router-link>
        <router-link to="/inquiry" @click="mobileMenuOpen=false">{{ t('nav.inquiry') }}</router-link>
      </div>
    </header>

    <main><router-view /></main>

    <footer class="footer">
      <div class="container footer-grid">
        <div>
          <h3>{{ siteName }}</h3>
          <p>{{ companyName }}</p>
        </div>
        <div>
          <h4>{{ t('footer.contact') }}</h4>
          <p><strong>{{ t('footer.address') }}:</strong> {{ address }}</p>
          <p><strong>{{ t('footer.phone') }}:</strong> {{ siteConfig.phone }}</p>
          <p><strong>Email:</strong> {{ siteConfig.email }}</p>
          <p v-if="siteConfig.whatsapp"><strong>WhatsApp:</strong> {{ siteConfig.whatsapp }}</p>
        </div>
        <div>
          <h4>{{ t('nav.inquiry') }}</h4>
          <button class="btn-primary" @click="goInquiry">{{ t('nav.inquiry') }}</button>
        </div>
      </div>
      <div class="copyright container">{{ t('footer.copyright') }}</div>
    </footer>
  </div>
</template>

<style scoped>
.front-layout { display: flex; flex-direction: column; min-height: 100vh; }
.topbar { background: #fff; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }
.topbar-inner { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; gap: 20px; }
.logo { cursor: pointer; }
.logo-text { font-size: 22px; font-weight: 700; color: #1a73e8; letter-spacing: 1px; }
.nav-desktop { display: flex; gap: 22px; flex: 1; justify-content: center; }
.nav-desktop a { color: #333; font-size: 15px; padding: 6px 4px; border-bottom: 2px solid transparent; }
.nav-desktop a.active, .nav-desktop a:hover { color: #1a73e8; border-bottom-color: #1a73e8; }
.actions { display: flex; align-items: center; gap: 8px; }
.act-btn { background: #f2f6ff; border: 1px solid #dbe7ff; color: #1a73e8; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.act-btn:hover { background: #e0ecff; }
.inquiry-btn { background: #1a73e8; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.inquiry-btn:hover { background: #1557b0; }
.menu-btn { display: none; background: none; border: 1px solid #ddd; padding: 6px 10px; border-radius: 4px; cursor: pointer; }
.nav-mobile { display: none; flex-direction: column; border-top: 1px solid #eee; padding: 10px 20px; background: #fff; }
.nav-mobile a { padding: 10px 0; color: #333; border-bottom: 1px solid #f5f5f5; }
main { flex: 1; }
.footer { background: #1f2937; color: #ddd; margin-top: 60px; }
.footer h3 { color: #fff; font-size: 18px; }
.footer h4 { color: #fff; font-size: 15px; }
.footer-grid { display: grid; grid-template-columns: 2fr 2fr 1fr; gap: 40px; padding: 50px 20px 30px; }
.footer p { margin: 6px 0; font-size: 14px; }
.copyright { border-top: 1px solid #374151; padding: 20px; text-align: center; color: #9ca3af; font-size: 13px; }
@media (max-width: 900px) {
  .nav-desktop { display: none; }
  .menu-btn { display: inline-block; }
  .inquiry-btn { display: none; }
  .footer-grid { grid-template-columns: 1fr; padding: 40px 20px 20px; gap: 30px; }
}
</style>