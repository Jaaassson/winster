<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { newsApi } from '@/api'
import { getI18nValue } from '@/utils/i18n'
import { ArrowLeft, Clock } from '@element-plus/icons-vue'
import type { News } from '@/types'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()

const loading = ref(false)
const news = ref<News | null>(null)

const title = computed(() => news.value ? getI18nValue(news.value.title) : '')
const content = computed(() => news.value ? getI18nValue(news.value.content) : '')

function formatDate(dateStr: string) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

async function loadDetail() {
  const id = Number(route.params.id)
  if (!id) {
    router.push('/news')
    return
  }
  loading.value = true
  try {
    const res = await newsApi.detail(id)
    if (res.code === 200 || res.code === 0) {
      news.value = res.data
    } else {
      router.push('/news')
    }
  } catch (e) {
    console.error('Failed to load news detail:', e)
    router.push('/news')
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.push('/news')
}

onMounted(() => {
  loadDetail()
})
</script>

<template>
  <div class="news-detail-page" v-loading="loading">
    <div v-if="news" class="news-detail">
      <div class="page-header">
        <div class="container">
          <h1 class="page-title">{{ title }}</h1>
          <div class="news-meta">
            <span class="meta-item">
              <el-icon><Clock /></el-icon>
              <span>{{ formatDate(news.created_at) }}</span>
            </span>
          </div>
        </div>
      </div>

      <div class="container section">
        <div v-if="news.cover_image" class="cover-wrapper">
          <img :src="news.cover_image" :alt="title" class="cover-image" />
        </div>

        <div class="article-content" v-html="content"></div>

        <div class="back-wrapper">
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            <span>{{ t('news.backToList') }}</span>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.news-detail-page {
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  color: #fff;
  padding: 60px 0;
  text-align: center;
  margin-bottom: 60px;

  .page-title {
    font-size: 32px;
    font-weight: 600;
    margin: 0 0 16px 0;
    line-height: 1.4;
  }

  .news-meta {
    display: flex;
    justify-content: center;

    .meta-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      opacity: 0.9;

      .el-icon {
        font-size: 16px;
      }
    }
  }
}

.section {
  padding: 60px 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.cover-wrapper {
  margin-bottom: 40px;

  .cover-image {
    width: 100%;
    max-height: 450px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }
}

.article-content {
  font-size: 16px;
  line-height: 1.9;
  color: #333;

  :deep(p) {
    margin: 0 0 20px 0;
  }

  :deep(h2) {
    font-size: 24px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 32px 0 16px 0;
  }

  :deep(h3) {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 28px 0 14px 0;
  }

  :deep(img) {
    max-width: 100%;
    border-radius: 8px;
    margin: 16px 0;
  }

  :deep(ul), :deep(ol) {
    margin: 0 0 20px 0;
    padding-left: 24px;

    li {
      margin-bottom: 8px;
    }
  }

  :deep(blockquote) {
    border-left: 4px solid #1a73e8;
    padding: 12px 20px;
    margin: 20px 0;
    background: #f8f9fa;
    color: #555;
    font-style: italic;
  }

  :deep(a) {
    color: #1a73e8;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}

.back-wrapper {
  margin-top: 60px;
  padding-top: 30px;
  border-top: 1px solid #eee;
  text-align: center;
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 0;
    margin-bottom: 40px;

    .page-title {
      font-size: 24px;
    }
  }

  .section {
    padding: 40px 0;
  }

  .cover-wrapper {
    margin-bottom: 24px;

    .cover-image {
      max-height: 240px;
    }
  }

  .article-content {
    font-size: 15px;
    line-height: 1.8;
  }
}
</style>
