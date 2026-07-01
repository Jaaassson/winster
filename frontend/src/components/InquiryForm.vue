<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { inquiryApi } from '@/api'

const props = defineProps<{
  productId?: number | string
  productName?: string
}>()

const emit = defineEmits<{
  success: []
  error: []
}>()

const { t } = useI18n()
const route = useRoute()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  customer_name: '',
  email: '',
  country: '',
  quantity: '',
  message: '',
  product_id: '' as number | string | ''
})

onMounted(() => {
  if (props.productId) {
    form.product_id = props.productId
  } else if (route.query.product_id) {
    form.product_id = route.query.product_id as string
  }
  if (props.productName) {
    form.message = `${t('common.message')}: ${props.productName}\n\n`
  }
})

const rules = computed<FormRules>(() => ({
  customer_name: [
    { required: true, message: t('common.required'), trigger: 'blur' },
    { min: 2, max: 50, message: t('common.required'), trigger: 'blur' }
  ],
  email: [
    { required: true, message: t('common.required'), trigger: 'blur' },
    { type: 'email', message: t('common.invalidEmail'), trigger: 'blur' }
  ],
  country: [
    { max: 100, message: t('common.required'), trigger: 'blur' }
  ],
  quantity: [
    { max: 50, message: t('common.required'), trigger: 'blur' }
  ],
  message: [
    { max: 1000, message: t('common.required'), trigger: 'blur' }
  ]
}))

async function onSubmit() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    return
  }

  loading.value = true
  try {
    const submitData: any = {
      customer_name: form.customer_name,
      email: form.email,
      country: form.country,
      quantity: form.quantity,
      message: form.message
    }

    if (form.product_id) {
      submitData.product_id = form.product_id
    }

    await inquiryApi.submit(submitData)
    ElMessage.success(t('common.success'))

    form.customer_name = ''
    form.email = ''
    form.country = ''
    form.quantity = ''
    form.message = ''

    formRef.value?.resetFields()
    emit('success')
  } catch (error: any) {
    console.error('Inquiry submission failed:', error)
    ElMessage.error(error?.message || 'Submission failed, please try again')
    emit('error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="inquiry-form-wrapper">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="inquiry-form"
      @submit.prevent="onSubmit"
    >
      <el-form-item :label="t('common.name')" prop="customer_name">
        <el-input
          v-model="form.customer_name"
          :placeholder="t('common.name')"
          size="large"
          clearable
        />
      </el-form-item>

      <el-form-item :label="t('common.email')" prop="email">
        <el-input
          v-model="form.email"
          type="email"
          :placeholder="t('common.email')"
          size="large"
          clearable
        />
      </el-form-item>

      <el-form-item :label="t('common.country')" prop="country">
        <el-input
          v-model="form.country"
          :placeholder="t('common.country')"
          size="large"
          clearable
        />
      </el-form-item>

      <el-form-item :label="t('common.quantity')" prop="quantity">
        <el-input
          v-model="form.quantity"
          :placeholder="t('common.quantity')"
          size="large"
          clearable
        />
      </el-form-item>

      <el-form-item :label="t('common.message')" prop="message">
        <el-input
          v-model="form.message"
          type="textarea"
          :rows="5"
          :placeholder="t('common.message')"
          maxlength="1000"
          show-word-limit
          resize="none"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="onSubmit"
          class="submit-btn"
        >
          <el-icon><Promotion /></el-icon>
          <span>{{ t('common.submit') }}</span>
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped lang="scss">
.inquiry-form-wrapper {
  .inquiry-form {
    :deep(.el-form-item__label) {
      font-weight: 500;
      color: #333;
    }

    :deep(.el-input__wrapper) {
      border-radius: 6px;
      box-shadow: 0 0 0 1px #dcdfe6 inset;
      transition: all 0.2s ease;

      &:hover {
        box-shadow: 0 0 0 1px #1a73e8 inset;
      }

      &.is-focus {
        box-shadow: 0 0 0 1px #1a73e8 inset;
      }
    }

    :deep(.el-textarea__inner) {
      border-radius: 6px;
      transition: all 0.2s ease;

      &:hover {
        border-color: #1a73e8;
      }

      &:focus {
        border-color: #1a73e8;
      }
    }

    .submit-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 160px;
      height: 44px;
      font-size: 16px;
      font-weight: 500;
      border-radius: 6px;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
      }
    }
  }
}

@media (max-width: 768px) {
  .inquiry-form-wrapper {
    .inquiry-form {
      :deep(.el-form-item) {
        margin-bottom: 18px;
      }

      :deep(.el-form-item__label) {
        width: 100% !important;
        text-align: left;
        margin-bottom: 6px;
      }

      :deep(.el-form-item__content) {
        margin-left: 0 !important;
      }

      .submit-btn {
        width: 100%;
      }
    }
  }
}
</style>
