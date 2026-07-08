<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { siteConfigApi, bannerApi, uploadApi } from '@/admin/api'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Edit, Delete, Upload, Sort } from '@element-plus/icons-vue'

const loading = ref(false)
const saving = ref(false)
const activeTab = ref('basic')
const bannerLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('添加Banner')
const editingId = ref<number | null>(null)

const configFormRef = ref<FormInstance>()
const bannerFormRef = ref<FormInstance>()

const configForm = reactive({
  site_name_zh: '',
  site_name_en: '',
  site_title_zh: '',
  site_title_en: '',
  keywords: '',
  description: '',
  company_name_zh: '',
  company_name_en: '',
  phone: '',
  email: '',
  address_zh: '',
  address_en: '',
  about_us_zh: '',
  about_us_en: '',
  facebook: '',
  twitter: '',
  linkedin: '',
  instagram: '',
  qrcode: ''
})

const bannerList = ref<any[]>([])

const bannerForm = reactive({
  image_url: '',
  title_zh: '',
  title_en: '',
  button_text_zh: '',
  button_text_en: '',
  link_url: '',
  sort_order: 0,
  status: 1
})

function parseI18nField(value: any): { 'zh-CN': string; 'en-US': string } {
  if (!value) return { 'zh-CN': '', 'en-US': '' }
  if (typeof value === 'object') {
    return { 'zh-CN': value['zh-CN'] || '', 'en-US': value['en-US'] || '' }
  }
  try {
    const parsed = JSON.parse(value)
    return { 'zh-CN': parsed['zh-CN'] || '', 'en-US': parsed['en-US'] || '' }
  } catch {
    return { 'zh-CN': String(value), 'en-US': String(value) }
  }
}

function buildI18nField(zh: string, en: string): string {
  return JSON.stringify({ 'zh-CN': zh || '', 'en-US': en || '' })
}

async function loadConfig() {
  loading.value = true
  try {
    const res = await siteConfigApi.get()
    if ((res.code === 200 || res.code === 0) && res.data) {
      const d = res.data
      const siteName = parseI18nField(d.site_name)
      const siteTitle = parseI18nField(d.site_title)
      const companyName = parseI18nField(d.company_name)
      const address = parseI18nField(d.address)
      const aboutUs = parseI18nField(d.about_us)
      configForm.site_name_zh = siteName['zh-CN']
      configForm.site_name_en = siteName['en-US']
      configForm.site_title_zh = siteTitle['zh-CN']
      configForm.site_title_en = siteTitle['en-US']
      configForm.keywords = d.keywords || ''
      configForm.description = d.description || ''
      configForm.company_name_zh = companyName['zh-CN']
      configForm.company_name_en = companyName['en-US']
      configForm.phone = d.phone || ''
      configForm.email = d.email || ''
      configForm.address_zh = address['zh-CN']
      configForm.address_en = address['en-US']
      configForm.about_us_zh = aboutUs['zh-CN']
      configForm.about_us_en = aboutUs['en-US']
      configForm.facebook = d.facebook || ''
      configForm.twitter = d.twitter || ''
      configForm.linkedin = d.linkedin || ''
      configForm.instagram = d.instagram || ''
      configForm.qrcode = d.qrcode || ''
    }
  } catch (error) {
    console.error('获取网站配置失败:', error)
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  saving.value = true
  try {
    const payload = {
      site_name: buildI18nField(configForm.site_name_zh, configForm.site_name_en),
      site_title: buildI18nField(configForm.site_title_zh, configForm.site_title_en),
      keywords: configForm.keywords,
      description: configForm.description,
      company_name: buildI18nField(configForm.company_name_zh, configForm.company_name_en),
      phone: configForm.phone,
      email: configForm.email,
      address: buildI18nField(configForm.address_zh, configForm.address_en),
      about_us: buildI18nField(configForm.about_us_zh, configForm.about_us_en),
      facebook: configForm.facebook,
      twitter: configForm.twitter,
      linkedin: configForm.linkedin,
      instagram: configForm.instagram,
      qrcode: configForm.qrcode
    }
    const res = await siteConfigApi.update(payload)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('保存成功')
    }
  } catch (error) {
    console.error('保存配置失败:', error)
  } finally {
    saving.value = false
  }
}

async function loadBanners() {
  bannerLoading.value = true
  try {
    const res = await bannerApi.list()
    if (res.code === 200 || res.code === 0) {
      bannerList.value = res.data || []
    }
  } catch (error) {
    console.error('获取Banner列表失败:', error)
  } finally {
    bannerLoading.value = false
  }
}

function handleAddBanner() {
  editingId.value = null
  dialogTitle.value = '添加Banner'
  bannerForm.image_url = ''
  bannerForm.title_zh = ''
  bannerForm.title_en = ''
  bannerForm.button_text_zh = ''
  bannerForm.button_text_en = ''
  bannerForm.link_url = ''
  bannerForm.sort_order = 0
  bannerForm.status = 1
  dialogVisible.value = true
}

function handleEditBanner(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑Banner'
  bannerForm.image_url = row.image_url || ''
  bannerForm.title_zh = row.title_i18n?.['zh-CN'] || row.title || ''
  bannerForm.title_en = row.title_i18n?.['en-US'] || ''
  bannerForm.button_text_zh = row.button_text_i18n?.['zh-CN'] || row.button_text || ''
  bannerForm.button_text_en = row.button_text_i18n?.['en-US'] || ''
  bannerForm.link_url = row.link_url || ''
  bannerForm.sort_order = row.sort_order || 0
  bannerForm.status = Number(row.status) ?? 1
  dialogVisible.value = true
}

async function handleDeleteBanner(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这个Banner吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await bannerApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('删除成功')
      loadBanners()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

async function handleBannerUpload(options: any) {
  const { file, onSuccess, onError } = options
  try {
    const res = await uploadApi.image(file)
    if (res.code === 200 || res.code === 0) {
      bannerForm.image_url = res.data.url
      onSuccess(res.data)
      ElMessage.success('上传成功')
    } else {
      onError(new Error(res.message || '上传失败'))
      ElMessage.error(res.message || '上传失败')
    }
  } catch (error: any) {
    console.error('上传失败:', error)
    onError(error)
    ElMessage.error(error.message || '上传失败')
  }
}

async function handleBannerSubmit() {
  const data = {
    image_url: bannerForm.image_url,
    title: {
      'zh-CN': bannerForm.title_zh,
      'en-US': bannerForm.title_en
    },
    button_text: {
      'zh-CN': bannerForm.button_text_zh,
      'en-US': bannerForm.button_text_en
    },
    link_url: bannerForm.link_url,
    sort_order: bannerForm.sort_order,
    status: bannerForm.status
  }

  try {
    let res
    if (editingId.value) {
      res = await bannerApi.update(editingId.value, data)
    } else {
      res = await bannerApi.create(data)
    }
    if (res.code === 200 || res.code === 0 || res.code === 201) {
      ElMessage.success(editingId.value ? '更新成功' : '创建成功')
      dialogVisible.value = false
      loadBanners()
    }
  } catch (error) {
    console.error('提交失败:', error)
  }
}

function getStatusTag(status: number) {
  return status === 1 ? 'success' : 'info'
}

function getStatusText(status: number) {
  return status === 1 ? '已上线' : '已下线'
}

async function handleQrcodeUpload(options: any) {
  const { file, onSuccess, onError } = options
  try {
    const res = await uploadApi.image(file)
    if (res.code === 200 || res.code === 0) {
      configForm.qrcode = res.data.url
      onSuccess(res.data)
      ElMessage.success('上传成功')
    } else {
      onError(new Error(res.message || '上传失败'))
      ElMessage.error(res.message || '上传失败')
    }
  } catch (error: any) {
    console.error('上传失败:', error)
    onError(error)
    ElMessage.error(error.message || '上传失败')
  }
}

onMounted(() => {
  loadConfig()
  loadBanners()
})
</script>

<template>
  <div class="settings-page">
    <el-card class="page-card" shadow="never" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span class="title">网站配置</span>
          <el-button type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="基本信息" name="basic">
          <el-form
            ref="configFormRef"
            :model="configForm"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="网站名称(中)">
                  <el-input v-model="configForm.site_name_zh" placeholder="请输入中文网站名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="网站名称(英)">
                  <el-input v-model="configForm.site_name_en" placeholder="Please enter English site name" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="网站标题(中)">
                  <el-input v-model="configForm.site_title_zh" placeholder="请输入中文网站标题" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="网站标题(英)">
                  <el-input v-model="configForm.site_title_en" placeholder="Please enter English site title" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="关键词">
                  <el-input v-model="configForm.keywords" placeholder="请输入关键词" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="描述">
                  <el-input v-model="configForm.description" placeholder="请输入描述" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="公司名称(中)">
                  <el-input v-model="configForm.company_name_zh" placeholder="请输入中文公司名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="公司名称(英)">
                  <el-input v-model="configForm.company_name_en" placeholder="Please enter English company name" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="联系电话">
                  <el-input v-model="configForm.phone" placeholder="请输入联系电话" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="邮箱">
                  <el-input v-model="configForm.email" placeholder="请输入联系邮箱" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="地址(中)">
                  <el-input v-model="configForm.address_zh" type="textarea" :rows="2" placeholder="请输入中文地址" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="地址(英)">
                  <el-input v-model="configForm.address_en" type="textarea" :rows="2" placeholder="Please enter English address" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="社交媒体" name="social">
          <el-form
            :model="configForm"
            label-width="120px"
            class="config-form"
          >
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="Facebook">
                  <el-input v-model="configForm.facebook" placeholder="请输入Facebook链接" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Twitter">
                  <el-input v-model="configForm.twitter" placeholder="请输入Twitter链接" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="LinkedIn">
                  <el-input v-model="configForm.linkedin" placeholder="请输入LinkedIn链接" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="Instagram">
                  <el-input v-model="configForm.instagram" placeholder="请输入Instagram链接" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="关于我们" name="about">
          <el-form
            :model="configForm"
            label-width="120px"
            class="config-form"
          >
            <el-form-item label="关于我们(中)">
              <el-input
                v-model="configForm.about_us_zh"
                type="textarea"
                :rows="8"
                placeholder="请输入中文关于我们内容"
              />
            </el-form-item>
            <el-form-item label="关于我们(英)">
              <el-input
                v-model="configForm.about_us_en"
                type="textarea"
                :rows="8"
                placeholder="Please enter English about us content"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="二维码" name="qrcode">
          <el-form
            :model="configForm"
            label-width="120px"
            class="config-form"
          >
            <el-form-item label="微信二维码">
              <div class="qrcode-upload">
                <div v-if="configForm.qrcode" class="qrcode-preview">
                  <el-image :src="configForm.qrcode" fit="contain" style="width: 100%; height: 100%" />
                  <span class="remove-qrcode" @click="configForm.qrcode = ''">×</span>
                </div>
                <el-upload
                  v-else
                  action="#"
                  :show-file-list="false"
                  :http-request="handleQrcodeUpload"
                  accept="image/*"
                >
                  <div class="upload-qrcode-btn">
                    <el-icon><Upload /></el-icon>
                    <span>上传二维码</span>
                  </div>
                </el-upload>
              </div>
              <div class="qrcode-tip">支持上传微信二维码图片，用于首页展示</div>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Banner管理" name="banner">
          <div class="banner-section">
            <div class="banner-header">
              <el-button type="primary" :icon="Plus" @click="handleAddBanner">添加Banner</el-button>
            </div>
            <el-table :data="bannerList" v-loading="bannerLoading" style="width: 100%" :header-cell-style="{ backgroundColor: '#f5f7fa' }">
              <el-table-column prop="id" label="ID" width="70" />
              <el-table-column label="图片" width="120">
                <template #default="{ row }">
                  <el-image
                    v-if="row.image_url"
                    :src="row.image_url"
                    style="width: 80px; height: 50px"
                    fit="cover"
                  />
                  <span v-else class="no-image">无图</span>
                </template>
              </el-table-column>
              <el-table-column label="标题(中文)" min-width="150" show-overflow-tooltip>
                <template #default="{ row }">
                  {{ row.title_i18n?.['zh-CN'] || row.title || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="标题(英文)" min-width="150" show-overflow-tooltip>
                <template #default="{ row }">
                  {{ row.title_i18n?.['en-US'] || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="按钮文字(中)" width="120" show-overflow-tooltip>
                <template #default="{ row }">
                  {{ row.button_text_i18n?.['zh-CN'] || row.button_text || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="按钮文字(英)" width="120" show-overflow-tooltip>
                <template #default="{ row }">
                  {{ row.button_text_i18n?.['en-US'] || '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="link_url" label="跳转链接" min-width="150" show-overflow-tooltip />
              <el-table-column prop="sort_order" label="排序" width="80" align="center" />
              <el-table-column label="状态" width="90" align="center">
                <template #default="{ row }">
                  <el-tag :type="getStatusTag(row.status)" size="small">
                    {{ getStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right" align="center">
                <template #default="{ row }">
                  <el-button type="primary" link :icon="Edit" @click="handleEditBanner(row)">编辑</el-button>
                  <el-button type="danger" link :icon="Delete" @click="handleDeleteBanner(row.id)">删除</el-button>
                </template>
              </el-table-column>
              <template #empty>
                <el-empty description="暂无Banner数据" />
              </template>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form ref="bannerFormRef" :model="bannerForm" label-width="120px">
        <el-form-item label="Banner图片" required>
          <div class="banner-upload">
            <div v-if="bannerForm.image_url" class="banner-preview">
              <el-image :src="bannerForm.image_url" fit="cover" style="width: 100%; height: 100%" />
              <span class="remove-banner" @click="bannerForm.image_url = ''">×</span>
            </div>
            <el-upload
              v-else
              action="#"
              :show-file-list="false"
              :http-request="handleBannerUpload"
              accept="image/*"
            >
              <div class="upload-banner-btn">
                <el-icon><Upload /></el-icon>
                <span>上传图片</span>
              </div>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="中文标题">
          <el-input v-model="bannerForm.title_zh" placeholder="请输入中文标题" />
        </el-form-item>
        <el-form-item label="英文标题">
          <el-input v-model="bannerForm.title_en" placeholder="请输入英文标题" />
        </el-form-item>
        <el-form-item label="按钮文字(中)">
          <el-input v-model="bannerForm.button_text_zh" placeholder="请输入中文按钮文字，如：查看产品" />
        </el-form-item>
        <el-form-item label="按钮文字(英)">
          <el-input v-model="bannerForm.button_text_en" placeholder="请输入英文按钮文字，如：View Products" />
        </el-form-item>
        <el-form-item label="跳转链接">
          <el-input v-model="bannerForm.link_url" placeholder="请输入跳转链接，可选" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="bannerForm.sort_order" :min="0" style="width: 200px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="bannerForm.status">
            <el-radio :label="1">上线</el-radio>
            <el-radio :label="0">下线</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleBannerSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.settings-page {
  padding: 0;
}

.page-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.config-form {
  padding: 20px 0;
}

.banner-section {
  padding: 20px 0;
}

.banner-header {
  margin-bottom: 20px;
}

.no-image {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 50px;
  background: #f5f5f5;
  color: #999;
  font-size: 12px;
}

.banner-upload {
  display: flex;
}

.banner-preview {
  position: relative;
  width: 300px;
  height: 120px;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}

.remove-banner {
  position: absolute;
  top: 0;
  right: 0;
  width: 24px;
  height: 24px;
  background: rgba(0,0,0,0.5);
  color: #fff;
  text-align: center;
  line-height: 24px;
  cursor: pointer;
  font-size: 16px;
}

.upload-banner-btn {
  width: 300px;
  height: 120px;
  border: 1px dashed #ddd;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #999;
  font-size: 14px;
  gap: 8px;
}

.upload-banner-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.qrcode-upload {
  display: flex;
}

.qrcode-preview {
  position: relative;
  width: 200px;
  height: 200px;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
  background: #f5f5f5;
}

.remove-qrcode {
  position: absolute;
  top: 0;
  right: 0;
  width: 24px;
  height: 24px;
  background: rgba(0,0,0,0.5);
  color: #fff;
  text-align: center;
  line-height: 24px;
  cursor: pointer;
  font-size: 16px;
}

.upload-qrcode-btn {
  width: 200px;
  height: 200px;
  border: 1px dashed #ddd;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #999;
  font-size: 14px;
  gap: 8px;
}

.upload-qrcode-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.qrcode-tip {
  margin-top: 10px;
  font-size: 12px;
  color: #999;
}
</style>
