import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useUserStore } from '@/store/user'
import { useLangStore } from '@/store/lang'

const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 15000
})

service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const userStore = useUserStore()
    const langStore = useLangStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    config.headers['Accept-Language'] = langStore.lang === 'zh' ? 'zh-CN' : 'en-US'
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (res) => {
    const data = res.data
    if (data && typeof data === 'object' && 'code' in data) {
      if (data.code === 200 || data.code === 0) {
        return data
      }
      if (data.code === 401) {
        const userStore = useUserStore()
        userStore.logout()
        ElMessage.error('登录已过期，请重新登录')
        router.push('/admin/login')
      } else {
        ElMessage.error(data.message || '请求失败')
      }
      return Promise.reject(new Error(data.message || 'Error'))
    }
    return data
  },
  (err) => {
    if (err?.response?.status === 401) {
      const userStore = useUserStore()
      userStore.logout()
      ElMessage.error('登录已过期，请重新登录')
      router.push('/admin/login')
    } else {
      ElMessage.error(err?.message || '网络错误')
    }
    return Promise.reject(err)
  }
)

export default service
