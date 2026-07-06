export interface Product {
  id: number
  name_en?: string
  name_zh?: string
  name?: string
  name_i18n?: Record<string, string>
  model?: string  // 型号
  description_en?: string
  description_zh?: string
  description?: string
  description_i18n?: Record<string, string>
  spec_en?: string
  spec_zh?: string
  spec?: string
  specs?: any[]
  package_en?: string
  package_zh?: string
  packaging?: string
  packaging_i18n?: Record<string, string>
  price?: number
  price_usd?: number
  price_cny?: number
  moq?: number
  stock?: number
  category_id?: number
  image?: string
  images?: string[]
  is_hot?: boolean
  is_online?: boolean
  status?: number
  sort_order?: number
  created_at?: string
  updated_at?: string
}

export interface Category {
  id: number
  name: string
  name_i18n?: Record<string, string>
  name_en?: string
  name_zh?: string
  description_en?: string
  description_zh?: string
  image?: string
  parent_id: number | null
  sort_order: number
  status?: number
  children?: Category[]
  created_at?: string
  updated_at?: string
}

export interface Inquiry {
  id: number
  product_id: number | null
  product_name: string
  name: string
  email: string
  country: string
  quantity: number
  message: string
  status: 'pending' | 'replied'
  reply_content: string
  created_at: string
  updated_at: string
}

export interface News {
  id: number
  title: string
  content: string
  cover_image: string
  sort_order: number
  status: number
  created_at: string
  updated_at: string
}

export interface Banner {
  id: number
  title: string
  title_i18n?: Record<string, string>
  title_en?: string
  title_zh?: string
  subtitle_en?: string
  subtitle_zh?: string
  image: string
  image_url?: string
  link: string
  link_url?: string
  is_online: boolean
  status: number
  sort_order: number
  created_at?: string
  updated_at?: string
}

export interface SiteConfig {
  id: number
  site_name: string
  site_title: string
  keywords: string
  description: string
  company_name: string
  phone: string
  email: string
  address: string
  about_us: string
  facebook: string
  twitter: string
  linkedin: string
  instagram: string
  created_at: string
  updated_at: string
}

export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar: string
  role: string
  created_at: string
}

export interface LoginData {
  token: string
  user: UserInfo
}

export interface DashboardSummary {
  total_products: number
  total_categories: number
  total_inquiries: number
  total_news: number
  pending_inquiries: number
  replied_inquiries: number
}
