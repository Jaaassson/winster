<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { newsApi } from '@/admin/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDateTime } from '@/utils/date'

const loading = ref(false)

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const newsList = ref<any[]>([])

async function loadNews() {
  loading.value = true
  try {
    const res = await newsApi.list({
      page: pagination.page,
      page_size: pagination.page_size
    })
    if (res.code === 200 || res.code === 0) {
      newsList.value = res.data.items
      pagination.total = res.data.total
    }
  } catch (error) {
    console.error('获取新闻列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  ElMessage.info('添加新闻功能开发中')
}

function handleEdit(row: any) {
  ElMessage.info('编辑新闻功能开发中')
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

function handleSizeChange(size: number) {
  pagination.page_size = size
  pagination.page = 1
  loadNews()
}

function handleCurrentChange(page: number) {
  pagination.page = page
  loadNews()
}

function getStatusTag(status: number) {
  return status === 1 ? 'success' : 'info'
}

function getStatusText(status: number) {
  return status === 1 ? '已上线' : '未上线'
}

onMounted(() => {
  loadNews()
})
</script>

<template>
  <div class="news-page">
    <el-card class="page-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">新闻管理</span>
          <el-button type="primary" @click="handleAdd">添加新闻</el-button>
        </div>
      </template>
      
      <el-table :data="newsList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
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
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
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
    </el-card>
  </div>
</template>

<style scoped>
.news-page {
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

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
