<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElCarousel, ElCarouselItem, ElButton } from 'element-plus'
import { Picture, ChatDotRound, ArrowRight, OfficeBuilding, Document } from '@element-plus/icons-vue'
import { bannerApi, siteConfigApi, categoryApi, productApi, newsApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'
import { useLangStore } from '@/store/lang'
import { useCurrencyStore } from '@/store/currency'
import { getI18nValue } from '@/utils/i18n'
import type { Banner, SiteConfig, Category, Product, News } from '@/types'

const { t } = useI18n()
const router = useRouter()
const langStore = useLangStore()
const currencyStore = useCurrencyStore()

const banners = ref<Banner[]>([])
const siteConfig = ref<SiteConfig | null>(null)
const categories = ref<Category[]>([])
const hotProducts = ref<Product[]>([])
const latestNews = ref<News[]>([])
const loading = ref(true)

const getBannerTitle = (banner: Banner) => {
  if (banner.title) return banner.title
  return langStore.lang === 'zh'
    ? (banner as any).title_zh || (banner as any).title_en
    : (banner as any).title_en || (banner as any).title_zh
}

const getBannerImage = (banner: Banner) => {
  return (banner as any).image || (banner as any).image_url
}

const getBannerButtonText = (banner: Banner) => {
  if ((banner as any).button_text) return (banner as any).button_text
  return ''
}

const getBannerLink = (banner: Banner) => {
  return (banner as any).link || (banner as any).link_url || ''
}

const getCategoryName = (category: Category) => {
  if ((category as any).name) return (category as any).name
  return langStore.lang === 'zh'
    ? category.name_zh || category.name_en
    : category.name_en || category.name_zh
}

const getAboutUs = computed(() => {
  if (!siteConfig.value) return ''
  return getI18nValue(siteConfig.value.about_us)
})

const getNewsTitle = (news: News) => getI18nValue(news.title)

const getNewsSummary = (news: News) => {
  const content = getI18nValue(news.content)
  const text = content.replace(/<[^>]+>/g, '').trim()
  return text.length > 80 ? text.slice(0, 80) + '...' : text
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const factoryImages = [
  {
    url: new URL('@/assets/images/product_line.jpg', import.meta.url).href,
    title: 'Production Line'
  },
  {
    url: new URL('@/assets/images/warehouse.jpg', import.meta.url).href,
    title: 'Warehouse'
  },
  {
    url: new URL('@/assets/images/quality_control.jpg', import.meta.url).href,
    title: 'Quality Control'
  }
]

async function loadData() {
  try {
    const [bannerRes, configRes, categoryRes, productRes, newsRes] = await Promise.all([
      bannerApi.list(),
      siteConfigApi.get(),
      categoryApi.list(),
      productApi.hot(),
      newsApi.list({ page: 1, page_size: 5 })
    ])
    banners.value = bannerRes.data || []
    siteConfig.value = configRes.data || null
    categories.value = (categoryRes.data || []).slice(0, 8)
    hotProducts.value = (productRes.data || []).slice(0, 4)
    latestNews.value = newsRes.data?.items || []
  } catch (error) {
    console.error('Failed to load home data:', error)
  } finally {
    loading.value = false
  }
}

function goToCategory(categoryId: number) {
  router.push(`/products?category=${categoryId}`)
}

function handleBannerClick(banner: Banner) {
  const link = getBannerLink(banner)
  if (link) {
    if (link.startsWith('http')) {
      window.open(link, '_blank')
    } else {
      router.push(link)
    }
  }
}

function goToNews() {
  router.push('/news')
}

function goToNewsDetail(id: number) {
  router.push(`/news/${id}`)
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="home-page">
    <section class="banner-section">
      <el-carousel
        v-if="banners.length > 0"
        :interval="4000"
        height="500px"
        arrow="hover"
        indicator-position="outside"
      >
        <el-carousel-item v-for="banner in banners" :key="banner.id">
          <div class="banner-item">
            <img :src="getBannerImage(banner)" :alt="getBannerTitle(banner)" class="banner-image" />
            <div class="banner-overlay">
              <div class="banner-content">
                <h1 class="banner-title">{{ getBannerTitle(banner) }}</h1>
                <div class="banner-actions">
                  <el-button
                    v-if="getBannerButtonText(banner) && getBannerLink(banner)"
                    type="primary"
                    size="large"
                    @click="handleBannerClick(banner)"
                  >
                    {{ getBannerButtonText(banner) }}
                    <el-icon class="el-icon--right"><ArrowRight /></el-icon>
                  </el-button>
                  <el-button size="large" @click="router.push('/inquiry')">
                    {{ t('nav.inquiry') }}
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>

    <section class="section about-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">{{ t('home.aboutTitle') }}</h2>
          <p class="section-subtitle">{{ t('home.aboutSubtitle') }}</p>
        </div>
        <div class="about-content">
          <div class="about-text">
            <p v-html="getAboutUs || t('home.aboutDesc')"></p>
            <el-button type="primary" @click="router.push('/about')">
              {{ t('common.readMore') }}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </div>
          <div class="about-stats">
            <div class="stat-card">
              <div class="stat-number">15+</div>
              <div class="stat-label">{{ t('home.years') }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">50+</div>
              <div class="stat-label">{{ t('home.countries') }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">500+</div>
              <div class="stat-label">{{ t('home.products') }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-number">1000+</div>
              <div class="stat-label">{{ t('home.clients') }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section categories-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">{{ t('home.categoriesTitle') }}</h2>
          <p class="section-subtitle">{{ t('home.categoriesSubtitle') }}</p>
        </div>
        <div class="categories-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-card"
            @click="goToCategory(category.id)"
          >
            <div class="category-image">
              <img v-if="category.image" :src="category.image" :alt="getCategoryName(category)" />
              <div v-else class="category-placeholder">
                <el-icon><Picture /></el-icon>
              </div>
            </div>
            <div class="category-info">
              <h3>{{ getCategoryName(category) }}</h3>
              <span class="view-more">{{ t('common.viewMore') }} →</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section hot-products-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">{{ t('home.hotTitle') }}</h2>
          <p class="section-subtitle">{{ t('home.hotSubtitle') }}</p>
        </div>
        <div class="products-grid">
          <ProductCard
            v-for="product in hotProducts"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="view-all-wrapper">
          <el-button type="primary" size="large" @click="router.push('/products')">
            {{ t('home.viewAllProducts') }}
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </section>

    <section class="section news-section" v-if="latestNews.length > 0">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon class="title-icon"><Document /></el-icon>
            {{ t('home.newsTitle') }}
          </h2>
          <p class="section-subtitle">{{ t('home.newsSubtitle') }}</p>
        </div>
        <div class="news-grid">
          <div
            v-for="news in latestNews"
            :key="news.id"
            class="news-card"
            @click="goToNewsDetail(news.id)"
          >
            <div class="news-cover">
              <img
                v-if="news.cover_image"
                :src="news.cover_image"
                :alt="getNewsTitle(news)"
              />
              <div v-else class="news-cover-placeholder">
                <el-icon :size="32"><Document /></el-icon>
              </div>
            </div>
            <div class="news-body">
              <div class="news-date">{{ formatDate(news.created_at) }}</div>
              <h3 class="news-title">{{ getNewsTitle(news) }}</h3>
              <p class="news-summary">{{ getNewsSummary(news) }}</p>
            </div>
          </div>
        </div>
        <div class="view-all-wrapper">
          <el-button type="primary" size="large" @click="goToNews">
            {{ t('home.viewAllNews') }}
            <el-icon class="el-icon--right"><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </section>

    <section class="section factory-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <el-icon class="title-icon"><OfficeBuilding /></el-icon>
            {{ t('home.factoryTitle') }}
          </h2>
          <p class="section-subtitle">{{ t('home.factorySubtitle') }}</p>
        </div>
        <div class="factory-grid">
          <div v-for="(img, index) in factoryImages" :key="index" class="factory-card">
            <img :src="img.url" :alt="img.title" class="factory-image" />
            <div class="factory-overlay">
              <span>{{ t('home.factory' + (index + 1)) || img.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>{{ t('home.inquiryTitle') }}</h2>
          <p>{{ t('home.inquirySubtitle') }}</p>
          <el-button type="primary" size="large" @click="router.push('/inquiry')">
            <el-icon><ChatDotRound /></el-icon>
            {{ t('nav.inquiry') }}
          </el-button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.home-page {
  .banner-section {
    .banner-item {
      position: relative;
      width: 100%;
      height: 100%;

      .banner-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .banner-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: transparent;
        display: flex;
        align-items: center;
        justify-content: center;

        .banner-content {
          text-align: center;
          color: #fff;
          max-width: 800px;
          padding: 0 20px;

          .banner-title {
            font-size: 48px;
            font-weight: 700;
            margin: 0 0 16px;
            line-height: 1.2;
            color: #fff;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
          }

          .banner-subtitle {
            font-size: 20px;
            margin: 0 0 32px;
            opacity: 0.95;
          }

          .banner-actions {
            display: flex;
            gap: 16px;
            justify-content: center;

            .el-button {
              padding: 14px 32px;
              font-size: 16px;
              border-radius: 8px;

              &:not(.el-button--primary) {
                background: rgba(255, 255, 255, 0.2);
                color: #fff;
                border-color: rgba(255, 255, 255, 0.5);
                backdrop-filter: blur(10px);

                &:hover {
                  background: rgba(255, 255, 255, 0.3);
                }
              }
            }
          }
        }
      }
    }
  }

  .section {
    padding: 80px 0;

    &.about-section {
      background: #fff;
    }

    &.categories-section {
      background: #f8fafd;
    }

    &.hot-products-section {
      background: #fff;
    }

    &.news-section {
      background: #f0f7ff;
    }

    &.factory-section {
      background: #f8fafd;
    }

    .section-header {
      text-align: center;
      margin-bottom: 50px;

      .section-title {
        font-size: 36px;
        font-weight: 700;
        color: #222;
        margin: 0 0 24px;

        .title-icon {
          color: #1a73e8;
          margin-right: 8px;
          vertical-align: middle;
        }
      }

      .section-subtitle {
        font-size: 16px;
        color: #666;
        margin: 0;
      }
    }
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .about-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    align-items: center;

    .about-text {
      p {
        font-size: 16px;
        line-height: 1.8;
        color: #555;
        margin-bottom: 24px;
      }
    }

    .about-stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;

      .stat-card {
        background: #fff;
        border: 1px solid #e8ecf1;
        border-radius: 12px;
        padding: 30px 20px;
        text-align: center;
        transition: all 0.3s ease;

        &:hover {
          transform: translateY(-4px);
          box-shadow: 0 8px 24px rgba(26, 115, 232, 0.12);
          border-color: #1a73e8;
        }

        .stat-number {
          font-size: 42px;
          font-weight: 700;
          color: #1a73e8;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 14px;
          color: #666;
        }
      }
    }
  }

  .categories-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;

    .category-card {
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

      &:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(26, 115, 232, 0.15);

        .category-image {
          img {
            transform: scale(1.1);
          }
        }

        .view-more {
          color: #1a73e8;
        }
      }

      .category-image {
        height: 160px;
        overflow: hidden;
        background: #f0f7ff;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.4s ease;
        }

        .category-placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #b3d4ff;
          font-size: 48px;
        }
      }

      .category-info {
        padding: 18px;

        h3 {
          font-size: 16px;
          font-weight: 600;
          color: #222;
          margin: 0 0 8px;
        }

        .view-more {
          font-size: 13px;
          color: #888;
          transition: color 0.2s ease;
        }
      }
    }
  }

  .news-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin-bottom: 40px;
  }

  .news-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(26, 115, 232, 0.15);

      .news-cover img {
        transform: scale(1.05);
      }

      .news-title {
        color: #1a73e8;
      }
    }
  }

  .news-cover {
    height: 120px;
    overflow: hidden;
    background: #e8f4ff;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }

    .news-cover-placeholder {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #b3d4ff;
    }
  }

  .news-body {
    padding: 14px 16px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .news-date {
    font-size: 11px;
    color: #888;
    margin-bottom: 6px;
  }

  .news-title {
    font-size: 14px;
    font-weight: 600;
    color: #222;
    margin: 0 0 8px;
    line-height: 1.4;
    transition: color 0.2s ease;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .news-summary {
    font-size: 12px;
    color: #666;
    line-height: 1.6;
    margin: 0;
    flex: 1;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .products-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    margin-bottom: 40px;
  }

  .view-all-wrapper {
    text-align: center;

    .el-button {
      padding: 14px 40px;
      font-size: 16px;
      border-radius: 8px;
    }
  }

  .factory-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;

    .factory-card {
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      aspect-ratio: 4 / 3;
      cursor: pointer;

      .factory-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
      }

      .factory-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px;
        background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
        color: #fff;
        font-size: 16px;
        font-weight: 500;
        transition: all 0.3s ease;
      }

      &:hover {
        .factory-image {
          transform: scale(1.08);
        }

        .factory-overlay {
          padding-bottom: 28px;
        }
      }
    }
  }

  .cta-section {
    background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
    padding: 80px 0;

    .cta-content {
      text-align: center;
      color: #fff;

      h2 {
        font-size: 36px;
        font-weight: 700;
        margin: 0 0 16px;
      }

      p {
        font-size: 18px;
        margin: 0 0 32px;
        opacity: 0.9;
      }

      .el-button {
        padding: 16px 48px;
        font-size: 18px;
        border-radius: 8px;
        background: #fff;
        color: #1a73e8;
        border: none;

        &:hover {
          background: #f0f7ff;
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        }
      }
    }
  }
}

@media (max-width: 1024px) {
  .home-page {
    .section {
      padding: 60px 0;

      .section-header {
        .section-title {
          font-size: 28px;
        }
      }
    }

    .about-content {
      grid-template-columns: 1fr;
      gap: 40px;
    }

    .categories-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .news-grid {
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .products-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .factory-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
}

@media (max-width: 768px) {
  .home-page {
    .banner-section {
      :deep(.el-carousel) {
        height: 350px !important;
      }

      .banner-item {
        .banner-overlay {
          .banner-content {
            .banner-title {
              font-size: 28px;
            }

            .banner-subtitle {
              font-size: 16px;
            }

            .banner-actions {
              flex-direction: column;
              align-items: center;

              .el-button {
                width: 200px;
              }
            }
          }
        }
      }
    }

    .section {
      padding: 50px 0;

      .section-header {
        margin-bottom: 30px;

        .section-title {
          font-size: 24px;
        }

        .section-subtitle {
          font-size: 14px;
        }
      }
    }

    .about-stats {
      grid-template-columns: repeat(2, 1fr) !important;
    }

    .categories-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .news-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .products-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }

    .factory-grid {
      grid-template-columns: 1fr;
      gap: 16px;
    }

    .cta-section {
      padding: 50px 0;

      .cta-content {
        h2 {
          font-size: 26px;
        }

        p {
          font-size: 16px;
        }

        .el-button {
          padding: 14px 36px;
          font-size: 16px;
        }
      }
    }
  }
}

@media (max-width: 480px) {
  .home-page {
    .categories-grid {
      grid-template-columns: 1fr;
    }

    .products-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
