<script setup lang="ts">


const props = defineProps<{

modelValue:number

}>();


const emit = defineEmits<{

(e:"update:modelValue",value:number):void

}>();



function change(e:Event){

const value =
Number((e.target as HTMLInputElement).value);


emit(
"update:modelValue",
value
);


}


</script>



<template>


<div class="planning">


<div class="title">

AI规划程度

</div>



<div class="labels">

<span>
🤖 AI自由规划
</span>


<span>
精准定制旅行 🎯
</span>

</div>



<input

type="range"

min="0"

max="100"

:value="props.modelValue"

@input="change"

/>



<div class="desc">


<span>
填写少：
AI决定更多，速度更快
</span>


<span>
填写多：
计划更符合个人需求
</span>


</div>


</div>


</template>




<style scoped>


.planning{

background:#f8fafc;

padding:20px;

border-radius:16px;

margin-bottom:25px;

}



.title{

font-weight:700;

margin-bottom:15px;

}



.labels{

display:flex;

justify-content:space-between;

font-size:14px;

}



input{

width:100%;

margin-top:15px;

}



.desc{

display:flex;

justify-content:space-between;

font-size:12px;

color:#64748b;

margin-top:10px;

}



</style>