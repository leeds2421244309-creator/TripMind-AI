<script setup lang="ts">

defineProps<{
  currentStep:number
}>()

</script>


<template>

<div class="progress-container">

  <div class="step-text">
    Step {{currentStep}} / 4
  </div>


  <div class="bar">

    <div 
      class="active"
      :style="{width:`${currentStep/4*100}%`}"
    >
    </div>

  </div>

</div>


</template>


<style scoped>

.progress-container{
  margin-bottom:30px;
}


.step-text{
  font-weight:600;
  margin-bottom:10px;
}


.bar{

height:8px;
background:#e5e7eb;
border-radius:20px;
overflow:hidden;

}


.active{

height:100%;
background:#2563eb;
transition:.3s;

}


</style>