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
  site_name: '',
  site_title: '',
  keywords: '',
  description: '',
  company_name: '',
  phone: '',
  email: '',
  address: '',
  about_us: '',
  facebook: '',
  twitter: '',
  linkedin: '',
  instagram: ''
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

async function loadConfig() {
  loading.value = true
  try {
    const res = await siteConfigApi.get()
    if ((res.code === 200 || res.code === 0) && res.data) {
      Object.assign(configForm, res.data)
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
    const res = await siteConfigApi.update(configForm)
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
                <el-form-item label="网站名称">
                  <el-input v-model="configForm.site_name" placeholder="请输入网站名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="网站标题">
                  <el-input v-model="configForm.site_title" placeholder="请输入网站标题" />
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
                <el-form-item label="公司名称">
                  <el-input v-model="configForm.company_name" placeholder="请输入公司名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="联系电话">
                  <el-input v-model="configForm.phone" placeholder="请输入联系电话" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="邮箱">
                  <el-input v-model="configForm.email" placeholder="请输入联系邮箱" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="地址">
                  <el-input v-model="configForm.address" placeholder="请输入地址" />
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
            <el-form-item label="关于我们">
              <el-input
                v-model="configForm.about_us"
                type="textarea"
                :rows="10"
                placeholder="请输入关于我们内容"
              />
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
              <el-table-column label="操作" width="140" fixed="right" align="center">
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
</style>
