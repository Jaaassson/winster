<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { siteConfigApi } from '@/api'
import LangSwitch from './LangSwitch.vue'
import CurrencySwitch from './CurrencySwitch.vue'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()
const mobileMenuOpen = ref(false)
const siteConfig = ref<any>({})
const scrolled = ref(false)

onMounted(async () => {
  try {
    const r = await siteConfigApi.get()
    siteConfig.value = r.data
    if (r.data?.rate_usd_to_cny) {
      currencyStore.setRate(Number(r.data.rate_usd_to_cny))
    }
  } catch (e) {
    console.error(e)
  }

  window.addEventListener('scroll', handleScroll)
})

function handleScroll() {
  scrolled.value = window.scrollY > 10
}

function t2(en: string, zh: string) {
  return langStore.lang === 'zh' ? (zh || en) : (en || zh)
}

function goInquiry() {
  router.push('/inquiry')
  mobileMenuOpen.value = false
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

const navItems = computed(() => [
  { path: '/', key: 'home', label: t('nav.home') },
  { path: '/products', key: 'products', label: t('nav.products') },
  { path: '/about', key: 'about', label: t('nav.about') },
  { path: '/contact', key: 'contact', label: t('nav.contact') },
  { path: '/faq', key: 'faq', label: t('nav.faq') },
  { path: '/inquiry', key: 'inquiry', label: t('nav.inquiry') }
])

function isActive(path: string) {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

<template>
  <header class="header" :class="{ scrolled }">
    <div class="container header-inner">
      <div class="logo" @click="router.push('/')">
        <img
          v-if="siteConfig.logo_url"
          :src="siteConfig.logo_url"
          alt="Logo"
          class="logo-img"
        />
        <span class="logo-text">{{ t2(siteConfig.site_name_en, siteConfig.site_name_zh) || 'WINSTER' }}</span>
      </div>

      <nav class="nav-desktop">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          :class="{ active: isActive(item.path) }"
          class="nav-link"
        >
          {{ item.label }}
        </router-link>
      </nav>

      <div class="header-actions">
        <LangSwitch />
        <CurrencySwitch />
        <button class="inquiry-btn" @click="goInquiry">
          <el-icon><ChatDotRound /></el-icon>
          <span>{{ t('nav.inquiry') }}</span>
        </button>
        <button class="menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <el-icon v-if="!mobileMenuOpen"><Menu /></el-icon>
          <el-icon v-else><Close /></el-icon>
        </button>
      </div>
    </div>

    <div v-if="mobileMenuOpen" class="nav-mobile">
      <div class="container">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          :class="{ active: isActive(item.path) }"
          class="mobile-nav-link"
          @click="closeMobileMenu"
        >
          {{ item.label }}
        </router-link>
        <div class="mobile-actions">
          <LangSwitch />
          <CurrencySwitch />
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.header {
  background: #fff;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: box-shadow 0.3s ease;

  &.scrolled {
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  }

  .header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    gap: 20px;
    height: 70px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    flex-shrink: 0;

    .logo-img {
      height: 40px;
      width: auto;
    }

    .logo-text {
      font-size: 22px;
      font-weight: 700;
      color: #1a73e8;
      letter-spacing: 1px;
    }
  }

  .nav-desktop {
    display: flex;
    gap: 28px;
    flex: 1;
    justify-content: center;

    .nav-link {
      color: #333;
      font-size: 15px;
      font-weight: 500;
      padding: 8px 2px;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      position: relative;

      &:hover,
      &.active {
        color: #1a73e8;
        border-bottom-color: #1a73e8;
      }
    }
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;

    .inquiry-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #1a73e8;
      color: #fff;
      border: none;
      padding: 8px 18px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s ease;

      &:hover {
        background: #1557b0;
        transform: translateY(-1px);
      }
    }

    .menu-btn {
      display: none;
      background: none;
      border: 1px solid #ddd;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 20px;
      color: #333;
      transition: all 0.2s ease;

      &:hover {
        border-color: #1a73e8;
        color: #1a73e8;
      }
    }
  }

  .nav-mobile {
    display: none;
    border-top: 1px solid #eee;
    background: #fff;
    animation: slideDown 0.3s ease;

    .container {
      padding: 10px 20px 20px;
    }

    .mobile-nav-link {
      display: block;
      padding: 14px 0;
      color: #333;
      font-size: 16px;
      border-bottom: 1px solid #f5f5f5;
      transition: all 0.2s ease;

      &:last-of-type {
        border-bottom: none;
      }

      &:hover,
      &.active {
        color: #1a73e8;
      }
    }

    .mobile-actions {
      display: flex;
      gap: 10px;
      padding-top: 16px;
      border-top: 1px solid #f5f5f5;
      margin-top: 8px;
    }
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 960px) {
  .header {
    .nav-desktop {
      display: none;
    }

    .header-actions {
      .inquiry-btn {
        display: none;
      }

      .menu-btn {
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }

    .nav-mobile {
      display: block;
    }
  }
}

@media (max-width: 600px) {
  .header {
    .header-inner {
      padding: 12px 16px;
      gap: 10px;
      height: auto;
    }

    .logo {
      .logo-text {
        font-size: 18px;
      }

      .logo-img {
        height: 32px;
      }
    }

    .header-actions {
      gap: 8px;
    }
  }
}
</style>
