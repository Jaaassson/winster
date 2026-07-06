<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { siteConfigApi } from '@/api'
import { getI18nValue } from '@/utils/i18n'
import { Trophy, Medal, User, OfficeBuilding, Clock, TrendCharts, Star, Goods } from '@element-plus/icons-vue'
import type { SiteConfig } from '@/types'

const { t } = useI18n()
const siteConfig = ref<SiteConfig | null>(null)

const aboutContent = computed(() => {
  if (!siteConfig.value) return ''
  return getI18nValue(siteConfig.value.about_us)
})

const companyName = computed(() => {
  if (!siteConfig.value) return ''
  return getI18nValue(siteConfig.value.company_name) || getI18nValue(siteConfig.value.site_name)
})

const advantages = computed(() => [
  { icon: Trophy, titleKey: 'about.qualityTitle', descKey: 'about.qualityDesc' },
  { icon: Medal, titleKey: 'about.experienceTitle', descKey: 'about.experienceDesc' },
  { icon: TrendCharts, titleKey: 'about.innovationTitle', descKey: 'about.innovationDesc' },
  { icon: Star, titleKey: 'about.serviceTitle', descKey: 'about.serviceDesc' }
])

const timeline = computed(() => [
  { year: '2008', titleKey: 'about.timeline2008', descKey: 'about.timeline2008Desc' },
  { year: '2012', titleKey: 'about.timeline2012', descKey: 'about.timeline2012Desc' },
  { year: '2016', titleKey: 'about.timeline2016', descKey: 'about.timeline2016Desc' },
  { year: '2020', titleKey: 'about.timeline2020', descKey: 'about.timeline2020Desc' },
  { year: '2024', titleKey: 'about.timeline2024', descKey: 'about.timeline2024Desc' }
])

const teamMembers = computed(() => [
  { nameKey: 'about.team1Name', roleKey: 'about.team1Role', avatar: '' },
  { nameKey: 'about.team2Name', roleKey: 'about.team2Role', avatar: '' },
  { nameKey: 'about.team3Name', roleKey: 'about.team3Role', avatar: '' },
  { nameKey: 'about.team4Name', roleKey: 'about.team4Role', avatar: '' }
])

const factoryImages = [
  { url: new URL('@/assets/images/factory_1.jpg', import.meta.url).href, title: 'Factory 1' },
  { url: new URL('@/assets/images/factory_2.jpg', import.meta.url).href, title: 'Factory 2' },
  { url: new URL('@/assets/images/factory_3.jpg', import.meta.url).href, title: 'Factory 3' },
  { url: new URL('@/assets/images/factory_4.jpg', import.meta.url).href, title: 'Factory 4' }
]

const introImage = new URL('@/assets/images/factory.jpg', import.meta.url).href

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
  <div class="about-page">
    <div class="page-header">
      <div class="container">
        <h1 class="page-title">{{ t('about.title') }}</h1>
        <p class="page-subtitle">{{ t('about.subtitle') }}</p>
      </div>
    </div>

    <div class="container section">
      <div class="about-intro">
        <div class="intro-text">
          <h2 class="section-title">{{ t('about.companyProfile') }}</h2>
          <h3 class="company-name">{{ companyName }}</h3>
          <div class="about-content" v-html="aboutContent"></div>
        </div>
        <div class="intro-image">
          <img :src="introImage" alt="Factory" />
        </div>
      </div>
    </div>

    <div class="advantages-section">
      <div class="container section">
        <h2 class="section-title text-center">{{ t('about.ourAdvantages') }}</h2>
        <p class="section-subtitle text-center">{{ t('about.advantagesSubtitle') }}</p>
        <div class="advantages-grid">
          <div class="advantage-card" v-for="(item, index) in advantages" :key="index">
            <div class="advantage-icon">
              <el-icon :size="36"><component :is="item.icon" /></el-icon>
            </div>
            <h3 class="advantage-title">{{ t(item.titleKey) }}</h3>
            <p class="advantage-desc">{{ t(item.descKey) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container section">
      <h2 class="section-title text-center">{{ t('about.history') }}</h2>
      <p class="section-subtitle text-center">{{ t('about.historySubtitle') }}</p>
      <div class="timeline">
        <div class="timeline-item" v-for="(item, index) in timeline" :key="index" :class="{ 'even': index % 2 === 1 }">
          <div class="timeline-dot">
            <span class="year">{{ item.year }}</span>
          </div>
          <div class="timeline-content">
            <h3 class="timeline-title">{{ t(item.titleKey) }}</h3>
            <p class="timeline-desc">{{ t(item.descKey) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="team-section">
      <div class="container section">
        <h2 class="section-title text-center">{{ t('about.ourTeam') }}</h2>
        <p class="section-subtitle text-center">{{ t('about.teamSubtitle') }}</p>
        <div class="team-grid">
          <div class="team-card" v-for="(member, index) in teamMembers" :key="index">
            <div class="team-avatar">
              <el-icon :size="48"><User /></el-icon>
            </div>
            <h3 class="team-name">{{ t(member.nameKey) }}</h3>
            <p class="team-role">{{ t(member.roleKey) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container section">
      <h2 class="section-title text-center">{{ t('about.ourFactory') }}</h2>
      <p class="section-subtitle text-center">{{ t('about.factorySubtitle') }}</p>
      <div class="factory-gallery">
        <div class="gallery-item" v-for="(item, index) in factoryImages" :key="index">
          <img :src="item.url" :alt="item.title" />
          <div class="gallery-overlay">
            <span>{{ t('about.factory') }} {{ index + 1 }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.about-page {
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

.about-intro {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.intro-text {
  .company-name {
    font-size: 20px;
    color: #1a73e8;
    font-weight: 600;
    margin: 0 0 20px 0;
  }

  .about-content {
    font-size: 15px;
    line-height: 1.8;
    color: #555;

    :deep(p) {
      margin: 0 0 16px 0;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.intro-image {
  img {
    width: 100%;
    height: 360px;
    object-fit: cover;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.advantages-section {
  background: #f8f9fa;
}

.advantages-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.advantage-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.advantage-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e8f0fe 0%, #d2e3fc 100%);
  color: #1a73e8;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.advantage-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
}

.advantage-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.timeline {
  position: relative;
  max-width: 900px;
  margin: 0 auto;

  &::before {
    content: '';
    position: absolute;
    left: 50%;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #e0e0e0;
    transform: translateX(-50%);
  }
}

.timeline-item {
  position: relative;
  display: flex;
  justify-content: flex-end;
  padding-right: 50%;
  margin-bottom: 40px;

  &:last-child {
    margin-bottom: 0;
  }

  &.even {
    justify-content: flex-start;
    padding-right: 0;
    padding-left: 50%;

    .timeline-content {
      margin-left: 40px;
      margin-right: 0;
    }

    .timeline-dot {
      left: 50%;
      right: auto;
      transform: translateX(-50%);
    }
  }
}

.timeline-dot {
  position: absolute;
  right: 50%;
  top: 0;
  transform: translateX(50%);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;

  .year {
    font-size: 16px;
    font-weight: 600;
  }
}

.timeline-content {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-right: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  max-width: 360px;
}

.timeline-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.timeline-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.team-section {
  background: #f8f9fa;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.team-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.team-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.team-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.team-role {
  font-size: 14px;
  color: #1a73e8;
  margin: 0;
}

.factory-gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.gallery-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;

  img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
  }

  &:hover img {
    transform: scale(1.08);
  }
}

.gallery-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: #fff;
  padding: 20px 12px 12px;
  font-size: 14px;
  font-weight: 500;
  opacity: 0;
  transition: opacity 0.3s ease;

  .gallery-item:hover & {
    opacity: 1;
  }
}

@media (max-width: 992px) {
  .about-intro {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .intro-image img {
    height: 280px;
  }

  .advantages-grid,
  .team-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .factory-gallery {
    grid-template-columns: repeat(2, 1fr);
  }

  .timeline::before {
    left: 20px;
    transform: none;
  }

  .timeline-item {
    padding-right: 0;
    padding-left: 60px;
    justify-content: flex-start;

    .timeline-dot {
      right: auto;
      left: 0;
      transform: none;
      width: 40px;
      height: 40px;

      .year {
        font-size: 12px;
      }
    }

    .timeline-content {
      margin-right: 0;
      margin-left: 0;
      max-width: none;
    }

    &.even {
      padding-left: 60px;

      .timeline-dot {
        left: 0;
        transform: none;
      }

      .timeline-content {
        margin-left: 0;
      }
    }
  }
}

@media (max-width: 576px) {
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

  .advantages-grid,
  .team-grid,
  .factory-gallery {
    grid-template-columns: 1fr;
  }

  .gallery-item img {
    height: 240px;
  }
}
</style>
