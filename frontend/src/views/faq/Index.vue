<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLangStore } from '@/store/lang'
import { siteConfigApi } from '@/api'
import { QuestionFilled, HelpFilled, CreditCard, Van } from '@element-plus/icons-vue'
import type { SiteConfig } from '@/types'

const { t } = useI18n()
const langStore = useLangStore()
const siteConfig = ref<SiteConfig | null>(null)
const activeNames = ref<string[]>(['1'])

const faqContent = computed(() => {
  if (!siteConfig.value) return ''
  return langStore.lang === 'zh'
    ? siteConfig.value.faq_zh || siteConfig.value.faq_en
    : siteConfig.value.faq_en || siteConfig.value.faq_zh
})

const faqCategories = computed(() => [
  {
    key: 'general',
    titleKey: 'faq.generalQuestions',
    icon: QuestionFilled,
    color: '#1a73e8',
    items: [
      { qKey: 'faq.generalQ1', aKey: 'faq.generalA1' },
      { qKey: 'faq.generalQ2', aKey: 'faq.generalA2' },
      { qKey: 'faq.generalQ3', aKey: 'faq.generalA3' },
      { qKey: 'faq.generalQ4', aKey: 'faq.generalA4' }
    ]
  },
  {
    key: 'order',
    titleKey: 'faq.orderQuestions',
    icon: HelpFilled,
    color: '#34a853',
    items: [
      { qKey: 'faq.orderQ1', aKey: 'faq.orderA1' },
      { qKey: 'faq.orderQ2', aKey: 'faq.orderA2' },
      { qKey: 'faq.orderQ3', aKey: 'faq.orderA3' },
      { qKey: 'faq.orderQ4', aKey: 'faq.orderA4' }
    ]
  },
  {
    key: 'payment',
    titleKey: 'faq.paymentQuestions',
    icon: CreditCard,
    color: '#fbbc05',
    items: [
      { qKey: 'faq.paymentQ1', aKey: 'faq.paymentA1' },
      { qKey: 'faq.paymentQ2', aKey: 'faq.paymentA2' },
      { qKey: 'faq.paymentQ3', aKey: 'faq.paymentA3' }
    ]
  },
  {
    key: 'shipping',
    titleKey: 'faq.shippingQuestions',
    icon: Van,
    color: '#ea4335',
    items: [
      { qKey: 'faq.shippingQ1', aKey: 'faq.shippingA1' },
      { qKey: 'faq.shippingQ2', aKey: 'faq.shippingA2' },
      { qKey: 'faq.shippingQ3', aKey: 'faq.shippingA3' },
      { qKey: 'faq.shippingQ4', aKey: 'faq.shippingA4' }
    ]
  }
])

onMounted(async () => {
  try {
    const res = await siteConfigApi.get()
    siteConfig.value = res.data
  } catch (e) {
    console.error('Failed to load site config')
  }
})

function handleChange(val: string | string[]) {
  console.log(val)
}
</script>

<template>
  <div class="faq-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('faq.title') }}</h1>
        <p class="page-subtitle">{{ t('faq.subtitle') }}</p>
      </div>
    </div>

    <div class="container section">
      <div class="faq-categories">
        <div
          v-for="(category, catIndex) in faqCategories"
          :key="category.key"
          class="faq-category"
        >
          <div class="category-header">
            <div class="category-icon" :style="{ background: `linear-gradient(135deg, ${category.color}20 0%, ${category.color}10 100%)`, color: category.color }">
              <el-icon :size="28"><component :is="category.icon" /></el-icon>
            </div>
            <h2 class="category-title">{{ t(category.titleKey) }}</h2>
          </div>

          <el-collapse v-model="activeNames" @change="handleChange" class="faq-collapse">
            <el-collapse-item
              v-for="(item, itemIndex) in category.items"
              :key="`${category.key}-${itemIndex}`"
              :name="`${catIndex}-${itemIndex}`"
            >
              <template #title>
                <div class="collapse-title">
                  <span class="question-text">{{ t(item.qKey) }}</span>
                </div>
              </template>
              <div class="answer-content">
                <p>{{ t(item.aKey) }}</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>

      <div v-if="faqContent" class="faq-custom-content">
        <div class="card">
          <h2 class="section-title">{{ t('faq.moreQuestions') }}</h2>
          <div v-html="faqContent"></div>
        </div>
      </div>

      <div class="faq-contact">
        <div class="contact-box">
          <h3>{{ t('faq.stillHaveQuestions') }}</h3>
          <p>{{ t('faq.contactUsDesc') }}</p>
          <el-button type="primary" size="large" @click="$router.push('/contact')">
            {{ t('contact.title') }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.faq-page {
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

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 24px 0;
}

.faq-categories {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.faq-category {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.category-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 32px;
  border-bottom: 1px solid #f0f0f0;
}

.category-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.category-title {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.faq-collapse {
  --el-collapse-border-color: transparent;

  :deep(.el-collapse-item) {
    border-bottom: 1px solid #f5f5f5;

    &:last-child {
      border-bottom: none;
    }
  }

  :deep(.el-collapse-item__header) {
    padding: 20px 32px;
    font-size: 15px;
    font-weight: 500;
    color: #333;
    transition: all 0.3s ease;

    &:hover {
      background: #f8f9fa;
    }
  }

  :deep(.el-collapse-item__wrap) {
    background: #fafafa;
  }

  :deep(.el-collapse-item__content) {
    padding: 20px 32px;
    padding-bottom: 24px;
  }
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.question-text {
  font-size: 15px;
  font-weight: 500;
}

.answer-content {
  font-size: 14px;
  line-height: 1.8;
  color: #666;

  p {
    margin: 0;
  }
}

.faq-custom-content {
  margin-top: 40px;

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

.faq-contact {
  margin-top: 40px;
  display: flex;
  justify-content: center;
}

.contact-box {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  color: #fff;
  max-width: 600px;
  width: 100%;

  h3 {
    font-size: 24px;
    font-weight: 600;
    margin: 0 0 12px 0;
  }

  p {
    font-size: 15px;
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

@media (max-width: 768px) {
  .page-header {
    padding: 40px 0;

    .page-title {
      font-size: 28px;
    }
  }

  .section {
    padding: 40px 0;
  }

  .category-header {
    padding: 24px;
  }

  .category-title {
    font-size: 20px;
  }

  .faq-collapse :deep(.el-collapse-item__header) {
    padding: 16px 24px;
    font-size: 14px;
  }

  .faq-collapse :deep(.el-collapse-item__content) {
    padding: 16px 24px;
    padding-bottom: 20px;
  }

  .contact-box {
    padding: 32px 24px;

    h3 {
      font-size: 20px;
    }

    p {
      font-size: 14px;
    }
  }

  .faq-custom-content .card {
    padding: 24px;
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

  .category-header {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
}
</style>
