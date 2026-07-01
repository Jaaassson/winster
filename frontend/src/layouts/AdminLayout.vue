<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useUserStore } from '@/store/user'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const menus = [
  { path: '/admin/dashboard', icon: 'DataAnalysis', labelKey: 'admin.dashboard' },
  { path: '/admin/products', icon: 'Goods', labelKey: 'admin.products' },
  { path: '/admin/categories', icon: 'Menu', labelKey: 'admin.categories' },
  { path: '/admin/inquiries', icon: 'Message', labelKey: 'admin.inquiries' },
  { path: '/admin/news', icon: 'Notebook', labelKey: 'admin.news' },
  { path: '/admin/settings', icon: 'Tools', labelKey: 'admin.config' }
]

function logout() {
  userStore.logout()
  router.push('/admin/login')
}
</script>

<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="aside">
      <div class="brand">WINSTER ADMIN</div>
      <el-menu :default-active="route.path" router background-color="#001529" text-color="#bfcbd9" active-text-color="#fff">
        <el-menu-item v-for="m in menus" :key="m.path" :index="m.path">
          <el-icon><component :is="m.icon" /></el-icon>
          <span>{{ t(m.labelKey) }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div></div>
        <div class="header-right">
          <span>{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</span>
          <el-button size="small" @click="logout">{{ t('admin.logout') }}</el-button>
        </div>
      </el-header>
      <el-main class="main"><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.admin-layout { min-height: 100vh; }
.aside { background: #001529; }
.brand { color: #fff; font-size: 18px; font-weight: 700; padding: 20px; text-align: center; letter-spacing: 2px; border-bottom: 1px solid #1f2d3d; }
.header { background: #fff; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.header-right { display: flex; align-items: center; gap: 12px; }
.main { background: #f5f7fa; }
</style>