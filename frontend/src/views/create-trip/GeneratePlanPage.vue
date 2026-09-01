<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

const previousStep = () => {
  router.back();
};
</script>

<template>
  <div class="page">
    <p class="step">Step 5 / 5</p>

    <h1>AI 生成旅行计划</h1>

    <p>这里将在 Day20 接入 AI Planner。</p>

    <div class="buttons">
      <button @click="previousStep">返回修改</button>
      <button disabled>生成旅行计划（Day20）</button>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 24px;
}
.step {
  color: #2563eb;
  font-weight: bold;
}
.buttons {
  display: flex;
  gap: 12px;
}
</style>