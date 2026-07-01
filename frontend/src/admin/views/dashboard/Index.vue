<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { productApi, inquiryApi, categoryApi } from '@/admin/api'
import type { Product, Inquiry, Category, DashboardSummary } from '@/types'
import { formatDateTime } from '@/utils/date'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import type { EChartsOption } from 'echarts'
import {
  Goods,
  Message,
  ChatDotRound,
  Menu,
  View,
  Edit,
  Tools
} from '@element-plus/icons-vue'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const router = useRouter()

const loading = ref(false)
const summary = reactive<DashboardSummary>({
  total_products: 0,
  total_categories: 0,
  total_inquiries: 0,
  total_news: 0,
  pending_inquiries: 0,
  replied_inquiries: 0
})

const recentInquiries = ref<Inquiry[]>([])
const chartType = ref<'bar' | 'line'>('bar')
const salesChartData = ref<{ name: string; value: number }[]>([])
const trendChartData = ref<{ name: string; value: number }[]>([])

const statsCards = computed(() => [
  {
    title: '总产品数',
    value: summary.total_products,
    icon: Goods,
    color: '#409eff',
    bgColor: '#ecf5ff'
  },
  {
    title: '总询盘数',
    value: summary.total_inquiries,
    icon: Message,
    color: '#67c23a',
    bgColor: '#f0f9eb'
  },
  {
    title: '未读询盘',
    value: summary.pending_inquiries,
    icon: ChatDotRound,
    color: '#e6a23c',
    bgColor: '#fdf6ec'
  },
  {
    title: '总分类数',
    value: summary.total_categories,
    icon: Menu,
    color: '#f56c6c',
    bgColor: '#fef0f0'
  }
])

const quickActions = [
  { title: '查看询盘', icon: View, path: '/admin/inquiries', desc: '处理客户询盘' },
  { title: '新闻管理', icon: Edit, path: '/admin/news', desc: '管理新闻资讯' },
  { title: '网站设置', icon: Tools, path: '/admin/settings', desc: '配置网站信息' }
]

const salesChartOption = computed<EChartsOption>(() => {
  const xAxisData = salesChartData.value.map(item => item.name)
  const seriesData = salesChartData.value.map(item => item.value)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: chartType.value === 'bar' ? 'shadow' : 'line'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: {
        rotate: 30,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      name: '销量'
    },
    series: [
      {
        name: '产品销量',
        type: chartType.value,
        data: seriesData,
        itemStyle: {
          color: '#409eff'
        },
        areaStyle: chartType.value === 'line' ? {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
            ]
          }
        } : undefined,
        smooth: chartType.value === 'line'
      }
    ]
  }
})

const trendChartOption = computed<EChartsOption>(() => {
  const xAxisData = trendChartData.value.map(item => item.name)
  const seriesData = trendChartData.value.map(item => item.value)
  
  return {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: xAxisData,
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      name: '询盘数'
    },
    series: [
      {
        name: '询盘趋势',
        type: 'line',
        data: seriesData,
        itemStyle: {
          color: '#67c23a'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
              { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
            ]
          }
        },
        smooth: true
      }
    ]
  }
})

async function loadSummary() {
  try {
    await loadSummaryFallback()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

async function loadSummaryFallback() {
  try {
    const [productsRes, inquiriesRes, categoriesRes] = await Promise.all([
      productApi.list({ page: 1, page_size: 1 }),
      inquiryApi.list({ page: 1, page_size: 1 }),
      categoryApi.list()
    ])
    
    summary.total_products = (productsRes.code === 200 || productsRes.code === 0) ? (productsRes.data?.total || 0) : 0
    summary.total_inquiries = (inquiriesRes.code === 200 || inquiriesRes.code === 0) ? (inquiriesRes.data?.total || 0) : 0
    summary.total_categories = (categoriesRes.code === 200 || categoriesRes.code === 0) ? (categoriesRes.data?.length || 0) : 0
    
    const pendingRes = await inquiryApi.list({ page: 1, page_size: 1, is_replied: 0 })
    summary.pending_inquiries = (pendingRes.code === 200 || pendingRes.code === 0) ? (pendingRes.data?.total || 0) : 0
    summary.replied_inquiries = summary.total_inquiries - summary.pending_inquiries
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

async function loadRecentInquiries() {
  try {
    const res = await inquiryApi.list({ page: 1, page_size: 5 })
    if (res.code === 200 || res.code === 0) {
      recentInquiries.value = res.data.items
    }
  } catch (error) {
    console.error('获取最近询盘失败:', error)
  }
}

async function loadSalesChart() {
  try {
    salesChartData.value = [
      { name: '产品A', value: 120 },
      { name: '产品B', value: 200 },
      { name: '产品C', value: 150 },
      { name: '产品D', value: 80 },
      { name: '产品E', value: 70 },
      { name: '产品F', value: 110 },
      { name: '产品G', value: 130 }
    ]
  } catch (error) {
    console.error('获取销量图表数据失败:', error)
  }
}

async function loadTrendChart() {
  try {
    const days = []
    for (let i = 6; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      const month = date.getMonth() + 1
      const day = date.getDate()
      days.push({
        name: `${month}/${day}`,
        value: Math.floor(Math.random() * 20) + 5
      })
    }
    trendChartData.value = days
  } catch (error) {
    console.error('获取询盘趋势数据失败:', error)
  }
}

function viewInquiry(id: number) {
  router.push(`/admin/inquiries`)
}

function goTo(path: string) {
  router.push(path)
}

function getStatusTag(is_replied: number) {
  return is_replied === 1 ? 'success' : 'warning'
}

function getStatusText(is_replied: number) {
  return is_replied === 1 ? '已回复' : '待回复'
}

onMounted(() => {
  loadSummary()
  loadRecentInquiries()
  loadSalesChart()
  loadTrendChart()
})
</script>

<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="card in statsCards" :key="card.title">
        <el-card class="stat-card" :body-style="{ padding: '20px' }">
          <div class="stat-content">
            <div class="stat-info">
              <p class="stat-title">{{ card.title }}</p>
              <p class="stat-value">{{ card.value }}</p>
            </div>
            <div class="stat-icon" :style="{ backgroundColor: card.bgColor, color: card.color }">
              <el-icon :size="32">
                <component :is="card.icon" />
              </el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>产品销量统计</span>
              <el-radio-group v-model="chartType" size="small">
                <el-radio-button label="bar">柱状图</el-radio-button>
                <el-radio-button label="line">折线图</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="quick-card">
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <div
              v-for="action in quickActions"
              :key="action.title"
              class="quick-item"
              @click="goTo(action.path)"
            >
              <el-icon :size="24" class="quick-icon">
                <component :is="action.icon" />
              </el-icon>
              <div class="quick-text">
                <p class="quick-title">{{ action.title }}</p>
                <p class="quick-desc">{{ action.desc }}</p>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="16">
        <el-card class="inquiries-card">
          <template #header>
            <div class="card-header">
              <span>最近询盘</span>
              <el-button type="primary" link @click="goTo('/admin/inquiries')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentInquiries" v-loading="loading" style="width: 100%" :header-cell-style="{ backgroundColor: '#f5f7fa' }">
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="customer_name" label="客户姓名" width="110" />
            <el-table-column prop="email" label="邮箱" width="160" show-overflow-tooltip />
            <el-table-column prop="country" label="国家" width="100" />
            <el-table-column prop="message" label="询盘内容" min-width="200" show-overflow-tooltip />
            <el-table-column label="状态" width="90" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusTag(row.is_replied)" size="small">
                  {{ getStatusText(row.is_replied) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="170">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="70" fixed="right" align="center">
              <template #default="{ row }">
                <el-button type="primary" link @click="viewInquiry(row.id)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="trend-card">
          <template #header>
            <span>询盘趋势（近7天）</span>
          </template>
          <div class="chart-container small">
            <v-chart :option="trendChartOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border: none;
  border-radius: 8px;
}

.stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-info .stat-title {
  font-size: 14px;
  color: #909399;
  margin: 0 0 8px 0;
}

.stat-info .stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-row {
  margin-bottom: 20px;
}

.chart-card,
.quick-card,
.inquiries-card,
.trend-card {
  border: none;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.chart-container.small {
  height: 280px;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.quick-item:hover {
  background-color: #f5f7fa;
}

.quick-icon {
  color: #409eff;
}

.quick-text .quick-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 2px 0;
}

.quick-text .quick-desc {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.inquiries-card {
  margin-bottom: 0;
}
</style>
