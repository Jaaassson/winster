import request from '@/utils/request'
import type { SiteConfig, Banner, ApiResponse } from '@/types'

export function getSiteConfig(): Promise<ApiResponse<SiteConfig>> {
  return request.get('/api/v1/site/config')
}

export function updateSiteConfig(data: Partial<SiteConfig>): Promise<ApiResponse<SiteConfig>> {
  return request.put('/api/v1/admin/site/config', data)
}

export function getBanners(): Promise<ApiResponse<Banner[]>> {
  return request.get('/api/v1/banners')
}

export function listBanners(): Promise<ApiResponse<Banner[]>> {
  return request.get('/api/v1/admin/banners')
}

export function createBanner(data: Partial<Banner>): Promise<ApiResponse<Banner>> {
  return request.post('/api/v1/admin/banners', data)
}

export function updateBanner(id: number, data: Partial<Banner>): Promise<ApiResponse<Banner>> {
  return request.put(`/api/v1/admin/banners/${id}`, data)
}

export function deleteBanner(id: number): Promise<ApiResponse<void>> {
  return request.delete(`/api/v1/admin/banners/${id}`)
}

export function uploadImage(file: File): Promise<ApiResponse<{ url: string }>> {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/api/v1/admin/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
