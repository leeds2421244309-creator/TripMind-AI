<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

const nextStep = () => {
  router.push("/create-trip/decision");
};

const previousStep = () => {
  router.back();
};
</script>

<template>
  <div class="page">
    <p class="step">Step 3 / 5</p>

    <h1>吃住行偏好</h1>

    <p>填写住宿、美食、交通偏好。</p>

    <div class="buttons">
      <button @click="previousStep">上一步</button>
      <button @click="nextStep">下一步</button>
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