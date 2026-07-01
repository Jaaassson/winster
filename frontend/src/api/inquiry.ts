import request from '@/utils/request'
import type { Inquiry, PaginatedData, ApiResponse } from '@/types'

export interface InquirySubmitData {
  product_id?: number
  product_name?: string
  name: string
  email: string
  country?: string
  quantity?: number
  message: string
}

export interface InquiryListParams {
  page?: number
  page_size?: number
  status?: 'pending' | 'replied'
  keyword?: string
}

export function submitInquiry(data: InquirySubmitData): Promise<ApiResponse<Inquiry>> {
  return request.post('/api/v1/inquiries', data)
}

export function listInquiries(params?: InquiryListParams): Promise<ApiResponse<PaginatedData<Inquiry>>> {
  return request.get('/api/v1/admin/inquiries', { params })
}

export function getInquiry(id: number): Promise<ApiResponse<Inquiry>> {
  return request.get(`/api/v1/admin/inquiries/${id}`)
}

export function updateInquiry(id: number, data: Partial<Inquiry>): Promise<ApiResponse<Inquiry>> {
  return request.put(`/api/v1/admin/inquiries/${id}`, data)
}

export function deleteInquiry(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/api/v1/admin/inquiries/${id}`)
}

export function exportInquiries(): string {
  return '/api/v1/admin/inquiries/export.csv'
}
