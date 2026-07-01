import request from '@/utils/request'
import type { Category, ApiResponse } from '@/types'

export function getCategories(): Promise<ApiResponse<Category[]>> {
  return request.get('/api/v1/categories')
}

export function getCategory(id: number): Promise<ApiResponse<Category>> {
  return request.get(`/api/v1/categories/${id}`)
}

export function listCategories(): Promise<ApiResponse<Category[]>> {
  return request.get('/api/v1/admin/categories')
}

export function createCategory(data: Partial<Category>): Promise<ApiResponse<Category>> {
  return request.post('/api/v1/admin/categories', data)
}

export function updateCategory(id: number, data: Partial<Category>): Promise<ApiResponse<Category>> {
  return request.put(`/api/v1/admin/categories/${id}`, data)
}

export function deleteCategory(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/api/v1/admin/categories/${id}`)
}
