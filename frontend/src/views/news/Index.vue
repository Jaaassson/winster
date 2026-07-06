<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { newsApi } from '@/api'
import { getI18nValue } from '@/utils/i18n'
import { Picture } from '@element-plus/icons-vue'
import type { News } from '@/types'

const { t } = useI18n()
const router = useRouter()

const loading = ref(false)
const newsList = ref<News[]>([])
const pagination = reactive({
  page: 1,
  page_size: 9,
  total: 0
})

function getTitle(news: News) {
  return getI18nValue(news.title)
}

function getSummary(news: News) {
  const content = getI18nValue(news.content)
  // 去除 HTML 标签后截取摘要
  const text = content.replace(/<[^>]+>/g, '').trim()
  return text.length > 120 ? text.slice(0, 120) + '...' : text
}

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

async function loadNews() {
  loading.value = true
  try {
    const res = await newsApi.list({
      page: pagination.page,
      page_size: pagination.page_size
    })
    if (res.code === 200 || res.code === 0) {
      newsList.value = res.data.items || []
      pagination.total = res.data.total || 0
    }
  } catch (e) {
    console.error('Failed to load news:', e)
  } finally {
    loading.value = false
  }
}

function goToDetail(id: number) {
  router.push(`/news/${id}`)
}

function handlePageChange(page: number) {
  pagination.page = page
  loadNews()
}

onMounted(() => {
  loadNews()
})
</script>

<template>
  <div class="news-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('news.title') }}</h1>
        <p class="page-subtitle">{{ t('news.latestNews') }}</p>
      </div>
    </div>

    <div class="container section" v-loading="loading">
      <div v-if="newsList.length > 0" class="news-grid">
        <div
          v-for="news in newsList"
          :key="news.id"
          class="news-card"
          @click="goToDetail(news.id)"
        >
          <div class="news-image">
            <img
              v-if="news.cover_image"
              :src="news.cover_image"
              :alt="getTitle(news)"
            />
            <div v-else class="image-placeholder">
              <el-icon :size="48"><Picture /></el-icon>
            </div>
            <div class="news-date">
              <span class="day">{{ formatDate(news.created_at).slice(8) }}</span>
              <span class="year-month">{{ formatDate(news.created_at).slice(0, 7) }}</span>
            </div>
          </div>
          <div class="news-content">
            <h3 class="news-title">{{ getTitle(news) }}</h3>
            <p class="news-summary">{{ getSummary(news) }}</p>
            <div class="news-footer">
              <span class="read-more">{{ t('news.readMore') }} →</span>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-else-if="!loading" :description="t('news.title')" />

      <div v-if="pagination.total > pagination.page_size" class="pagination-wrapper">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="pagination.total"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.news-page {
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
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
    transform: translateY(-6px);
    box-shadow: 0 12px 28px rgba(26, 115, 232, 0.15);

    .news-image img {
      transform: scale(1.08);
    }

    .news-title {
      color: #1a73e8;
    }
  }
}

.news-image {
  position: relative;
  height: 220px;
  overflow: hidden;
  background: #f0f7ff;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
  }

  .image-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #b3d4ff;
  }

  .news-date {
    position: absolute;
    top: 0;
    left: 0;
    background: rgba(26, 115, 232, 0.9);
    color: #fff;
    padding: 10px 14px;
    border-radius: 0 0 8px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1.2;

    .day {
      font-size: 22px;
      font-weight: 700;
    }

    .year-month {
      font-size: 11px;
      opacity: 0.9;
    }
  }
}

.news-content {
  padding: 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.news-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.news-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin: 0 0 16px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-footer {
  .read-more {
    font-size: 13px;
    color: #1a73e8;
    font-weight: 500;
  }
}

.pagination-wrapper {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}

@media (max-width: 992px) {
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
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

  .news-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .news-image {
    height: 200px;
  }
}
</style>
