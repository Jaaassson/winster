<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ElButton,
  ElTable,
  ElTableColumn,
  ElDialog,
  ElTag,
  ElIcon,
  ElMessage
} from 'element-plus'
import {
  ArrowLeft,
  ShoppingCart,
  ChatDotRound,
  Box,
  PriceTag,
  Document,
  Star
} from '@element-plus/icons-vue'
import { productApi, categoryApi } from '@/api'
import ImageCarousel from '@/components/ImageCarousel.vue'
import InquiryForm from '@/components/InquiryForm.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { getI18nValue } from '@/utils/i18n'
import type { Product, Category } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()

const product = ref<Product | null>(null)
const relatedProducts = ref<Product[]>([])
const loading = ref(true)
const inquiryDialogVisible = ref(false)

const productName = computed(() => {
  if (!product.value) return ''
  return getI18nValue((product.value as any).name_i18n || product.value.name)
})

const productDescription = computed(() => {
  if (!product.value) return ''
  return getI18nValue((product.value as any).description_i18n || (product.value as any).description)
})

const productSpec = computed(() => {
  if (!product.value) return ''
  return getI18nValue((product.value as any).spec_i18n || (product.value as any).specifications)
})

const productPackage = computed(() => {
  if (!product.value) return ''
  return getI18nValue((product.value as any).packaging_i18n || (product.value as any).packaging)
})

const carouselImages = computed(() => {
  if (!product.value) return []
  const images: { url: string; alt: string }[] = []
  if (product.value.image) {
    images.push({ url: product.value.image, alt: productName.value })
  }
  if (product.value.images && Array.isArray(product.value.images)) {
    product.value.images.forEach((img: string, index: number) => {
      if (img && img !== product.value?.image) {
        images.push({ url: img, alt: `${productName.value} ${index + 1}` })
      }
    })
  }
  return images
})

const formattedPrice = computed(() => {
  if (!product.value) return '-'
  const price = currencyStore.currency === 'USD'
    ? (product.value as any).price_usd
    : (product.value as any).price_cny
  return currencyStore.format(price)
})

const specTableData = computed(() => {
  if (!productSpec.value) return []
  try {
    const lines = productSpec.value.split('\n').filter(line => line.trim())
    return lines.map(line => {
      const parts = line.split(/[:：]/)
      return {
        label: parts[0]?.trim() || '',
        value: parts.slice(1).join(':').trim() || ''
      }
    }).filter(item => item.label && item.value)
  } catch {
    return []
  }
})

async function loadProduct(id: number) {
  loading.value = true
  try {
    const res = await productApi.detail(id)
    product.value = res.data || null

    if (product.value?.category_id) {
      loadRelatedProducts(product.value.category_id, id)
    }
  } catch (error) {
    console.error('Failed to load product:', error)
  } finally {
    loading.value = false
  }
}

async function loadRelatedProducts(categoryId: number, currentProductId: number) {
  try {
    const res = await productApi.list({
      category_id: categoryId,
      page_size: 4
    })
    relatedProducts.value = (res.data?.items || []).filter(
      (p: Product) => p.id !== currentProductId
    ).slice(0, 4)
  } catch (error) {
    console.error('Failed to load related products:', error)
  }
}

function openInquiryDialog() {
  inquiryDialogVisible.value = true
}

function handleInquirySuccess() {
  inquiryDialogVisible.value = false
  ElMessage.success(t('common.success'))
}

function goBack() {
  router.back()
}

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    loadProduct(id)
  }
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    loadProduct(Number(newId))
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
})
</script>

<template>
  <div class="product-detail-page">
    <div class="container">
      <div class="breadcrumb-bar">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          {{ t('common.backToList') }}
        </el-button>
        <div class="breadcrumb">
          <span @click="router.push('/')">{{ t('nav.home') }}</span>
          <span class="separator">/</span>
          <span @click="router.push('/products')">{{ t('nav.products') }}</span>
          <span class="separator">/</span>
          <span class="current">{{ productName }}</span>
        </div>
      </div>

      <div v-loading="loading" class="detail-content" v-if="product">
        <div class="detail-main">
          <div class="images-section">
            <ImageCarousel
              :images="carouselImages"
              height="500px"
              :autoplay="false"
              rounded
            />
          </div>

          <div class="info-section">
            <div class="product-header">
              <h1 class="product-title">{{ productName }}</h1>
              <div v-if="product.is_hot" class="hot-badge">
                <el-icon><Star /></el-icon>
                {{ t('common.hot') }}
              </div>
            </div>

            <div class="product-price-section">
              <span class="price-label">{{ t('common.price') }}:</span>
              <span class="price-value">{{ formattedPrice }}</span>
            </div>

            <div class="product-meta">
              <div class="meta-item">
                <el-icon class="meta-icon"><PriceTag /></el-icon>
                <span class="meta-label">型号:</span>
                <span class="meta-value">{{ product.model || '-' }}</span>
              </div>
              <div class="meta-item">
                <el-icon class="meta-icon"><Box /></el-icon>
                <span class="meta-label">{{ t('common.stock') }}:</span>
                <span class="meta-value">
                  <el-tag v-if="product.stock && product.stock > 0" type="success" effect="light">
                    {{ product.stock }}
                  </el-tag>
                  <el-tag v-else type="danger" effect="light">
                    {{ t('common.outOfStock') }}
                  </el-tag>
                </span>
              </div>
              <div class="meta-item">
                <el-icon class="meta-icon"><Box /></el-icon>
                <span class="meta-label">{{ t('common.moq') }}:</span>
                <span class="meta-value">{{ product.moq || '-' }}</span>
              </div>
            </div>

            <div class="product-actions">
              <el-button type="primary" size="large" @click="openInquiryDialog">
                <el-icon><ChatDotRound /></el-icon>
                {{ t('nav.inquiry') }}
              </el-button>
              <el-button size="large" @click="router.push(`/inquiry?product_id=${product.id}`)">
                {{ t('common.sendInquiry') }}
              </el-button>
            </div>

            <div class="product-quick-info">
              <div class="quick-info-item">
                <el-icon><Document /></el-icon>
                <span>{{ t('common.qualityAssured') }}</span>
              </div>
              <div class="quick-info-item">
                <el-icon><Box /></el-icon>
                <span>{{ t('common.safePackaging') }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="detail-tabs">
          <div class="tabs-nav">
            <div class="tab-item active">
              {{ t('common.description') }}
            </div>
          </div>

          <div class="tabs-content">
            <div v-if="specTableData.length > 0" class="spec-section">
              <h3 class="section-title">
                <el-icon><Document /></el-icon>
                {{ t('common.specifications') }}
              </h3>
              <div class="spec-table-wrapper">
                <el-table :data="specTableData" border stripe style="width: 100%">
                  <el-table-column prop="label" :label="t('common.parameter')" width="200" />
                  <el-table-column prop="value" :label="t('common.value')" />
                </el-table>
              </div>
            </div>

            <div v-if="productDescription" class="description-section">
              <h3 class="section-title">
                <el-icon><Document /></el-icon>
                {{ t('common.description') }}
              </h3>
              <div class="description-content">
                <p v-html="productDescription"></p>
              </div>
            </div>

            <div v-if="productPackage" class="package-section">
              <h3 class="section-title">
                <el-icon><Box /></el-icon>
                {{ t('common.package') }}
              </h3>
              <div class="package-content">
                <p v-html="productPackage"></p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="relatedProducts.length > 0" class="related-products">
          <h2 class="section-title">
            <el-icon><Star /></el-icon>
            {{ t('common.relatedProducts') }}
          </h2>
          <div class="related-grid">
            <ProductCard
              v-for="item in relatedProducts"
              :key="item.id"
              :product="item"
            />
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <p>{{ t('common.productNotFound') }}</p>
        <el-button type="primary" @click="router.push('/products')">
          {{ t('nav.products') }}
        </el-button>
      </div>
    </div>

    <ElDialog
      v-model="inquiryDialogVisible"
      :title="t('nav.inquiry')"
      width="600px"
      :close-on-click-modal="false"
    >
      <InquiryForm
        :product-id="product?.id"
        :product-name="productName"
        @success="handleInquirySuccess"
      />
    </ElDialog>
  </div>
</template>

<style scoped lang="scss">
.product-detail-page {
  padding: 30px 0 60px;
  min-height: 60vh;

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .breadcrumb-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    flex-wrap: wrap;
    gap: 12px;

    .breadcrumb {
      font-size: 14px;
      color: #888;

      span {
        cursor: pointer;

        &:hover {
          color: #1a73e8;
        }
      }

      .separator {
        margin: 0 8px;
        color: #ccc;
        cursor: default;
      }

      .current {
        color: #333;
        cursor: default;
      }
    }
  }

  .detail-content {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e8ecf1;
    overflow: hidden;
  }

  .detail-main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    padding: 30px;
  }

  .images-section {
    :deep(.image-carousel) {
      border-radius: 12px;
    }
  }

  .info-section {
    display: flex;
    flex-direction: column;

    .product-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 20px;
      gap: 16px;

      .product-title {
        font-size: 28px;
        font-weight: 700;
        color: #222;
        margin: 0;
        line-height: 1.3;
        flex: 1;
      }

      .hot-badge {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 4px 12px;
        background: #fff7ed;
        color: #ea580c;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        flex-shrink: 0;

        .el-icon {
          font-size: 14px;
        }
      }
    }

    .product-price-section {
      display: flex;
      align-items: baseline;
      gap: 12px;
      padding: 20px;
      background: #f8fafd;
      border-radius: 10px;
      margin-bottom: 24px;

      .price-label {
        font-size: 15px;
        color: #666;
      }

      .price-value {
        font-size: 36px;
        font-weight: 700;
        color: #1a73e8;
      }
    }

    .product-meta {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 30px;

      .meta-item {
        display: flex;
        align-items: center;
        gap: 10px;

        .meta-icon {
          font-size: 18px;
          color: #1a73e8;
        }

        .meta-label {
          font-size: 14px;
          color: #666;
          width: 80px;
        }

        .meta-value {
          font-size: 15px;
          color: #333;
          font-weight: 500;
        }
      }
    }

    .product-actions {
      display: flex;
      gap: 16px;
      margin-bottom: 30px;

      .el-button {
        flex: 1;
        height: 48px;
        font-size: 16px;
        border-radius: 8px;
      }
    }

    .product-quick-info {
      display: flex;
      gap: 24px;
      padding-top: 20px;
      border-top: 1px solid #eee;

      .quick-info-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
        color: #555;

        .el-icon {
          color: #10b981;
          font-size: 18px;
        }
      }
    }
  }

  .detail-tabs {
    border-top: 1px solid #e8ecf1;

    .tabs-nav {
      display: flex;
      background: #f8fafd;
      border-bottom: 1px solid #e8ecf1;

      .tab-item {
        padding: 16px 30px;
        font-size: 16px;
        font-weight: 500;
        color: #666;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.2s ease;

        &.active {
          color: #1a73e8;
          background: #fff;
          border-bottom-color: #1a73e8;
        }
      }
    }

    .tabs-content {
      padding: 30px;

      .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #222;
        margin: 0 0 20px;
        text-align: left;

        &::after {
          margin-left: 0;
        }

        .el-icon {
          color: #1a73e8;
          margin-right: 8px;
          vertical-align: middle;
        }
      }

      .spec-section,
      .package-section,
      .description-section {
        margin-bottom: 40px;

        &:last-child {
          margin-bottom: 0;
        }
      }

      .spec-table-wrapper {
        :deep(.el-table) {
          border-radius: 8px;
          overflow: hidden;
        }
      }

      .package-content,
      .description-content {
        font-size: 15px;
        line-height: 1.8;
        color: #444;

        p {
          margin: 0 0 12px;

          &:last-child {
            margin-bottom: 0;
          }
        }

        ul, ol {
          margin: 12px 0;
          padding-left: 24px;
        }

        img {
          max-width: 100%;
          border-radius: 8px;
        }
      }
    }
  }

  .related-products {
    margin-top: 50px;

    .section-title {
      font-size: 24px;
      font-weight: 600;
      color: #222;
      margin: 0 0 24px;
      text-align: left;

      &::after {
        margin-left: 0;
      }

      .el-icon {
        color: #1a73e8;
        margin-right: 8px;
        vertical-align: middle;
      }
    }

    .related-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }
  }

  .empty-state {
    text-align: center;
    padding: 80px 20px;

    p {
      font-size: 16px;
      color: #888;
      margin-bottom: 20px;
    }
  }
}

@media (max-width: 1024px) {
  .product-detail-page {
    .detail-main {
      grid-template-columns: 1fr;
    }

    .related-grid {
      grid-template-columns: repeat(3, 1fr) !important;
    }
  }
}

@media (max-width: 768px) {
  .product-detail-page {
    padding: 20px 0 40px;

    .breadcrumb-bar {
      flex-direction: column;
      align-items: flex-start;
    }

    .detail-main {
      padding: 20px;
      gap: 24px;
    }

    .images-section {
      :deep(.image-carousel) {
        height: 350px !important;
      }
    }

    .info-section {
      .product-header {
        .product-title {
          font-size: 22px;
        }
      }

      .product-price-section {
        .price-value {
          font-size: 28px;
        }
      }

      .product-actions {
        flex-direction: column;

        .el-button {
          width: 100%;
        }
      }
    }

    .detail-tabs {
      .tabs-content {
        padding: 20px;
      }
    }

    .related-products {
      margin-top: 30px;

      .related-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 12px;
      }
    }
  }
}

@media (max-width: 480px) {
  .product-detail-page {
    .related-products {
      .related-grid {
        grid-template-columns: 1fr !important;
      }
    }
  }
}
</style>
