<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { getI18nValue } from '@/utils/i18n'
import { Picture, Box, ChatDotRound } from '@element-plus/icons-vue'

interface Product {
  id: number
  name_en?: string
  name_zh?: string
  name?: string
  name_i18n?: Record<string, string>
  model?: string  // 型号
  image?: string
  images?: string[]
  price?: number | string
  price_usd?: number | string
  price_cny?: number | string
  moq?: number | string
  category_id?: number
  sku?: string
  [key: string]: any
}

const props = defineProps<{
  product: Product
}>()

const router = useRouter()
const { t } = useI18n()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()

const productName = computed(() => {
  return getI18nValue(props.product.name_i18n || props.product.name)
})

const productImage = computed(() => {
  return props.product.image || (props.product.images && props.product.images[0]) || ''
})

const formattedPrice = computed(() => {
  const price = currencyStore.currency === 'USD'
    ? props.product.price_usd
    : props.product.price_cny
  if (!price && price !== 0) {
    return '-'
  }
  return currencyStore.format(price)
})

const moqText = computed(() => {
  if (!props.product.moq && props.product.moq !== 0) {
    return ''
  }
  return `${t('common.moq')}: ${props.product.moq}`
})

function goToDetail() {
  router.push(`/products/${props.product.id}`)
}
</script>

<template>
  <div class="product-card" @click="goToDetail">
    <div class="product-image-wrapper">
      <img
        v-if="productImage"
        :src="productImage"
        :alt="productName"
        class="product-image"
      />
      <div v-else class="product-image-placeholder">
        <el-icon><Picture /></el-icon>
      </div>
      <div class="product-overlay">
        <span class="view-detail">{{ t('common.details') }}</span>
      </div>
    </div>

    <div class="product-info">
      <h3 class="product-name ellipsis-2" :title="productName">
        {{ productName }}
      </h3>

      <div v-if="props.product.model" class="product-model">
        型号: {{ props.product.model }}
      </div>

      <div class="product-price">
        <span class="price-value">{{ formattedPrice }}</span>
      </div>

      <div v-if="moqText" class="product-moq">
        <el-icon><Box /></el-icon>
        <span>{{ moqText }}</span>
      </div>

      <button class="inquiry-btn" @click.stop="router.push(`/inquiry?product_id=${product.id}`)">
        <el-icon><ChatDotRound /></el-icon>
        <span>{{ t('nav.inquiry') }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.product-card {
  background: #fff;
  border: 1px solid #e4e7eb;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;

  &:hover {
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transform: translateY(-4px);
    border-color: #1a73e8;

    .product-image-wrapper {
      .product-image {
        transform: scale(1.05);
      }

      .product-overlay {
        opacity: 1;
      }
    }
  }

  .product-image-wrapper {
    position: relative;
    width: 100%;
    padding-top: 100%;
    overflow: hidden;
    background: #f5f7fa;

    .product-image {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }

    .product-image-placeholder {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ccc;
      font-size: 48px;
    }

    .product-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(26, 115, 232, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s ease;

      .view-detail {
        color: #fff;
        font-size: 14px;
        font-weight: 500;
        padding: 10px 24px;
        border: 2px solid #fff;
        border-radius: 30px;
        transition: all 0.3s ease;

        &:hover {
          background: #fff;
          color: #1a73e8;
        }
      }
    }
  }

  .product-info {
    padding: 16px;
    display: flex;
    flex-direction: column;
    flex: 1;

    .product-name {
      font-size: 15px;
      font-weight: 600;
      color: #222;
      margin: 0 0 12px;
      line-height: 1.4;
      min-height: 42px;
      transition: color 0.2s ease;
    }

    &:hover .product-name {
      color: #1a73e8;
    }

    .product-model {
      font-size: 13px;
      color: #888;
      margin-bottom: 8px;
    }

    .product-price {
      margin-bottom: 10px;

      .price-value {
        font-size: 20px;
        font-weight: 700;
        color: #1a73e8;
      }
    }

    .product-moq {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #888;
      margin-bottom: 14px;

      .el-icon {
        font-size: 14px;
      }
    }

    .inquiry-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
      padding: 10px;
      background: #f0f7ff;
      color: #1a73e8;
      border: 1px solid #b3d4ff;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: auto;

      &:hover {
        background: #1a73e8;
        color: #fff;
        border-color: #1a73e8;
      }

      .el-icon {
        font-size: 16px;
      }
    }
  }
}

@media (max-width: 600px) {
  .product-card {
    .product-info {
      padding: 12px;

      .product-name {
        font-size: 14px;
        min-height: 38px;
      }

      .product-price {
        .price-value {
          font-size: 18px;
        }
      }
    }
  }
}
</style>
