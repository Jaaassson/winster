<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { inquiryApi } from '@/admin/api'
import type { Inquiry, PaginatedData } from '@/types'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { formatDateTime } from '@/utils/date'

const loading = ref(false)
const dialogVisible = ref(false)
const currentInquiry = ref<any>(null)

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const inquiryList = ref<any[]>([])

const replyFormRef = ref<FormInstance>()
const replyForm = reactive({
  reply_content: ''
})

async function loadInquiries() {
  loading.value = true
  try {
    const res = await inquiryApi.list({
      page: pagination.page,
      page_size: pagination.page_size
    })
    if (res.code === 200 || res.code === 0) {
      inquiryList.value = res.data.items
      pagination.total = res.data.total
    }
  } catch (error) {
    console.error('获取询盘列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleView(inquiry: any) {
  currentInquiry.value = inquiry
  dialogVisible.value = true
  if (inquiry.is_read === 0) {
    inquiry.is_read = 1
  }
}

async function handleMarkReplied(id: number) {
  try {
    const res = await inquiryApi.markReplied(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('标记已回复成功')
      dialogVisible.value = false
      loadInquiries()
    }
  } catch (error) {
    console.error('标记已回复失败:', error)
  }
}

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这条询盘吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const res = await inquiryApi.delete(id)
    if (res.code === 200 || res.code === 0) {
      ElMessage.success('删除成功')
      loadInquiries()
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
  loadInquiries()
}

function handleCurrentChange(page: number) {
  pagination.page = page
  loadInquiries()
}

function getStatusTag(is_replied: number) {
  return is_replied === 1 ? 'success' : 'warning'
}

function getStatusText(is_replied: number) {
  return is_replied === 1 ? '已回复' : '待回复'
}

onMounted(() => {
  loadInquiries()
})
</script>

<template>
  <div class="inquiries-page">
    <el-card class="page-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">询盘管理</span>
        </div>
      </template>
      
      <el-table :data="inquiryList" v-loading="loading" style="width: 100%" :header-cell-style="{ backgroundColor: '#f5f7fa' }">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="customer_name" label="客户姓名" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" show-overflow-tooltip />
        <el-table-column prop="country" label="国家" width="100" />
        <el-table-column prop="quantity" label="数量" width="90" align="center" />
        <el-table-column prop="message" label="询盘内容" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.is_replied)" size="small">
              {{ getStatusText(row.is_replied) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="170">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
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

    <el-dialog
      v-model="dialogVisible"
      title="询盘详情"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="currentInquiry" class="inquiry-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="客户姓名">{{ currentInquiry.customer_name }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentInquiry.email }}</el-descriptions-item>
          <el-descriptions-item label="国家">{{ currentInquiry.country || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数量">{{ currentInquiry.quantity || '-' }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusTag(currentInquiry.is_replied)" size="small">
              {{ getStatusText(currentInquiry.is_replied) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ formatDateTime(currentInquiry.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="询盘内容" :span="2">
            <div class="message-content">{{ currentInquiry.message }}</div>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button v-if="currentInquiry?.is_replied === 0" type="primary" @click="handleMarkReplied(currentInquiry.id)">标记已回复</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.inquiries-page {
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

.inquiry-detail {
  padding: 10px 0;
}

.message-content {
  white-space: pre-wrap;
  line-height: 1.6;
  min-height: 80px;
}
</style>
