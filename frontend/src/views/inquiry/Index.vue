<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { siteConfigApi } from '@/api'
import InquiryForm from '@/components/InquiryForm.vue'
import { Phone, Message, Location, Clock, ChatDotRound } from '@element-plus/icons-vue'
import { getI18nValue } from '@/utils/i18n'

const { t } = useI18n()
const siteConfig = ref<any>(null)

const address = computed(() => {
  if (!siteConfig.value) return ''
  return getI18nValue(siteConfig.value.address)
})

onMounted(async () => {
  try {
    const res = await siteConfigApi.get()
    siteConfig.value = res.data
  } catch (e) {
    console.error('Failed to load site config')
  }
})
</script>

<template>
  <div class="inquiry-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('inquiry.title') }}</h1>
        <p class="page-subtitle">{{ t('inquiry.subtitle') }}</p>
      </div>
    </div>

    <div class="container section">
      <div class="inquiry-wrapper">
        <div class="inquiry-left">
          <div class="card">
          <h2 class="section-title">{{ t('inquiry.sendInquiry') }}</h2>
          <InquiryForm />
        </div>
        </div>

        <div class="inquiry-right">
          <div class="contact-info-card">
            <h3 class="info-title">{{ t('contact.getInTouch') }}</h3>

            <div class="contact-item">
              <div class="contact-icon">
                <el-icon :size="24"><Phone /></el-icon>
              </div>
              <div class="contact-content">
                <div class="contact-label">{{ t('contact.phone') }}</div>
                <div class="contact-value">{{ siteConfig?.phone || '-' }}</div>
              </div>
            </div>

            <div class="contact-item">
              <div class="contact-icon">
                <el-icon :size="24"><Message /></el-icon>
              </div>
              <div class="contact-content">
                <div class="contact-label">{{ t('contact.email') }}</div>
                <div class="contact-value">{{ siteConfig?.email || '-' }}</div>
              </div>
            </div>

            <div class="contact-item" v-if="siteConfig?.whatsapp">
              <div class="contact-icon whatsapp">
                <el-icon :size="24"><ChatDotRound /></el-icon>
              </div>
              <div class="contact-content">
                <div class="contact-label">WhatsApp</div>
                <div class="contact-value">{{ siteConfig.whatsapp }}</div>
              </div>
            </div>

            <div class="contact-item">
              <div class="contact-icon">
                <el-icon :size="24"><Location /></el-icon>
              </div>
              <div class="contact-content">
                <div class="contact-label">{{ t('contact.address') }}</div>
                <div class="contact-value">{{ address || '-' }}</div>
              </div>
            </div>

            <div class="contact-item">
              <div class="contact-icon">
                <el-icon :size="24"><Clock /></el-icon>
              </div>
              <div class="contact-content">
                <div class="contact-label">{{ t('contact.workingHours') }}</div>
                <div class="contact-value">{{ t('contact.workingHoursValue') }}</div>
              </div>
            </div>
          </div>

          <div class="social-card">
            <h3 class="info-title">{{ t('footer.followUs') }}</h3>
            <div class="social-links">
              <a v-if="siteConfig?.facebook" :href="siteConfig.facebook" target="_blank" class="social-link facebook">
                <span>Facebook</span>
              </a>
              <a v-if="siteConfig?.twitter" :href="siteConfig.twitter" target="_blank" class="social-link twitter">
                <span>Twitter</span>
              </a>
              <a v-if="siteConfig?.linkedin" :href="siteConfig.linkedin" target="_blank" class="social-link linkedin">
                <span>LinkedIn</span>
              </a>
              <a v-if="siteConfig?.instagram" :href="siteConfig.instagram" target="_blank" class="social-link instagram">
                <span>Instagram</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.inquiry-page {
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  color: #fff;
  padding: 60px 0;
  text-align: center;

  .page-title {
    font-size: 36px;
    font-weight: 600;
    margin: 0 0 12px 0;
  }

  .page-subtitle {
    font-size: 16px;
    opacity: 0.9;
    margin: 0;
  }
}

.section {
  padding: 60px 0;
}

.inquiry-wrapper {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 40px;
  align-items: start;
}

.inquiry-left {
  .card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    padding: 40px;
  }

  .section-title {
    font-size: 24px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0 0 24px 0;
  }
}

.inquiry-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.contact-info-card,
.social-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 32px;
}

.info-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
}

.contact-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
  color: #1a73e8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &.whatsapp {
    background: linear-gradient(135deg, #dcf8c6 0%, #c5e8a8 100%);
    color: #25d366;
  }
}

.contact-content {
  flex: 1;
  min-width: 0;
}

.contact-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.contact-value {
  font-size: 15px;
  color: #1a1a1a;
  font-weight: 500;
  word-break: break-word;
}

.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;

  &.facebook {
    background: #1877f2;
    color: #fff;
    &:hover { background: #166fe5; transform: translateY(-2px); }
  }

  &.twitter {
    background: #1da1f2;
    color: #fff;
    &:hover { background: #1a91da; transform: translateY(-2px); }
  }

  &.linkedin {
    background: #0a66c2;
    color: #fff;
    &:hover { background: #0958a8; transform: translateY(-2px); }
  }

  &.instagram {
    background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    color: #fff;
    &:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(225, 48, 108, 0.4); }
  }
}

@media (max-width: 992px) {
  .inquiry-wrapper {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 30px;
  }

  .inquiry-left {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  .inquiry-right {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  .page-header {
    padding: 40px 0;

    .page-title {
      font-size: 28px;
    }
  }

  .section {
    padding: 40px 0;
  }

  .inquiry-left .card {
    padding: 20px;
    width: 100%;
    margin: 0 auto;
  }

  .contact-info-card,
  .social-card {
    padding: 20px;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 576px) {
  .page-header {
    padding: 32px 0;

    .page-title {
      font-size: 24px;
    }

    .page-subtitle {
      font-size: 14px;
    }
  }

  .social-links {
    flex-direction: column;
  }

  .social-link {
    width: 100%;
  }
}
</style>
