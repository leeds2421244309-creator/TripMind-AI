<script setup lang="ts">

defineProps<{
  score:number
}>()


</script>


<template>

<div class="container">

  <div class="title">
    AI规划程度
  </div>


  <div class="labels">

    <span>
      🤖 AI发挥空间
    </span>


    <span>
      个性化定制 🎯
    </span>

  </div>



  <div class="bar">


    <div
      class="progress"
      :style="{width:score+'%'}"
    >


    </div>


    <div
      class="point"
      :style="{left:score+'%'}"
    >


    </div>


  </div>



  <div class="tip">

    信息越完整，AI生成计划越符合你的需求

  </div>



</div>


</template>



<style scoped>


.container{

background:#f8fafc;

padding:20px;

border-radius:16px;

margin-bottom:25px;

}



.title{

font-size:16px;

font-weight:700;

margin-bottom:15px;

}



.labels{

display:flex;

justify-content:space-between;

font-size:14px;

color:#475569;

}



.bar{

position:relative;

height:8px;

background:#e2e8f0;

border-radius:10px;

margin-top:18px;

}



.progress{

height:100%;

background:#3b82f6;

border-radius:10px;

}



.point{

position:absolute;

top:50%;

transform:translate(-50%,-50%);

width:18px;

height:18px;

background:white;

border:4px solid #2563eb;

border-radius:50%;

}



.tip{

margin-top:15px;

font-size:12px;

color:#64748b;

text-align:center;

}



</style>