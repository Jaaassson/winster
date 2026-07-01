<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'

interface CarouselImage {
  url: string
  alt?: string
  link?: string
}

const props = withDefaults(defineProps<{
  images: CarouselImage[]
  height?: string
  autoplay?: boolean
  interval?: number
  showArrows?: boolean
  showIndicators?: boolean
  rounded?: boolean
}>(), {
  height: '400px',
  autoplay: true,
  interval: 4000,
  showArrows: true,
  showIndicators: true,
  rounded: false
})

const emit = defineEmits<{
  change: [index: number]
}>()

const currentIndex = ref(0)
let autoplayTimer: ReturnType<typeof setInterval> | null = null

const validImages = computed(() => props.images.filter(img => img && img.url))

const totalSlides = computed(() => validImages.value.length)

function next() {
  if (totalSlides.value === 0) return
  currentIndex.value = (currentIndex.value + 1) % totalSlides.value
  emit('change', currentIndex.value)
}

function prev() {
  if (totalSlides.value === 0) return
  currentIndex.value = (currentIndex.value - 1 + totalSlides.value) % totalSlides.value
  emit('change', currentIndex.value)
}

function goTo(index: number) {
  if (index < 0 || index >= totalSlides.value) return
  currentIndex.value = index
  emit('change', currentIndex.value)
}

function startAutoplay() {
  if (!props.autoplay || totalSlides.value <= 1) return
  stopAutoplay()
  autoplayTimer = setInterval(() => {
    next()
  }, props.interval)
}

function stopAutoplay() {
  if (autoplayTimer) {
    clearInterval(autoplayTimer)
    autoplayTimer = null
  }
}

function handleMouseEnter() {
  stopAutoplay()
}

function handleMouseLeave() {
  startAutoplay()
}

watch(() => props.images, () => {
  currentIndex.value = 0
  startAutoplay()
}, { deep: true })

onMounted(() => {
  startAutoplay()
})

onBeforeUnmount(() => {
  stopAutoplay()
})
</script>

<template>
  <div
    class="image-carousel"
    :class="{ 'rounded': rounded }"
    :style="{ height }"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div class="carousel-track">
      <div
        v-for="(image, index) in validImages"
        :key="index"
        class="carousel-slide"
        :class="{ active: index === currentIndex }"
        :style="{ height }"
      >
        <img
          :src="image.url"
          :alt="image.alt || ''"
          class="carousel-image"
        />
      </div>
    </div>

    <button
      v-if="showArrows && totalSlides > 1"
      class="carousel-arrow arrow-prev"
      @click="prev"
    >
      <el-icon><ArrowLeft /></el-icon>
    </button>

    <button
      v-if="showArrows && totalSlides > 1"
      class="carousel-arrow arrow-next"
      @click="next"
    >
      <el-icon><ArrowRight /></el-icon>
    </button>

    <div v-if="showIndicators && totalSlides > 1" class="carousel-indicators">
      <button
        v-for="(_, index) in validImages"
        :key="index"
        class="indicator-dot"
        :class="{ active: index === currentIndex }"
        @click="goTo(index)"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.image-carousel {
  position: relative;
  width: 100%;
  overflow: hidden;
  background: #f5f7fa;

  &.rounded {
    border-radius: 8px;
  }

  .carousel-track {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .carousel-slide {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.6s ease;
    pointer-events: none;

    &.active {
      opacity: 1;
      pointer-events: auto;
    }

    .carousel-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .carousel-arrow {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.9);
    border: none;
    color: #333;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    opacity: 0;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

    &:hover {
      background: #1a73e8;
      color: #fff;
      transform: translateY(-50%) scale(1.1);
    }

    .el-icon {
      font-size: 20px;
    }
  }

  &:hover .carousel-arrow {
    opacity: 1;
  }

  .arrow-prev {
    left: 20px;
  }

  .arrow-next {
    right: 20px;
  }

  .carousel-indicators {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
    z-index: 10;

    .indicator-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.5);
      border: none;
      cursor: pointer;
      transition: all 0.3s ease;
      padding: 0;

      &:hover {
        background: rgba(255, 255, 255, 0.8);
      }

      &.active {
        background: #fff;
        width: 30px;
        border-radius: 5px;
      }
    }
  }
}

@media (max-width: 768px) {
  .image-carousel {
    .carousel-arrow {
      width: 36px;
      height: 36px;

      .el-icon {
        font-size: 16px;
      }
    }

    .arrow-prev {
      left: 10px;
    }

    .arrow-next {
      right: 10px;
    }

    .carousel-indicators {
      bottom: 12px;
      gap: 8px;

      .indicator-dot {
        width: 8px;
        height: 8px;

        &.active {
          width: 24px;
        }
      }
    }
  }
}
</style>
