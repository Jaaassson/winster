import request from '@/utils/request'

export interface ApiResult<T = any> {
  code: number
  message: string
  data: T
}
export interface PageData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export const productApi = {
  list: (params?: any) =>
    request.get('/api/v1/products', { params }) as Promise<ApiResult<PageData<any>>>,
  detail: (id: number) =>
    request.get(`/api/v1/products/${id}`) as Promise<ApiResult<any>>,
  hot: () =>
    request.get('/api/v1/products/hot') as Promise<ApiResult<any[]>>
}

export const categoryApi = {
  list: () =>
    request.get('/api/v1/categories') as Promise<ApiResult<any[]>>,
  tree: () =>
    request.get('/api/v1/categories/tree') as Promise<ApiResult<any[]>>
}

export const newsApi = {
  list: (params?: any) =>
    request.get('/api/v1/news', { params }) as Promise<ApiResult<PageData<any>>>,
  detail: (id: number) =>
    request.get(`/api/v1/news/${id}`) as Promise<ApiResult<any>>
}

export const inquiryApi = {
  submit: (data: any) =>
    request.post('/api/v1/inquiries', data) as Promise<ApiResult<any>>
}

export const bannerApi = {
  list: () =>
    request.get('/api/v1/banners') as Promise<ApiResult<any[]>>
}

export const siteConfigApi = {
  get: () =>
    request.get('/api/v1/site-config') as Promise<ApiResult<any>>
}

export const authApi = {
  login: (data: { username: string; password: string }) =>
    request.post('/api/v1/auth/login', data) as Promise<ApiResult<{ access_token: string; user: any }>>
}
