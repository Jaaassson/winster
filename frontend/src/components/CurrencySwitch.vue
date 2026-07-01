<script setup lang="ts">
import { useCurrencyStore } from '@/store/currency'
import { ref } from 'vue'
import { ElDropdown } from 'element-plus'

const currencyStore = useCurrencyStore()
const dropdownRef = ref<InstanceType<typeof ElDropdown> | null>(null)

const currencies = [
  { value: 'USD', label: 'USD', symbol: '$', icon: '💵' },
  { value: 'CNY', label: 'CNY', symbol: '¥', icon: '💴' }
]

function handleCommand(command: string | number | object) {
  currencyStore.set(command as string)
}

function getCurrentCurrency() {
  return currencies.find(c => c.value === currencyStore.currency) || currencies[0]
}
</script>

<template>
  <el-dropdown ref="dropdownRef" @command="handleCommand" trigger="click">
    <span class="currency-switch">
      <span class="currency-icon">{{ getCurrentCurrency().icon }}</span>
      <span class="currency-label">{{ getCurrentCurrency().label }}</span>
      <el-icon class="currency-arrow"><ArrowDown /></el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
          v-for="currency in currencies"
          :key="currency.value"
          :command="currency.value"
          :disabled="currency.value === currencyStore.currency"
        >
          <span class="dropdown-currency-icon">{{ currency.icon }}</span>
          {{ currency.label }} ({{ currency.symbol }})
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<style scoped lang="scss">
.currency-switch {
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

  .currency-icon {
    font-size: 16px;
  }

  .currency-label {
    font-weight: 500;
  }

  .currency-arrow {
    font-size: 12px;
    transition: transform 0.2s ease;
  }
}

.dropdown-currency-icon {
  margin-right: 8px;
}
</style>
