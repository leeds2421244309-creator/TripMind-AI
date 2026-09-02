<script setup lang="ts">

import { useRouter } from "vue-router";


interface Props {
  currentStep:number;
  completedSteps:number[];
}


const props = defineProps<Props>();

const router = useRouter();


const steps=[
  {
    name:"基础",
    path:"/create-trip"
  },
  {
    name:"预算",
    path:"/create-trip/budget"
  },
  {
    name:"偏好",
    path:"/create-trip/preference"
  },
  {
    name:"确认",
    path:"/create-trip/decision"
  }
];


function goPage(index:number){

  const step=steps[index];
  if(!step) return;
  router.push(step.path);

}


</script>


<template>

<div class="navigation">


<div
v-for="(step,index) in steps"
:key="step.name"
class="item"
@click="goPage(index)"
>


<div
class="dot"
:class="{

active:index+1===props.currentStep,

completed:
props.completedSteps.includes(index+1)

}"
>
</div>


<span>
{{step.name}}
</span>


</div>


</div>


</template>



<style scoped>


.navigation{

display:flex;
justify-content:center;
align-items:flex-start;
gap:35px;
margin-bottom:30px;

}


.item{

display:flex;
flex-direction:column;
align-items:center;
cursor:pointer;
font-size:14px;
color:#64748b;

}


.dot{

width:14px;
height:14px;

border-radius:50%;

background:#e5e7eb;

margin-bottom:8px;

transition:.3s;

}


/* 当前 */

.dot.active{

background:#2563eb;

transform:scale(1.2);

}


/* 已完成 */

.dot.completed{

background:#22c55e;

}



</style>