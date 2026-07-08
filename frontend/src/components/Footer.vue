<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { siteConfigApi } from '@/api'
import { getI18nValue } from '@/utils/i18n'
import {
  Phone,
  Message,
  ChatDotRound,
  Location,
  Clock,
  ArrowRight,
  Promotion,
  Share,
  Link,
  VideoPlay
} from '@element-plus/icons-vue'

const { t } = useI18n()
const router = useRouter()
const siteConfig = ref<any>({})

onMounted(async () => {
  try {
    const r = await siteConfigApi.get()
    siteConfig.value = r.data
  } catch (e) {
    console.error(e)
  }
})

const siteName = computed(() => {
  return getI18nValue(siteConfig.value.site_name) || 'WINSTER'
})

const companyName = computed(() => {
  return getI18nValue(siteConfig.value.company_name)
})

const address = computed(() => {
  return getI18nValue(siteConfig.value.address)
})

const workTime = computed(() => {
  return getI18nValue(siteConfig.value.work_time)
})

function goInquiry() {
  router.push('/inquiry')
}

const quickLinks = computed(() => [
  { path: '/', label: t('nav.home') },
  { path: '/products', label: t('nav.products') },
  { path: '/news', label: t('nav.news') },
  { path: '/about', label: t('nav.about') },
  { path: '/contact', label: t('nav.contact') },
  { path: '/inquiry', label: t('nav.inquiry') }
])

const socialLinks = [
  { icon: 'Promotion', label: 'Facebook', url: '#' },
  { icon: 'Share', label: 'Twitter', url: '#' },
  { icon: 'Link', label: 'LinkedIn', url: '#' },
  { icon: 'VideoPlay', label: 'YouTube', url: '#' }
]
</script>

<template>
  <footer class="footer">
    <div class="footer-main">
      <div class="container footer-grid">
        <div class="footer-col footer-about">
          <h3 class="footer-title">{{ siteName }}</h3>
          <p class="footer-desc">
            {{ companyName }}
          </p>
          <div class="footer-social">
            <a
              v-for="social in socialLinks"
              :key="social.label"
              :href="social.url"
              target="_blank"
              rel="noopener noreferrer"
              class="social-link"
              :title="social.label"
            >
              <el-icon><component :is="social.icon" /></el-icon>
            </a>
          </div>
        </div>

        <div class="footer-col">
          <h4 class="footer-subtitle">{{ t('nav.inquiry') }}</h4>
          <p class="footer-contact-item">
            <el-icon><Phone /></el-icon>
            <span>{{ siteConfig.phone || '+86-XXX-XXXXXXX' }}</span>
          </p>
          <p class="footer-contact-item">
            <el-icon><Message /></el-icon>
            <span>{{ siteConfig.email || 'info@example.com' }}</span>
          </p>
          <p v-if="siteConfig.whatsapp" class="footer-contact-item">
            <el-icon><ChatDotRound /></el-icon>
            <span>WhatsApp: {{ siteConfig.whatsapp }}</span>
          </p>
          <button class="footer-inquiry-btn" @click="goInquiry">
            {{ t('nav.inquiry') }}
            <el-icon><ArrowRight /></el-icon>
          </button>
        </div>

        <div class="footer-col">
          <h4 class="footer-subtitle">{{ t('footer.quickLinks') }}</h4>
          <ul class="footer-links">
            <li v-for="link in quickLinks" :key="link.path">
              <router-link :to="link.path">{{ link.label }}</router-link>
            </li>
          </ul>
        </div>

        <div class="footer-col">
          <h4 class="footer-subtitle">{{ t('footer.contact') }}</h4>
          <p class="footer-contact-item">
            <el-icon><Location /></el-icon>
            <span>{{ address }}</span>
          </p>
          <p v-if="workTime" class="footer-contact-item">
            <el-icon><Clock /></el-icon>
            <span>{{ workTime }}</span>
          </p>
          <div v-if="siteConfig.qrcode" class="qrcode-wrapper">
            <p class="qrcode-label">{{ t('footer.qrcode') }}</p>
            <img :src="siteConfig.qrcode" class="qrcode-img" alt="WeChat QR Code" />
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p class="copyright">{{ t('footer.copyright') }}</p>
      </div>
    </div>
  </footer>
</template>

<style scoped lang="scss">
.footer {
  background: #1f2937;
  color: #d1d5db;
  margin-top: 60px;

  .footer-main {
    padding: 60px 0 40px;
  }

  .footer-grid {
    display: grid;
    grid-template-columns: 2fr 1.5fr 1fr 1.5fr;
    gap: 40px;
  }

  .footer-col {
    .footer-title {
      color: #fff;
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 16px;
      letter-spacing: 1px;
    }

    .footer-subtitle {
      color: #fff;
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 20px;
      position: relative;
      padding-bottom: 10px;

      &::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        width: 30px;
        height: 2px;
        background: #1a73e8;
      }
    }

    .footer-desc {
      font-size: 14px;
      line-height: 1.8;
      margin-bottom: 20px;
      color: #9ca3af;
    }
  }

  .footer-about {
    .footer-social {
      display: flex;
      gap: 12px;

      .social-link {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #374151;
        color: #d1d5db;
        font-size: 18px;
        transition: all 0.3s ease;

        &:hover {
          background: #1a73e8;
          color: #fff;
          transform: translateY(-3px);
        }
      }
    }
  }

  .footer-contact-item {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 14px;
      margin-bottom: 12px;
      color: #9ca3af;
      line-height: 1.6;

      .el-icon {
        flex-shrink: 0;
        margin-top: 2px;
        color: #1a73e8;
      }
    }

    .qrcode-wrapper {
      margin-top: 16px;

      .qrcode-label {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 8px;
      }

      .qrcode-img {
        width: 120px;
        height: 120px;
        border-radius: 8px;
        background: #fff;
        padding: 4px;
      }
    }

  .footer-inquiry-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
    padding: 10px 20px;
    background: #1a73e8;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: #1557b0;
      transform: translateY(-2px);
    }
  }

  .footer-links {
    li {
      margin-bottom: 12px;

      a {
        color: #9ca3af;
        font-size: 14px;
        transition: all 0.2s ease;
        position: relative;
        padding-left: 0;

        &::before {
          content: '›';
          position: absolute;
          left: -10px;
          opacity: 0;
          transition: all 0.2s ease;
        }

        &:hover {
          color: #1a73e8;
          padding-left: 12px;

          &::before {
            left: 0;
            opacity: 1;
          }
        }
      }
    }
  }

  .footer-bottom {
    border-top: 1px solid #374151;
    padding: 20px 0;

    .footer-bottom-inner {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .copyright {
      margin: 0;
      font-size: 13px;
      color: #6b7280;
      text-align: center;
    }
  }
}

@media (max-width: 960px) {
  .footer {
    .footer-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 30px;
    }
  }
}

@media (max-width: 600px) {
  .footer {
    .footer-main {
      padding: 40px 0 30px;
    }

    .footer-grid {
      grid-template-columns: 1fr;
      gap: 30px;
    }

    .footer-col {
      .footer-title {
        font-size: 20px;
      }
    }
  }
}
</style>
