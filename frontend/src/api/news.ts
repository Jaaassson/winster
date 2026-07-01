import request from '@/utils/request'
import type { News, PaginatedData, ApiResponse } from '@/types'

export interface NewsListParams {
  page?: number
  page_size?: number
  keyword?: string
  is_online?: boolean
}

export function getNews(params?: NewsListParams): Promise<ApiResponse<PaginatedData<News>>> {
  return request.get('/api/v1/news', { params })
}

export function getNewsDetail(id: number): Promise<ApiResponse<News>> {
  return request.get(`/api/v1/news/${id}`)
}

export function getLatestNews(limit: number = 5): Promise<ApiResponse<News[]>> {
  return request.get('/api/v1/news/latest', { params: { limit } })
}

export function listNews(params?: NewsListParams): Promise<ApiResponse<PaginatedData<News>>> {
  return request.get('/api/v1/admin/news', { params })
}

export function createNews(data: Partial<News>): Promise<ApiResponse<News>> {
  return request.post('/api/v1/admin/news', data)
}

export function updateNews(id: number, data: Partial<News>): Promise<ApiResponse<News>> {
  return request.put(`/api/v1/admin/news/${id}`, data)
}

export function deleteNews(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/api/v1/admin/news/${id}`)
}
