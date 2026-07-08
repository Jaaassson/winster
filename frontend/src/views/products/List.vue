<script setup lang="ts">
import { ref, computed, onMounted, watch, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ElInput,
  ElButton,
  ElPagination,
  ElTree,
  ElIcon,
  ElDrawer,
  ElSelect,
  ElOption
} from 'element-plus'
import {
  Search,
  Menu,
  Grid,
  List as ListIcon,
  Filter,
  Sort,
  ArrowUp,
  ArrowDown,
  Picture
} from '@element-plus/icons-vue'
import { productApi, categoryApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { getI18nValue } from '@/utils/i18n'
import type { Product, Category, PaginatedData } from '@/types'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const total = ref(0)
const loading = ref(false)
const mobileDrawerVisible = ref(false)

const queryParams = reactive({
  page: 1,
  pageSize: 12,
  keyword: '',
  categoryId: '' as number | string | '',
  sortBy: 'default'
})

const viewMode = ref<'grid' | 'list'>('grid')

const getCategoryName = (category: Category) => {
  return getI18nValue((category as any).name_i18n || category.name)
}

const getProductName = (product: any) => {
  return getI18nValue(product.name_i18n || product.name)
}

const getProductDescription = (product: any) => {
  return getI18nValue(product.description_i18n || product.description)
}

const formatProductPrice = (product: any) => {
  const price = currencyStore.currency === 'USD'
    ? product.price_usd
    : product.price_cny
  if (!price && price !== 0) {
    return '-'
  }
  return currencyStore.format(price)
}

const getProductImage = (product: any) => {
  if (product.image) return product.image
  if (product.images && product.images.length > 0) return product.images[0]
  return ''
}

const getProductDescShort = (product: any) => {
  const desc = getProductDescription(product)
  if (!desc || typeof desc !== 'string') return ''
  return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
}

function buildTreeData(categories: any[]): any[] {
  return categories.map(cat => ({
    id: cat.id,
    label: getCategoryName(cat),
    children: cat.children && cat.children.length > 0 ? buildTreeData(cat.children) : []
  }))
}

const treeData = computed(() => {
  return buildTreeData(categories.value)
})

function getParentIds(categories: any[], targetId: number, parents: number[] = []): number[] {
  for (const cat of categories) {
    if (cat.id === targetId) {
      return parents
    }
    if (cat.children && cat.children.length > 0) {
      const result = getParentIds(cat.children, targetId, [...parents, cat.id])
      if (result.length > 0 || cat.children.some((c: any) => c.id === targetId)) {
        return [...parents, cat.id]
      }
    }
  }
  return []
}

const defaultExpandedKeys = computed(() => {
  if (queryParams.categoryId) {
    const catId = Number(queryParams.categoryId)
    const parentIds = getParentIds(categories.value, catId)
    return parentIds
  }
  return []
})

const currentNodeKey = computed(() => {
  return queryParams.categoryId ? Number(queryParams.categoryId) : null
})

const selectedCategoryName = computed(() => {
  if (!queryParams.categoryId) return t('common.all')
  const cat = categories.value.find(c => c.id === Number(queryParams.categoryId))
  return cat ? getCategoryName(cat) : t('common.all')
})

async function loadProducts() {
  loading.value = true
  try {
    const params: any = {
      page: queryParams.page,
      page_size: queryParams.pageSize
    }

    if (queryParams.keyword) {
      params.keyword = queryParams.keyword
    }
    if (queryParams.categoryId) {
      params.category_id = queryParams.categoryId
    }
    if (queryParams.sortBy === 'price_asc') {
      params.sort_by = 'price'
      params.order = 'asc'
    } else if (queryParams.sortBy === 'price_desc') {
      params.sort_by = 'price'
      params.order = 'desc'
    } else if (queryParams.sortBy === 'newest') {
      params.sort_by = 'created_at'
      params.order = 'desc'
    }

    const res = await productApi.list(params)
    products.value = res.data?.items || []
    total.value = res.data?.total || 0
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loading.value = false
  }
}

async function loadCategories() {
  try {
    const res = await categoryApi.list()
    categories.value = res.data || []
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

function handleNodeClick(data: any) {
  if (!data.children || data.children.length === 0) {
    queryParams.categoryId = data.id
    queryParams.page = 1
    mobileDrawerVisible.value = false
    loadProducts()
  }
}

function clearCategory() {
  queryParams.categoryId = ''
  queryParams.page = 1
  loadProducts()
}

function handleSearch() {
  queryParams.page = 1
  loadProducts()
}

function handleSortChange(value: string) {
  queryParams.sortBy = value
  queryParams.page = 1
  loadProducts()
}

function handlePageChange(page: number) {
  queryParams.page = page
  loadProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleSizeChange(size: number) {
  queryParams.pageSize = size
  queryParams.page = 1
  loadProducts()
}

function toggleViewMode(mode: 'grid' | 'list') {
  viewMode.value = mode
}

onMounted(async () => {
  await loadCategories()

  if (route.query.category) {
    queryParams.categoryId = route.query.category as string
  }
  if (route.query.keyword) {
    queryParams.keyword = route.query.keyword as string
  }

  loadProducts()
})

watch(() => route.query, (newQuery) => {
  if (newQuery.category !== undefined) {
    queryParams.categoryId = newQuery.category as string
  }
  if (newQuery.keyword !== undefined) {
    queryParams.keyword = newQuery.keyword as string
  }
  queryParams.page = 1
  loadProducts()
})
</script>

<template>
  <div class="products-list-page">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">{{ t('nav.products') }}</h1>
        <div class="breadcrumb">
          <span @click="router.push('/')">{{ t('nav.home') }}</span>
          <span class="separator">/</span>
          <span class="current">{{ t('nav.products') }}</span>
          <span v-if="queryParams.categoryId" class="separator">/</span>
          <span v-if="queryParams.categoryId" class="current">{{ selectedCategoryName }}</span>
        </div>
      </div>

      <div class="mobile-filter-bar">
        <el-button @click="mobileDrawerVisible = true">
          <el-icon><Filter /></el-icon>
          {{ t('common.filter') }}
        </el-button>
        <div class="mobile-category-name">
          {{ selectedCategoryName }}
        </div>
      </div>

      <div class="page-content">
        <aside class="sidebar">
          <div class="sidebar-section">
            <h3 class="sidebar-title">{{ t('common.categories') }}</h3>
            <div class="category-list">
              <div
                :class="['category-item', { active: !queryParams.categoryId }]"
                @click="clearCategory"
              >
                {{ t('common.all') }}
              </div>
              <el-tree
                :data="treeData"
                :props="{ label: 'label', children: 'children' }"
                :default-expanded-keys="defaultExpandedKeys"
                :current-node-key="currentNodeKey"
                node-key="id"
                highlight-current
                @node-click="handleNodeClick"
                :expand-on-click-node="true"
                class="category-tree"
              >
                <template #default="{ node, data }">
                  <span
                    :class="['tree-node-content', { active: queryParams.categoryId === data.id }]"
                  >
                    {{ node.label }}
                  </span>
                </template>
              </el-tree>
            </div>
          </div>
        </aside>

        <ElDrawer
          v-model="mobileDrawerVisible"
          :title="t('common.filter')"
          direction="ltr"
          size="80%"
        >
          <div class="mobile-sidebar">
            <h3 class="sidebar-title">{{ t('common.categories') }}</h3>
            <div class="category-list">
              <div
                :class="['category-item', { active: !queryParams.categoryId }]"
                @click="clearCategory"
              >
                {{ t('common.all') }}
              </div>
              <el-tree
                :data="treeData"
                :props="{ label: 'label', children: 'children' }"
                :default-expanded-keys="defaultExpandedKeys"
                :current-node-key="currentNodeKey"
                node-key="id"
                highlight-current
                @node-click="handleNodeClick"
                :expand-on-click-node="true"
                class="category-tree"
              >
                <template #default="{ node, data }">
                  <span
                    :class="['tree-node-content', { active: queryParams.categoryId === data.id }]"
                  >
                    {{ node.label }}
                  </span>
                </template>
              </el-tree>
            </div>
          </div>
        </ElDrawer>

        <main class="main-content">
          <div class="toolbar">
            <div class="toolbar-left">
              <div class="search-box">
                <el-input
                  v-model="queryParams.keyword"
                  :placeholder="t('common.search')"
                  @keyup.enter="handleSearch"
                  clearable
                >
                  <template #append>
                    <el-button @click="handleSearch">
                      <el-icon><Search /></el-icon>
                    </el-button>
                  </template>
                </el-input>
              </div>
            </div>
            <div class="toolbar-right">
              <div class="sort-wrapper">
                <el-icon class="sort-icon"><Sort /></el-icon>
                <el-select
                  v-model="queryParams.sortBy"
                  :placeholder="t('common.sortBy')"
                  @change="handleSortChange"
                  size="default"
                >
                  <el-option label="Default" value="default" />
                  <el-option :label="t('common.priceAsc')" value="price_asc" />
                  <el-option :label="t('common.priceDesc')" value="price_desc" />
                  <el-option :label="t('common.newest')" value="newest" />
                </el-select>
              </div>
              <div class="view-toggle">
                <button
                  :class="['view-btn', { active: viewMode === 'grid' }]"
                  @click="toggleViewMode('grid')"
                >
                  <el-icon><Grid /></el-icon>
                </button>
                <button
                  :class="['view-btn', { active: viewMode === 'list' }]"
                  @click="toggleViewMode('list')"
                >
                  <el-icon><ListIcon /></el-icon>
                </button>
              </div>
            </div>
          </div>

          <div class="result-info">
            {{ t('common.total', { count: total }) }}
          </div>

          <div v-loading="loading" class="products-container">
            <div v-if="products.length > 0">
              <div v-if="viewMode === 'grid'" class="products-grid">
                <ProductCard
                  v-for="product in products"
                  :key="product.id"
                  :product="product"
                />
              </div>

              <div v-else class="products-list">
                <div
                  v-for="product in products"
                  :key="product.id"
                  class="product-list-item"
                  @click="router.push(`/products/${product.id}`)"
                >
                  <div class="product-list-image">
                    <img
                      v-if="getProductImage(product)"
                      :src="getProductImage(product)"
                      :alt="getProductName(product)"
                    />
                    <div v-else class="product-image-placeholder">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </div>
                  <div class="product-list-info">
                    <h3 class="product-name">
                      {{ getProductName(product) }}
                    </h3>
                    <div class="product-price">
                      {{ formatProductPrice(product) }}
                    </div>
                    <div class="product-meta">
                      <span v-if="product.moq" class="meta-item">
                        MOQ: {{ product.moq }}
                      </span>
                      <span v-if="product.stock" class="meta-item">
                        Stock: {{ product.stock }}
                      </span>
                    </div>
                    <p class="product-desc">
                      {{ getProductDescShort(product) }}
                    </p>
                    <div class="product-actions">
                      <el-button type="primary" @click.stop="router.push(`/products/${product.id}`)">
                        {{ t('common.details') }}
                      </el-button>
                      <el-button @click.stop="router.push(`/inquiry?product_id=${product.id}`)">
                        {{ t('nav.inquiry') }}
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="!loading" class="empty-state">
              <el-icon class="empty-icon"><Search /></el-icon>
              <p>{{ t('common.noResults') }}</p>
            </div>
          </div>

          <div v-if="total > 0" class="pagination-wrapper">
            <el-pagination
              v-model:current-page="queryParams.page"
              v-model:page-size="queryParams.pageSize"
              :page-sizes="[12, 24, 48, 96]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @current-change="handlePageChange"
              @size-change="handleSizeChange"
            />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.products-list-page {
  padding: 40px 0;
  min-height: 60vh;

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .page-header {
    margin-bottom: 30px;

    .page-title {
      font-size: 32px;
      font-weight: 700;
      color: #222;
      margin: 0 0 10px;
    }

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

  .mobile-filter-bar {
    display: none;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding: 12px 16px;
    background: #f8fafd;
    border-radius: 8px;

    .mobile-category-name {
      font-size: 14px;
      color: #666;
      flex: 1;
    }
  }

  .page-content {
    display: flex;
    gap: 30px;
  }

  .sidebar {
    width: 260px;
    flex-shrink: 0;

    .sidebar-section {
      background: #fff;
      border: 1px solid #e8ecf1;
      border-radius: 12px;
      padding: 20px;
      position: sticky;
      top: 20px;

      .sidebar-title {
        font-size: 18px;
        font-weight: 600;
        color: #222;
        margin: 0 0 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #eee;
      }
    }

    .category-list {
      .category-item {
        padding: 10px 12px;
        cursor: pointer;
        border-radius: 6px;
        font-size: 15px;
        color: #444;
        transition: all 0.2s ease;
        margin-bottom: 4px;

        &:hover {
          background: #f0f7ff;
          color: #1a73e8;
        }

        &.active {
          background: #1a73e8;
          color: #fff;
        }
      }
    }

    .category-tree {
      background: transparent;
      margin-top: 8px;

      :deep(.el-tree-node__content) {
        height: 36px;
        border-radius: 6px;
        margin-bottom: 2px;

        &:hover {
          background-color: #f0f7ff;
        }
      }

      :deep(.el-tree-node.is-current > .el-tree-node__content) {
        background-color: #e8f0fe;
      }

      .tree-node-content {
        font-size: 14px;
        color: #444;
        padding: 4px 0;

        &.active {
          color: #1a73e8;
          font-weight: 500;
        }
      }
    }
  }

  .mobile-sidebar {
    .sidebar-title {
      font-size: 18px;
      font-weight: 600;
      color: #222;
      margin: 0 0 16px;
    }

    .category-list {
      .category-item {
        padding: 12px;
        cursor: pointer;
        border-radius: 6px;
        font-size: 15px;
        color: #444;
        transition: all 0.2s ease;
        margin-bottom: 4px;

        &:hover {
          background: #f0f7ff;
          color: #1a73e8;
        }

        &.active {
          background: #1a73e8;
          color: #fff;
        }
      }
    }

    .category-tree {
      margin-top: 8px;

      :deep(.el-tree-node__content) {
        height: 40px;
      }
    }
  }

  .main-content {
    flex: 1;
    min-width: 0;
  }

  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 16px 20px;
    background: #fff;
    border: 1px solid #e8ecf1;
    border-radius: 12px;
    flex-wrap: wrap;
    gap: 16px;

    .toolbar-left {
      .search-box {
        width: 320px;
      }
    }

    .toolbar-right {
      display: flex;
      align-items: center;
      gap: 20px;

      .sort-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;

        .sort-icon {
          font-size: 18px;
          color: #666;
        }
      }

      .view-toggle {
        display: flex;
        border: 1px solid #e8ecf1;
        border-radius: 6px;
        overflow: hidden;

        .view-btn {
          width: 36px;
          height: 36px;
          border: none;
          background: #fff;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #888;
          transition: all 0.2s ease;

          &:hover {
            color: #1a73e8;
            background: #f0f7ff;
          }

          &.active {
            background: #1a73e8;
            color: #fff;
          }
        }
      }
    }
  }

  .result-info {
    font-size: 14px;
    color: #888;
    margin-bottom: 16px;
  }

  .products-container {
    min-height: 400px;
  }

  .products-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }

  .products-list {
    display: flex;
    flex-direction: column;
    gap: 16px;

    .product-list-item {
      display: flex;
      background: #fff;
      border: 1px solid #e8ecf1;
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
        border-color: #1a73e8;
      }

      .product-list-image {
        width: 220px;
        height: 220px;
        flex-shrink: 0;
        background: #f5f7fa;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.3s ease;
        }

        .product-image-placeholder {
          color: #ccc;
          font-size: 48px;
        }
      }

      .product-list-info {
        padding: 20px;
        flex: 1;
        display: flex;
        flex-direction: column;

        .product-name {
          font-size: 18px;
          font-weight: 600;
          color: #222;
          margin: 0 0 10px;
        }

        .product-price {
          font-size: 24px;
          font-weight: 700;
          color: #1a73e8;
          margin-bottom: 10px;
        }

        .product-meta {
          display: flex;
          gap: 20px;
          margin-bottom: 12px;

          .meta-item {
            font-size: 13px;
            color: #888;
          }
        }

        .product-desc {
          font-size: 14px;
          color: #666;
          line-height: 1.6;
          margin: 0 0 16px;
          flex: 1;
        }

        .product-actions {
          display: flex;
          gap: 12px;
        }
      }
    }
  }

  .empty-state {
    text-align: center;
    padding: 80px 20px;

    .empty-icon {
      font-size: 64px;
      color: #ccc;
      margin-bottom: 16px;
    }

    p {
      font-size: 16px;
      color: #999;
      margin: 0;
    }
  }

  .pagination-wrapper {
    margin-top: 40px;
    display: flex;
    justify-content: center;
  }
}

@media (max-width: 1024px) {
  .products-list-page {
    .products-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
}

@media (max-width: 768px) {
  .products-list-page {
    padding: 20px 0;

    .page-header {
      .page-title {
        font-size: 24px;
      }
    }

    .mobile-filter-bar {
      display: flex;
    }

    .sidebar {
      display: none;
    }

    .toolbar {
      .toolbar-left {
        width: 100%;

        .search-box {
          width: 100%;
        }
      }

      .toolbar-right {
        width: 100%;
        justify-content: space-between;
      }
    }

    .products-grid {
      grid-template-columns: repeat(2, 1fr) !important;
      gap: 12px !important;
    }

    .products-list {
      .product-list-item {
        flex-direction: column;

        .product-list-image {
          width: 100%;
          height: 200px;
        }
      }
    }
  }
}

@media (max-width: 480px) {
  .products-list-page {
    .products-grid {
      grid-template-columns: 1fr !important;
    }
  }
}
</style>
