<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { productApi, categoryApi, uploadApi } from '@/admin/api'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { Plus, Edit, Delete, Search, Upload, Switch } from '@element-plus/icons-vue'

const loading = ref(false)
const productList = ref<any[]>([])
const categoryList = ref<any[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加产品')
const formRef = ref<FormInstance>()
const editingId = ref<number | null>(null)
const activeTab = ref('basic')

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const searchForm = reactive({
  keyword: '',
  category_id: null as number | null,
  status: null as number | null
})

const form = reactive({
  category_id: null as number | null,
  name_zh: '',
  name_en: '',
  model: '',
  desc_zh: '',
  desc_en: '',
  images: [] as string[],
  price_usd: 0,
  price_cny: 0,
  stock: 0,
  moq: 1,
  packaging_zh: '',
  packaging_en: '',
  sort_order: 0,
  is_hot: 0,
  status: 1
})

async function loadCategories() {
  try {
    const res = await categoryApi.list()
    if (res.code === 200 || res.code === 0) {
      categoryList.value = res.data || []
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

async function loadProducts() {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (searchForm.keyword) params.keyword = searchForm.keyword
    if (searchForm.category_id) params.category_id = searchForm.category_id
    if (searchForm.status !== null) params.status = searchForm.status
    
    const res = await productApi.list(params)
    if (res.code === 200 || res.code === 0) {
      productList.value = res.data.items || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取产品列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  loadProducts()
}

function handleReset() {
  searchForm.keyword = ''
  searchForm.category_id = null
  searchForm.status = null
  pagination.page = 1
  loadProducts()
}

function handleAdd() {
  editingId.value = null
  dialogTitle.value = '添加产品'
  activeTab.value = 'basic'
  resetForm()
  dialogVisible.value = true
}

function resetForm() {
  form.category_id = null
  form.name_zh = ''
  form.name_en = ''
  form.model = ''
  form.desc_zh = ''
  form.desc_en = ''
  form.images = []
  form.price_usd = 0
  form.price_cny = 0
  form.stock = 0
  form.moq = 1
  form.packaging_zh = ''
  form.packaging_en = ''
  form.sort_order = 0
  form.is_hot = 0
  form.status = 1
}

function handleEdit(row: any) {
  editingId.value = row.id
  dialogTitle.value = '编辑产品'
  activeTab.value = 'basic'
  form.category_id = row.category_id
  form.name_zh = row.name_i18n?.['zh-CN'] || row.name || ''
  form.name_en = row.name_i18n?.['en-US'] || row.name || ''
  form.model = row.model || ''
  form.desc_zh = row.description_i18n?.['zh-CN'] || row.description || ''
  form.desc_en = row.description_i18n?.['en-US'] || row.description || ''
  form.images = row.images || []
  form.price_usd = row.price_usd || 0
  form.price_cny = row.price_cny || 0
  form.stock = row.stock || 0
  form.moq = row.moq || 1
  form.packaging_zh = row.packaging_i18n?.['zh-CN'] || row.packaging || ''
  form.packaging_en = row.packaging_i18n?.['en-US'] || row.packaging || ''
  form.sort_order = row.sort_order || 0
  form.is_hot = Number(row.is_hot) || 0
  form.status = row.status !== undefined ? Number(row.status) : 1
  dialogVisible.value = true
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这个产品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await productApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('删除成功')
      loadProducts()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

async function handleToggleStatus(row: any) {
  try {
    const res = await productApi.toggleStatus(row.id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success(row.status === 1 ? '下架成功' : '上架成功')
      loadProducts()
    }
  } catch (error) {
    console.error('操作失败:', error)
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    const data = {
      category_id: form.category_id,
      name: {
        'zh-CN': form.name_zh,
        'en-US': form.name_en
      },
      model: form.model,
      description: {
        'zh-CN': form.desc_zh,
        'en-US': form.desc_en
      },
      images: form.images,
      price_usd: form.price_usd,
      price_cny: form.price_cny,
      stock: form.stock,
      moq: form.moq,
      packaging: {
        'zh-CN': form.packaging_zh,
        'en-US': form.packaging_en
      },
      sort_order: form.sort_order,
      is_hot: form.is_hot,
      status: form.status
    }

    try {
      let res
      if (editingId.value) {
        res = await productApi.update(editingId.value, data)
      } else {
        res = await productApi.create(data)
      }
      if (res.code === 200 || res.code === 0 || res.code === 201) {
        ElMessage.success(editingId.value ? '更新成功' : '创建成功')
        dialogVisible.value = false
        loadProducts()
      }
    } catch (error) {
      console.error('提交失败:', error)
    }
  })
}

async function handleUpload(options: any) {
  const { file, onSuccess, onError } = options
  try {
    const res = await uploadApi.image(file)
    if (res.code === 200 || res.code === 0) {
      form.images.push(res.data.url)
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

function handleRemoveImage(index: number) {
  form.images.splice(index, 1)
}

function getStatusTag(status: number) {
  return status === 1 ? 'success' : 'info'
}

function getStatusText(status: number) {
  return status === 1 ? '上架' : '下架'
}

function handleSizeChange(size: number) {
  pagination.page_size = size
  pagination.page = 1
  loadProducts()
}

function handleCurrentChange(page: number) {
  pagination.page = page
  loadProducts()
}

const flatCategories = computed(() => {
  const result: any[] = []
  function flatten(list: any[], level = 0) {
    list.forEach(item => {
      result.push({
        id: item.id,
        name: '  '.repeat(level) + item.name
      })
      if (item.children && item.children.length > 0) {
        flatten(item.children, level + 1)
      }
    })
  }
  flatten(categoryList.value)
  return result
})

function getCategoryName(categoryId: number): string {
  const cat = flatCategories.value.find(c => c.id === categoryId)
  return cat ? cat.name.trim() : '-'
}

onMounted(() => {
  loadCategories()
  loadProducts()
})
</script>

<template>
  <div class="product-page">
    <div class="page-header">
      <h2>产品管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd">添加产品</el-button>
    </div>

    <div class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="产品名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="searchForm.category_id"
            placeholder="全部分类"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="cat in flatCategories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="全部状态"
            clearable
            style="width: 150px"
          >
            <el-option label="上架" :value="1" />
            <el-option label="下架" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="page-content">
      <el-table :data="productList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column label="图片" width="90">
          <template #default="{ row }">
            <el-image
              v-if="row.images && row.images.length > 0"
              :src="row.images[0]"
              style="width: 50px; height: 50px"
              fit="cover"
            />
            <span v-else class="no-image">无图</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="产品名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="model" label="型号" width="120" show-overflow-tooltip />
        <el-table-column label="分类" width="220">
          <template #default="{ row }">
            {{ getCategoryName(row.category_id) }}
          </template>
        </el-table-column>
        <el-table-column label="价格(USD)" width="100">
          <template #default="{ row }">${{ row.price_usd }}</template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="moq" label="MOQ" width="80" />
        <el-table-column label="热门" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.is_hot" type="danger" size="small">热门</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleToggleStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button type="primary" link :icon="Edit" @click="handleEdit(row)">编辑</el-button>
              <el-button type="danger" link :icon="Delete" @click="handleDelete(row.id)">删除</el-button>
            </div>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无产品数据" />
        </template>
      </el-table>

      <div class="pagination">
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px" top="5vh">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-form ref="formRef" :model="form" label-width="100px">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="所属分类" prop="category_id" :rules="[{ required: true, message: '请选择分类', trigger: 'change' }]">
                  <el-tree-select
                    v-model="form.category_id"
                    :data="categoryList"
                    :props="{ label: 'name', value: 'id', children: 'children' }"
                    check-strictly
                    :render-after-expand="false"
                    placeholder="请选择分类"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="中文名称" prop="name_zh" :rules="[{ required: true, message: '请输入中文名称', trigger: 'blur' }]">
                  <el-input v-model="form.name_zh" placeholder="请输入中文名称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="英文名称" prop="name_en" :rules="[{ required: true, message: '请输入英文名称', trigger: 'blur' }]">
                  <el-input v-model="form.name_en" placeholder="请输入英文名称" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="型号">
                  <el-input v-model="form.model" placeholder="请输入型号" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="排序">
                  <el-input-number v-model="form.sort_order" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="美元价格">
                  <el-input-number v-model="form.price_usd" :min="0" :precision="2" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="人民币价格">
                  <el-input-number v-model="form.price_cny" :min="0" :precision="2" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="库存">
                  <el-input-number v-model="form.stock" :min="0" style="width: 100%" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="起订量(MOQ)">
                  <el-input-number v-model="form.moq" :min="1" style="width: 100%" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="是否热门">
                  <el-switch v-model="form.is_hot" :active-value="1" :inactive-value="0" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="状态">
                  <el-radio-group v-model="form.status">
                    <el-radio :label="1">上架</el-radio>
                    <el-radio :label="0">下架</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="产品描述" name="desc">
          <el-form :model="form" label-width="100px">
            <el-form-item label="中文描述">
              <el-input
                v-model="form.desc_zh"
                type="textarea"
                :rows="10"
                placeholder="请输入中文描述"
              />
            </el-form-item>
            <el-form-item label="英文描述">
              <el-input
                v-model="form.desc_en"
                type="textarea"
                :rows="10"
                placeholder="请输入英文描述"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="产品图片" name="images">
          <el-form :model="form" label-width="100px">
            <el-form-item label="产品图片">
              <div class="image-uploader">
                <div class="image-list">
                  <div
                    v-for="(img, index) in form.images"
                    :key="index"
                    class="image-item"
                  >
                    <el-image :src="img" fit="cover" style="width: 100%; height: 100%" />
                    <span class="remove-btn" @click="handleRemoveImage(index)">×</span>
                  </div>
                </div>
                <el-upload
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
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="包装信息" name="packaging">
          <el-form :model="form" label-width="100px">
            <el-form-item label="中文包装">
              <el-input
                v-model="form.packaging_zh"
                type="textarea"
                :rows="6"
                placeholder="请输入中文包装信息"
              />
            </el-form-item>
            <el-form-item label="英文包装">
              <el-input
                v-model="form.packaging_en"
                type="textarea"
                :rows="6"
                placeholder="请输入英文包装信息"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.product-page {
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
.search-bar {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}
.page-content {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.no-image {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: #f5f5f5;
  color: #999;
  font-size: 12px;
}
.image-uploader {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.image-item {
  position: relative;
  width: 100px;
  height: 100px;
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}
.remove-btn {
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
.upload-btn {
  width: 100px;
  height: 100px;
  border: 1px dashed #ddd;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #999;
  font-size: 12px;
  gap: 4px;
}
.upload-btn:hover {
  border-color: #409eff;
  color: #409eff;
}
.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
