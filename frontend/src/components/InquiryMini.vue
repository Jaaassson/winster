<template>
  <div class="card" style="margin-top:16px;">
    <h3>{{ t("inquiry.title") }}</h3>
    <el-form :model="form" label-width="120px" @submit.prevent>
      <el-form-item :label="t('inquiry.name')" required><el-input v-model="form.customer_name" /></el-form-item>
      <el-form-item :label="t('inquiry.email')" required><el-input v-model="form.email" /></el-form-item>
      <el-form-item :label="t('inquiry.country')"><el-input v-model="form.country" /></el-form-item>
      <el-form-item :label="t('inquiry.message')"><el-input v-model="form.message" type="textarea" :rows="4" /></el-form-item>
      <el-form-item><el-button type="primary" :loading="loading" @click="onSubmit">{{ t("common.submit") }}</el-button></el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useI18n } from "vue-i18n";
import { ElMessage } from "element-plus";
import { inquiryApi } from "@/api";
const { t } = useI18n();
const form = reactive<any>({ customer_name: "", email: "", country: "", message: "" });
const loading = ref(false);
async function onSubmit() {
  if (!form.customer_name || !form.email) return ElMessage.warning("required");
  loading.value = true;
  try { await inquiryApi.submit(form); ElMessage.success(t("inquiry.submitSuccess")); Object.assign(form, { customer_name: "", email: "", country: "", message: "" }); }
  catch { ElMessage.error(t("inquiry.submitFailed")); }
  finally { loading.value = false; }
}
</script>