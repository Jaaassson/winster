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

const workingHours = computed(() => [
  { day: t('contact.mondayFriday'), time: '9:00 - 18:00' },
  { day: t('contact.saturday'), time: '10:00 - 16:00' },
  { day: t('contact.sunday'), time: t('contact.closed') }
])

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
  <div class="contact-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('contact.title') }}</h1>
        <p class="page-subtitle">{{ t('contact.subtitle') }}</p>
      </div>
    </div>

    <div class="container section">
      <div class="contact-info-grid">
        <div class="info-card">
          <div class="info-icon phone">
            <el-icon :size="28"><Phone /></el-icon>
          </div>
          <h3 class="info-title">{{ t('contact.phone') }}</h3>
          <p class="info-value">{{ siteConfig?.phone || '-' }}</p>
        </div>

        <div class="info-card">
          <div class="info-icon email">
            <el-icon :size="28"><Message /></el-icon>
          </div>
          <h3 class="info-title">{{ t('contact.email') }}</h3>
          <p class="info-value">{{ siteConfig?.email || '-' }}</p>
        </div>

        <div class="info-card">
          <div class="info-icon address">
            <el-icon :size="28"><Location /></el-icon>
          </div>
          <h3 class="info-title">{{ t('contact.address') }}</h3>
          <p class="info-value">{{ address || '-' }}</p>
        </div>

        <div class="info-card">
          <div class="info-icon hours">
            <el-icon :size="28"><Clock /></el-icon>
          </div>
          <h3 class="info-title">{{ t('contact.workingHours') }}</h3>
          <p class="info-value">{{ t('contact.workingHoursValue') }}</p>
        </div>
      </div>
    </div>

    <div class="map-section">
      <div class="map-placeholder">
        <el-icon :size="64" class="map-icon"><Location /></el-icon>
        <p class="map-text">{{ t('contact.mapPlaceholder') }}</p>
        <p class="map-address">{{ address }}</p>
      </div>
    </div>

    <div class="container section">
      <div class="contact-wrapper">
        <div class="contact-left">
          <div class="card">
            <h2 class="section-title">{{ t('contact.sendMessage') }}</h2>
            <p class="section-desc">{{ t('contact.sendMessageDesc') }}</p>
            <InquiryForm />
          </div>
        </div>

        <div class="contact-right">
          <div class="working-hours-card">
            <h3 class="card-title">{{ t('contact.workingHours') }}</h3>
            <div class="hours-list">
              <div class="hours-item" v-for="(item, index) in workingHours" :key="index">
                <span class="hours-day">{{ item.day }}</span>
                <span class="hours-time">{{ item.time }}</span>
              </div>
            </div>
          </div>

          <div class="social-card">
            <h3 class="card-title">{{ t('footer.followUs') }}</h3>
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

          <div class="whatsapp-card" v-if="siteConfig?.whatsapp">
            <div class="whatsapp-icon">
              <el-icon :size="32"><ChatDotRound /></el-icon>
            </div>
            <div class="whatsapp-content">
              <h3>WhatsApp</h3>
              <p>{{ siteConfig.whatsapp }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.contact-page {
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

.contact-info-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.info-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.info-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #fff;

  &.phone {
    background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  }

  &.email {
    background: linear-gradient(135deg, #34a853 0%, #0f9d58 100%);
  }

  &.address {
    background: linear-gradient(135deg, #ea4335 0%, #d93025 100%);
  }

  &.hours {
    background: linear-gradient(135deg, #fbbc05 0%, #f9ab00 100%);
  }
}

.info-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.info-value {
  font-size: 14px;
  color: #666;
  margin: 0;
  word-break: break-word;
}

.map-section {
  width: 100%;
}

.map-placeholder {
  width: 100%;
  height: 360px;
  background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;

  .map-icon {
    margin-bottom: 16px;
    color: #bbb;
  }

  .map-text {
    font-size: 16px;
    margin: 0 0 8px 0;
  }

  .map-address {
    font-size: 14px;
    color: #888;
    margin: 0;
    max-width: 600px;
    text-align: center;
  }
}

.contact-wrapper {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 40px;
  align-items: start;
}

.contact-left {
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
    margin: 0 0 8px 0;
  }

  .section-desc {
    font-size: 14px;
    color: #666;
    margin: 0 0 24px 0;
  }
}

.contact-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.working-hours-card,
.social-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 32px;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 24px 0;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.hours-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hours-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
}

.hours-day {
  font-size: 14px;
  color: #666;
}

.hours-time {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
}

.social-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
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

.whatsapp-card {
  background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(37, 211, 102, 0.3);
  }

  .whatsapp-icon {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .whatsapp-content {
    h3 {
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 4px 0;
    }

    p {
      font-size: 14px;
      margin: 0;
      opacity: 0.9;
    }
  }
}

@media (max-width: 992px) {
  .contact-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .contact-wrapper {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 30px;
  }

  .contact-left {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }

  .contact-right {
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

  .contact-left .card {
    padding: 24px;
    width: 100%;
    margin: 0 auto;
  }

  .working-hours-card,
  .social-card {
    padding: 24px;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 576px) {
  .contact-info-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    padding: 32px 0;

    .page-title {
      font-size: 24px;
    }

    .page-subtitle {
      font-size: 14px;
    }
  }

  .map-placeholder {
    height: 240px;
    padding: 20px;

    .map-text {
      font-size: 14px;
    }

    .map-address {
      font-size: 12px;
    }
  }
}
</style>
