<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { newsApi, uploadApi } from '@/admin/api'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Edit, Delete, Upload } from '@element-plus/icons-vue'
import { formatDateTime } from '@/utils/date'
import { getI18nValue } from '@/utils/i18n'
import { useLangStore } from '@/store/lang'

const langStore = useLangStore()
const loading = ref(false)
const newsList = ref<any[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加新闻')
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const form = reactive({
  title_zh: '',
  title_en: '',
  content_zh: '',
  content_en: '',
  cover_image: '',
  sort_order: 0,
  status: 1
})

function getNewsTitle(news: any) {
  return getI18nValue(news.title)
}

async function loadNews() {
  loading.value = true
  try {
    const res = await newsApi.list({
      page: pagination.page,
      page_size: pagination.page_size
    })
    if (res.code === 200 || res.code === 0) {
      newsList.value = res.data.items || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取新闻列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  editingId.value = null
  dialogTitle.value = '添加新闻'
  form.title_zh = ''
  form.title_en = ''
  form.content_zh = ''
  form.content_en = ''
  form.cover_image = ''
  form.sort_order = 0
  form.status = 1
  dialogVisible.value = true
}

function handleEdit(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑新闻'
  const titleObj = safeParseJSON(row.title)
  const contentObj = safeParseJSON(row.content)
  form.title_zh = titleObj?.['zh-CN'] || row.title || ''
  form.title_en = titleObj?.['en-US'] || ''
  form.content_zh = contentObj?.['zh-CN'] || row.content || ''
  form.content_en = contentObj?.['en-US'] || ''
  form.cover_image = row.cover_image || ''
  form.sort_order = row.sort_order || 0
  form.status = Number(row.status) ?? 1
  dialogVisible.value = true
}

function safeParseJSON(str: string): any {
  if (!str) return null
  if (typeof str !== 'string') return str
  try {
    return JSON.parse(str)
  } catch {
    return null
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这条新闻吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await newsApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('删除成功')
      loadNews()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return

    const data = {
      title: JSON.stringify({
        'zh-CN': form.title_zh,
        'en-US': form.title_en
      }),
      content: JSON.stringify({
        'zh-CN': form.content_zh,
        'en-US': form.content_en
      }),
      cover_image: form.cover_image,
      sort_order: form.sort_order,
      status: form.status
    }

    try {
      let res
      if (editingId.value) {
        res = await newsApi.update(editingId.value, data)
      } else {
        res = await newsApi.create(data)
      }
      if (res.code === 200 || res.code === 0 || res.code === 201) {
        ElMessage.success(editingId.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        loadNews()
      }
    } catch (error) {
      console.error('提交失败:', error)
    }
  })
}

function getStatusTag(status: number) {
  return status === 1 ? 'success' : 'info'
}

function getStatusText(status: number) {
  return status === 1 ? '已上线' : '未上线'
}

function handleSizeChange(size: number) {
  pagination.page_size = size
  pagination.page = 1
  loadNews()
}

function handleCurrentChange(page: number) {
  pagination.page = page
  loadNews()
}

async function handleUpload(options: any) {
  const { file, onSuccess, onError } = options
  try {
    const res = await uploadApi.image(file)
    if (res.code === 200 || res.code === 0) {
      form.cover_image = res.data.url
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

function handleRemoveImage() {
  form.cover_image = ''
}

onMounted(() => {
  loadNews()
})
</script>

<template>
  <div class="news-page">
    <div class="page-header">
      <h2>新闻管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd">添加新闻</el-button>
    </div>

    <div class="page-content">
      <el-table :data="newsList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="标题" min-width="280">
          <template #default="{ row }">
            <span :title="getNewsTitle(row)">{{ getNewsTitle(row) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="封面" width="100">
          <template #default="{ row }">
            <el-image
              v-if="row.cover_image"
              :src="row.cover_image"
              :preview-src-list="[row.cover_image]"
              fit="cover"
              style="width: 60px; height: 60px; border-radius: 4px;"
            />
            <span v-else style="color: #999;">无</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link :icon="Edit" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link :icon="Delete" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无新闻数据" />
        </template>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px">
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="中文标题" prop="title_zh" :rules="[{ required: true, message: '请输入中文标题', trigger: 'blur' }]">
          <el-input v-model="form.title_zh" placeholder="请输入中文标题" />
        </el-form-item>
        <el-form-item label="英文标题" prop="title_en" :rules="[{ required: true, message: '请输入英文标题', trigger: 'blur' }]">
          <el-input v-model="form.title_en" placeholder="请输入英文标题" />
        </el-form-item>
        <el-form-item label="封面图">
          <div class="image-upload-container">
            <div v-if="form.cover_image" class="image-preview">
              <el-image :src="form.cover_image" fit="cover" style="width: 100px; height: 100px; border-radius: 4px;" />
              <div class="image-actions">
                <el-button type="danger" size="small" @click="handleRemoveImage">删除</el-button>
              </div>
            </div>
            <el-upload
              v-else
              action="#"
              :show-file-list="false"
              :http-request="handleUpload"
              accept="image/*"
            >
              <div class="upload-btn">
                <el-icon><Upload /></el-icon>
                <span>上传图片</span>
              </div>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="中文内容" prop="content_zh">
          <el-input
            v-model="form.content_zh"
            type="textarea"
            :rows="6"
            placeholder="请输入中文内容"
          />
        </el-form-item>
        <el-form-item label="英文内容" prop="content_en">
          <el-input
            v-model="form.content_en"
            type="textarea"
            :rows="6"
            placeholder="请输入英文内容"
          />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">已上线</el-radio>
            <el-radio :label="0">未上线</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.news-page {
  padding: 20px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h2 {
  margin: 0;
  font-size: 20px;
}
.page-content {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.image-upload-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.image-preview {
  display: flex;
  align-items: center;
  gap: 10px;
}

.image-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.upload-btn {
  width: 100px;
  height: 100px;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-btn:hover {
  border-color: #409eff;
}

.upload-btn .el-icon {
  font-size: 28px;
  color: #8c939d;
  margin-bottom: 5px;
}

.upload-btn span {
  font-size: 12px;
  color: #8c939d;
}
</style>
