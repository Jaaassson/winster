<script setup lang="ts">
import { useLangStore } from '@/store/lang'
import { ref } from 'vue'
import { ElDropdown } from 'element-plus'

const langStore = useLangStore()
const dropdownRef = ref<InstanceType<typeof ElDropdown> | null>(null)

const languages = [
  { value: 'en', label: 'English', icon: '🇺🇸' },
  { value: 'zh', label: '中文', icon: '🇨🇳' }
]

function handleCommand(command: string | number | object) {
  langStore.set(command as string)
}

function getCurrentLang() {
  return languages.find(l => l.value === langStore.lang) || languages[0]
}
</script>

<template>
  <el-dropdown ref="dropdownRef" @command="handleCommand" trigger="click">
    <span class="lang-switch">
      <span class="lang-icon">{{ getCurrentLang().icon }}</span>
      <span class="lang-label">{{ getCurrentLang().label }}</span>
      <el-icon class="lang-arrow"><ArrowDown /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
          v-for="lang in languages"
          :key="lang.value"
          :command="lang.value"
          :disabled="lang.value === langStore.lang"
        >
          <span class="dropdown-lang-icon">{{ lang.icon }}</span>
          {{ lang.label }}
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped lang="scss">
.lang-switch {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  background: #f2f6ff;
  color: #1a73e8;
  font-size: 14px;
  transition: all 0.2s ease;

  &:hover {
    background: #e0ecff;
  }

  .lang-icon {
    font-size: 16px;
  }

  .lang-label {
    font-weight: 500;
  }

  .lang-arrow {
    font-size: 12px;
    transition: transform 0.2s ease;
  }
}

.dropdown-lang-icon {
  margin-right: 8px;
}
</style>
