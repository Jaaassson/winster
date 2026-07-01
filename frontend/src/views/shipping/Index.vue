<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLangStore } from '@/store/lang'
import { siteConfigApi } from '@/api'
import { Van, Clock, Money, Box, Warning, CircleCheck } from '@element-plus/icons-vue'
import type { SiteConfig } from '@/types'

const { t } = useI18n()
const langStore = useLangStore()
const siteConfig = ref<SiteConfig | null>(null)

const shippingContent = computed(() => {
  if (!siteConfig.value) return ''
  return langStore.lang === 'zh'
    ? siteConfig.value.shipping_zh || siteConfig.value.shipping_en
    : siteConfig.value.shipping_en || siteConfig.value.shipping_zh
})

const shippingMethods = computed(() => [
  {
    icon: Van,
    titleKey: 'shipping.airExpress',
    descKey: 'shipping.airExpressDesc',
    timeKey: 'shipping.airExpressTime',
    features: [
      'shipping.airExpressFeature1',
      'shipping.airExpressFeature2',
      'shipping.airExpressFeature3'
    ],
    color: '#1a73e8'
  },
  {
    icon: Box,
    titleKey: 'shipping.seaFreight',
    descKey: 'shipping.seaFreightDesc',
    timeKey: 'shipping.seaFreightTime',
    features: [
      'shipping.seaFreightFeature1',
      'shipping.seaFreightFeature2',
      'shipping.seaFreightFeature3'
    ],
    color: '#34a853'
  },
  {
    icon: Van,
    titleKey: 'shipping.landTransport',
    descKey: 'shipping.landTransportDesc',
    timeKey: 'shipping.landTransportTime',
    features: [
      'shipping.landTransportFeature1',
      'shipping.landTransportFeature2',
      'shipping.landTransportFeature3'
    ],
    color: '#fbbc05'
  }
])

const shippingTime = computed(() => [
  { regionKey: 'shipping.regionAsia', timeKey: 'shipping.timeAsia' },
  { regionKey: 'shipping.regionEurope', timeKey: 'shipping.timeEurope' },
  { regionKey: 'shipping.regionNorthAmerica', timeKey: 'shipping.timeNorthAmerica' },
  { regionKey: 'shipping.regionSouthAmerica', timeKey: 'shipping.timeSouthAmerica' },
  { regionKey: 'shipping.regionAfrica', timeKey: 'shipping.timeAfrica' },
  { regionKey: 'shipping.regionOceania', timeKey: 'shipping.timeOceania' }
])

const packagingInfo = computed(() => [
  { titleKey: 'shipping.standardPack', descKey: 'shipping.standardPackDesc' },
  { titleKey: 'shipping.customPack', descKey: 'shipping.customPackDesc' },
  { titleKey: 'shipping.exportPack', descKey: 'shipping.exportPackDesc' }
])

const notes = computed(() => [
  'shipping.note1',
  'shipping.note2',
  'shipping.note3',
  'shipping.note4',
  'shipping.note5',
  'shipping.note6'
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
  <div class="shipping-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('shipping.title') }}</h1>
        <p class="page-subtitle">{{ t('shipping.subtitle') }}</p>
      </div>
    </div>

    <div class="container section">
      <h2 class="section-title text-center">{{ t('shipping.shippingMethods') }}</h2>
      <p class="section-subtitle text-center">{{ t('shipping.shippingMethodsSubtitle') }}</p>
      <div class="methods-grid">
        <div
          v-for="(method, index) in shippingMethods"
          :key="index"
          class="method-card"
        >
          <div class="method-icon" :style="{ background: `linear-gradient(135deg, ${method.color}20 0%, ${method.color}10 100%)`, color: method.color }">
            <el-icon :size="40"><component :is="method.icon" /></el-icon>
          </div>
          <h3 class="method-title">{{ t(method.titleKey) }}</h3>
          <p class="method-desc">{{ t(method.descKey) }}</p>
          <div class="method-time">
            <el-icon><Clock /></el-icon>
            <span>{{ t(method.timeKey) }}</span>
          </div>
          <ul class="method-features">
            <li v-for="(feature, fIndex) in method.features" :key="fIndex">
              <el-icon><CircleCheck /></el-icon>
              <span>{{ t(feature) }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="alt-section">
      <div class="container section">
        <h2 class="section-title text-center">{{ t('shipping.shippingTime') }}</h2>
        <p class="section-subtitle text-center">{{ t('shipping.shippingTimeSubtitle') }}</p>
        <div class="time-table">
          <div
            v-for="(item, index) in shippingTime"
            :key="index"
            class="time-row"
          >
            <span class="region">{{ t(item.regionKey) }}</span>
            <span class="time">{{ t(item.timeKey) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="container section">
      <h2 class="section-title text-center">{{ t('shipping.shippingCost') }}</h2>
      <p class="section-subtitle text-center">{{ t('shipping.shippingCostSubtitle') }}</p>
      <div class="cost-info">
        <div class="cost-card">
          <div class="cost-icon">
            <el-icon :size="36"><Money /></el-icon>
          </div>
          <h3>{{ t('shipping.costFactors') }}</h3>
          <ul>
            <li>{{ t('shipping.costFactor1') }}</li>
            <li>{{ t('shipping.costFactor2') }}</li>
            <li>{{ t('shipping.costFactor3') }}</li>
            <li>{{ t('shipping.costFactor4') }}</li>
          </ul>
        </div>
        <div class="cost-card highlight">
          <div class="cost-icon">
            <el-icon :size="36"><Van /></el-icon>
          </div>
          <h3>{{ t('shipping.freeShipping') }}</h3>
          <p class="free-shipping-desc">{{ t('shipping.freeShippingDesc') }}</p>
          <el-button type="primary" size="large" @click="$router.push('/inquiry')">
            {{ t('inquiry.title') }}
          </el-button>
        </div>
      </div>
    </div>

    <div class="alt-section">
      <div class="container section">
        <h2 class="section-title text-center">{{ t('shipping.packaging') }}</h2>
        <p class="section-subtitle text-center">{{ t('shipping.packagingSubtitle') }}</p>
        <div class="packaging-grid">
          <div
            v-for="(pack, index) in packagingInfo"
            :key="index"
            class="packaging-card"
          >
            <div class="pack-icon">
              <el-icon :size="36"><Box /></el-icon>
            </div>
            <h3>{{ t(pack.titleKey) }}</h3>
            <p>{{ t(pack.descKey) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container section">
      <h2 class="section-title text-center">{{ t('shipping.notes') }}</h2>
      <p class="section-subtitle text-center">{{ t('shipping.notesSubtitle') }}</p>
      <div class="notes-list">
        <div
          v-for="(note, index) in notes"
          :key="index"
          class="note-item"
        >
          <div class="note-icon">
            <el-icon><Warning /></el-icon>
          </div>
          <div class="note-content">
            <span class="note-number">{{ index + 1 }}</span>
            <p>{{ t(note) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="shippingContent" class="custom-shipping-section">
      <div class="container section">
        <div class="card">
          <h2 class="section-title">{{ t('shipping.moreInfo') }}</h2>
          <div v-html="shippingContent"></div>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <div class="container">
        <div class="cta-box">
          <h3>{{ t('shipping.needQuote') }}</h3>
          <p>{{ t('shipping.needQuoteDesc') }}</p>
          <el-button type="primary" size="large" @click="$router.push('/contact')">
            {{ t('contact.title') }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.shipping-page {
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

.alt-section {
  background: #f8f9fa;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;

  &.text-center {
    text-align: center;
  }
}

.section-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0 0 40px 0;

  &.text-center {
    text-align: center;
  }
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.method-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  }
}

.method-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.method-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.method-desc {
  font-size: 14px;
  color: #666;
  margin: 0 0 16px 0;
  line-height: 1.6;
}

.method-time {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f0f7ff;
  color: #1a73e8;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 20px;
}

.method-features {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;

  li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 10px;
    font-size: 14px;
    color: #555;

    &:last-child {
      margin-bottom: 0;
    }

    .el-icon {
      color: #34a853;
      flex-shrink: 0;
      margin-top: 2px;
    }
  }
}

.time-table {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.time-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
}

.region {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.time {
  font-size: 15px;
  color: #1a73e8;
  font-weight: 500;
}

.cost-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.cost-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);

  &.highlight {
    background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
  }

  h3 {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 16px 0 16px 0;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      font-size: 14px;
      color: #555;
      padding: 8px 0;
      padding-left: 20px;
      position: relative;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 14px;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #1a73e8;
      }
    }
  }
}

.cost-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
  color: #1a73e8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.free-shipping-desc {
  font-size: 14px;
  color: #555;
  line-height: 1.6;
  margin: 0 0 20px 0;
}

.packaging-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.packaging-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }

  .pack-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: linear-gradient(135deg, #fef3e2 0%, #fce4c4 100%);
    color: #fbbc05;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
  }

  h3 {
    font-size: 18px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0 0 12px 0;
  }

  p {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
    margin: 0;
  }
}

.notes-list {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.note-item {
  display: flex;
  gap: 16px;
  background: #fff;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.note-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #fff4e5;
  color: #f59e0b;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.note-content {
  flex: 1;
  display: flex;
  gap: 12px;
  align-items: flex-start;

  p {
    flex: 1;
    font-size: 14px;
    color: #555;
    line-height: 1.6;
    margin: 0;
  }
}

.note-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1a73e8;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.custom-shipping-section {
  .card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    padding: 32px;

    :deep(p) {
      margin: 0 0 12px 0;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.cta-section {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  padding: 60px 0;
  text-align: center;
  color: #fff;

  .cta-box {
    max-width: 600px;
    margin: 0 auto;

    h3 {
      font-size: 28px;
      font-weight: 600;
      margin: 0 0 12px 0;
    }

    p {
      font-size: 16px;
      opacity: 0.9;
      margin: 0 0 24px 0;
    }

    .el-button {
      background: #fff;
      color: #1a73e8;
      border: none;
      font-weight: 600;
      padding: 0 32px;
      height: 48px;
      font-size: 16px;
      border-radius: 8px;

      &:hover {
        background: #f0f0f0;
        color: #0d47a1;
      }
    }
  }
}

@media (max-width: 992px) {
  .methods-grid,
  .packaging-grid {
    grid-template-columns: 1fr;
  }

  .cost-info {
    grid-template-columns: 1fr;
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

  .section-title {
    font-size: 24px;
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

  .method-card,
  .packaging-card,
  .cost-card {
    padding: 24px;
  }

  .time-row {
    padding: 14px 16px;
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .note-item {
    padding: 16px;
  }

  .custom-shipping-section .card {
    padding: 24px;
  }
}
</style>
