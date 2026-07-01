import request from '@/utils/request'
import type { Product, PaginatedData, ApiResponse } from '@/types'

export interface ProductListParams {
  page?: number
  page_size?: number
  category_id?: number
  keyword?: string
  is_hot?: boolean
  is_online?: boolean
}

export function getProducts(params?: ProductListParams): Promise<ApiResponse<PaginatedData<Product>>> {
  return request.get('/api/v1/products', { params })
}

export function getProduct(id: number): Promise<ApiResponse<Product>> {
  return request.get(`/api/v1/products/${id}`)
}

export function getHotProducts(limit: number = 8): Promise<ApiResponse<Product[]>> {
  return request.get('/api/v1/products/hot', { params: { limit } })
}

export function listProducts(params?: ProductListParams): Promise<ApiResponse<PaginatedData<Product>>> {
  return request.get('/api/v1/admin/products', { params })
}

export function createProduct(data: Partial<Product>): Promise<ApiResponse<Product>> {
  return request.post('/api/v1/admin/products', data)
}

export function updateProduct(id: number, data: Partial<Product>): Promise<ApiResponse<Product>> {
  return request.put(`/api/v1/admin/products/${id}`, data)
}

export function deleteProduct(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/api/v1/admin/products/${id}`)
}
