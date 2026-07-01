<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { categoryApi, uploadApi } from '@/admin/api'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Edit, Delete, Upload } from '@element-plus/icons-vue'
import { formatDateTime } from '@/utils/date'

const loading = ref(false)
const categoryList = ref<any[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加分类')
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)

const form = reactive({
  parent_id: 0,
  name_zh: '',
  name_en: '',
  image: '',
  sort_order: 0,
  status: 1
})

function convertStatusToNumber(categories: any[]): any[] {
  return categories.map(cat => {
    cat.status = Number(cat.status)
    if (cat.children && cat.children.length > 0) {
      cat.children = convertStatusToNumber(cat.children)
    }
    return cat
  })
}

async function loadCategories() {
  loading.value = true
  try {
    const res = await categoryApi.list()
    if (res.code === 200 || res.code === 0) {
      categoryList.value = convertStatusToNumber(res.data || [])
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleAdd(parentId: number = 0) {
  editingId.value = null
  dialogTitle.value = '添加分类'
  form.parent_id = parentId
  form.name_zh = ''
  form.name_en = ''
  form.image = ''
  form.sort_order = 0
  form.status = 1
  dialogVisible.value = true
}

function handleEdit(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑分类'
  form.parent_id = row.parent_id || 0
  form.name_zh = row.name_i18n?.['zh-CN'] || row.name || ''
  form.name_en = row.name_i18n?.['en-US'] || row.name || ''
  form.image = row.image || ''
  form.sort_order = row.sort_order || 0
  form.status = Number(row.status) ?? 1
  dialogVisible.value = true
}

async function handleToggleStatus(row: any) {
  try {
    const res = await categoryApi.toggleStatus(row.id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('状态更新成功')
      loadCategories()
    }
  } catch (error) {
    console.error('状态更新失败:', error)
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这个分类吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await categoryApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('删除成功')
      loadCategories()
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
      parent_id: form.parent_id,
      name: {
        'zh-CN': form.name_zh,
        'en-US': form.name_en
      },
      image: form.image,
      sort_order: form.sort_order,
      status: form.status
    }

    try {
      let res
      if (editingId.value) {
        res = await categoryApi.update(editingId.value, data)
      } else {
        res = await categoryApi.create(data)
      }
      if (res.code === 200 || res.code === 0 || res.code === 201) {
        ElMessage.success(editingId.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        loadCategories()
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
  return status === 1 ? '启用' : '禁用'
}

async function handleUpload(options: any) {
  const { file, onSuccess, onError } = options
  try {
    const res = await uploadApi.image(file)
    if (res.code === 200 || res.code === 0) {
      form.image = res.data.url
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
  form.image = ''
}

onMounted(() => {
  loadCategories()
})
</script>

<template>
  <div class="category-page">
    <div class="page-header">
      <h2>分类管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd()">添加分类</el-button>
    </div>

    <div class="page-content">
      <el-table :data="categoryList" v-loading="loading" row-key="id" default-expand-all style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分类名称" min-width="200" />
        <el-table-column label="图片" width="100">
          <template #default="{ row }">
            <el-image
              v-if="row.image"
              :src="row.image"
              :preview-src-list="[row.image]"
              fit="cover"
              style="width: 60px; height: 60px; border-radius: 4px;"
            />
            <span v-else style="color: #999;">暂无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleToggleStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <div class="action-btns">
              <el-button type="primary" link :icon="Plus" @click="handleAdd(row.id)">添加子分类</el-button>
              <el-button type="primary" link :icon="Edit" @click="handleEdit(row)">编辑</el-button>
              <el-button type="danger" link :icon="Delete" @click="handleDelete(row.id)">删除</el-button>
            </div>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无分类数据" />
        </template>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="父级分类">
          <el-tree-select
            v-model="form.parent_id"
            :data="categoryList"
            :props="{ label: 'name', value: 'id', children: 'children' }"
            check-strictly
            :render-after-expand="false"
            placeholder="顶级分类"
            clearable
          />
        </el-form-item>
        <el-form-item label="中文名称" prop="name_zh" :rules="[{ required: true, message: '请输入中文名称', trigger: 'blur' }]">
          <el-input v-model="form.name_zh" placeholder="请输入中文名称" />
        </el-form-item>
        <el-form-item label="英文名称" prop="name_en" :rules="[{ required: true, message: '请输入英文名称', trigger: 'blur' }]">
          <el-input v-model="form.name_en" placeholder="请输入英文名称" />
        </el-form-item>
        <el-form-item label="分类图片">
          <div class="image-upload-container">
            <div v-if="form.image" class="image-preview">
              <el-image :src="form.image" fit="cover" style="width: 100px; height: 100px; border-radius: 4px;" />
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
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
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
.category-page {
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

.action-btns {
  display: flex;
  flex-wrap: nowrap;
  gap: 4px;
  white-space: nowrap;
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
