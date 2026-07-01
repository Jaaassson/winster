import request from '@/utils/request'
import type { ApiResponse, LoginData, UserInfo } from '@/types'

export interface LoginParams {
  username: string
  password: string
}

export function login(data: LoginParams): Promise<ApiResponse<LoginData>> {
  return request.post('/api/v1/auth/login', data)
}

export function logout(): Promise<ApiResponse<void>> {
  return request.post('/api/v1/auth/logout')
}

export function getCurrentUser(): Promise<ApiResponse<UserInfo>> {
  return request.get('/api/v1/auth/me')
}

export function changePassword(data: {
  old_password: string
  new_password: string
  confirm_password: string
}): Promise<ApiResponse<void>> {
  return request.post('/api/v1/auth/change-password', data)
}
