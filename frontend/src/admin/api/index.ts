import request from '@/utils/request'
import type { ApiResult, PageData } from '@/api'

export const adminApi = {
  login: (data: { username: string; password: string }) =>
    request.post('/api/v1/auth/login', data) as Promise<ApiResult<{ access_token: string; user: any }>>,

  getProfile: () =>
    request.get('/api/v1/auth/me') as Promise<ApiResult<any>>,

  updatePassword: (data: { old_password: string; new_password: string }) =>
    request.put('/api/v1/auth/password', data) as Promise<ApiResult<any>>
}

export const productApi = {
  list: (params?: any) =>
    request.get('/api/v1/admin/products', { params }) as Promise<ApiResult<PageData<any>>>,
  detail: (id: number) =>
    request.get(`/api/v1/admin/products/${id}`) as Promise<ApiResult<any>>,
  create: (data: any) =>
    request.post('/api/v1/admin/products', data) as Promise<ApiResult<any>>,
  update: (id: number, data: any) =>
    request.put(`/api/v1/admin/products/${id}`, data) as Promise<ApiResult<any>>,
  delete: (id: number) =>
    request.delete(`/api/v1/admin/products/${id}`) as Promise<ApiResult<any>>,
  toggleStatus: (id: number) =>
    request.patch(`/api/v1/admin/products/${id}/status`) as Promise<ApiResult<any>>
}

export const categoryApi = {
  list: (params?: any) =>
    request.get('/api/v1/admin/categories', { params }) as Promise<ApiResult<any[]>>,
  tree: () =>
    request.get('/api/v1/admin/categories/tree') as Promise<ApiResult<any[]>>,
  create: (data: any) =>
    request.post('/api/v1/admin/categories', data) as Promise<ApiResult<any>>,
  update: (id: number, data: any) =>
    request.put(`/api/v1/admin/categories/${id}`, data) as Promise<ApiResult<any>>,
  delete: (id: number) =>
    request.delete(`/api/v1/admin/categories/${id}`) as Promise<ApiResult<any>>,
  toggleStatus: (id: number) =>
    request.patch(`/api/v1/admin/categories/${id}/status`) as Promise<ApiResult<any>>
}

export const inquiryApi = {
  list: (params?: any) =>
    request.get('/api/v1/admin/inquiries', { params }) as Promise<ApiResult<PageData<any>>>,
  detail: (id: number) =>
    request.get(`/api/v1/admin/inquiries/${id}`) as Promise<ApiResult<any>>,
  markReplied: (id: number) =>
    request.patch(`/api/v1/admin/inquiries/${id}/status`) as Promise<ApiResult<any>>,
  delete: (id: number) =>
    request.delete(`/api/v1/admin/inquiries/${id}`) as Promise<ApiResult<any>>
}

export const newsApi = {
  list: (params?: any) =>
    request.get('/api/v1/admin/news', { params }) as Promise<ApiResult<PageData<any>>>,
  detail: (id: number) =>
    request.get(`/api/v1/admin/news/${id}`) as Promise<ApiResult<any>>,
  create: (data: any) =>
    request.post('/api/v1/admin/news', data) as Promise<ApiResult<any>>,
  update: (id: number, data: any) =>
    request.put(`/api/v1/admin/news/${id}`, data) as Promise<ApiResult<any>>,
  delete: (id: number) =>
    request.delete(`/api/v1/admin/news/${id}`) as Promise<ApiResult<any>>
}

export const bannerApi = {
  list: () =>
    request.get('/api/v1/admin/banners') as Promise<ApiResult<any[]>>,
  create: (data: any) =>
    request.post('/api/v1/admin/banners', data) as Promise<ApiResult<any>>,
  update: (id: number, data: any) =>
    request.put(`/api/v1/admin/banners/${id}`, data) as Promise<ApiResult<any>>,
  delete: (id: number) =>
    request.delete(`/api/v1/admin/banners/${id}`) as Promise<ApiResult<any>>
}

export const siteConfigApi = {
  get: () =>
    request.get('/api/v1/admin/site-config') as Promise<ApiResult<any>>,
  update: (data: any) =>
    request.put('/api/v1/admin/site-config', data) as Promise<ApiResult<any>>
}

export const uploadApi = {
  image: (file: File) => {
    const fd = new FormData()
    fd.append('file', file)
    return request.post('/api/v1/admin/upload/image', fd) as Promise<ApiResult<{ url: string }>>
  }
}
