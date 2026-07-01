import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'
import { adminRoutes } from '@/admin/router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('@/views/home/Index.vue') },
      { path: 'products', name: 'products', component: () => import('@/views/products/List.vue') },
      { path: 'products/:id', name: 'product-detail', component: () => import('@/views/products/Detail.vue'), props: true },
      { path: 'inquiry', name: 'inquiry', component: () => import('@/views/inquiry/Index.vue') },
      { path: 'about', name: 'about', component: () => import('@/views/about/Index.vue') },
      { path: 'contact', name: 'contact', component: () => import('@/views/contact/Index.vue') },
      { path: 'faq', name: 'faq', component: () => import('@/views/faq/Index.vue') },
      { path: 'shipping', name: 'shipping', component: () => import('@/views/shipping/Index.vue') }
    ]
  },
  ...adminRoutes,
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    if (!userStore.token) {
      return { path: '/admin/login', query: { redirect: to.fullPath } }
    }
  }
})

export default router
