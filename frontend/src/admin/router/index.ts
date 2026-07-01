import type { RouteRecordRaw } from 'vue-router'

export const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/admin/login',
    name: 'admin-login',
    component: () => import('@/admin/views/login/Index.vue')
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: () => import('@/admin/views/dashboard/Index.vue')
      },
      {
        path: 'inquiries',
        name: 'admin-inquiries',
        component: () => import('@/admin/views/inquiries/Index.vue')
      },
      {
        path: 'products',
        name: 'admin-products',
        component: () => import('@/admin/views/products/Index.vue')
      },
      {
        path: 'categories',
        name: 'admin-categories',
        component: () => import('@/admin/views/categories/Index.vue')
      },
      {
        path: 'news',
        name: 'admin-news',
        component: () => import('@/admin/views/news/Index.vue')
      },
      {
        path: 'settings',
        name: 'admin-settings',
        component: () => import('@/admin/views/settings/Index.vue')
      }
    ]
  }
]
