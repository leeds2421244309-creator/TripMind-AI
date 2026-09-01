<script setup lang="ts">


import {ref} from "vue";

import {useRouter} from "vue-router";


import TripNavigation from "@/components/create-trip/TripNavigation.vue";

import TripPlanningMode from "@/components/create-trip/TripPlanningMode.vue";



const router=useRouter();



// const planningMode=ref(50);
import {computed} from "vue";

import AIPlanningIndicator 
from "@/components/create-trip/AIPlanningIndicator.vue";


const activeField=ref("");



const errors=ref<any>({});



const travel=ref({

title:"",

origin:"",

destination:"",

goal:"",

start_date:"",

end_date:"",

people:1

});


const planningScore = computed(()=>{


let score = 50;


// 已填写增加

if(travel.value.title)
score += 3;


if(travel.value.origin)
score += 8;


if(travel.value.destination)
score += 10;


if(travel.value.goal)
score += 8;


if(travel.value.start_date)
score += 8;


if(travel.value.end_date)
score += 5;



// 未填写可选项扣除

if(!travel.value.title)
score -= 3;


if(!travel.value.goal)
score -= 8;


if(!travel.value.start_date)
score -= 8;


if(!travel.value.end_date)
score -= 5;



// 限制范围

return Math.max(
0,
Math.min(
100,
score
)
);


})
const goals=[

"🚶 特种兵旅行",

"🌿 深度体验",

"😎 休闲度假",

"📸 摄影打卡",

"🍜 美食探索",

"💰 省钱旅行",

"✨ 高品质旅行",

"🎒 独自旅行"

];





function chooseGoal(goal:string){

travel.value.goal=
goal.replace(/[^\u4e00-\u9fa5]/g,"");


}




function validate(){


errors.value={};



if(!travel.value.origin){

errors.value.origin=
"请输入出发地";

}



if(!travel.value.destination){

errors.value.destination=
"请输入目的地";

}



return Object.keys(errors.value).length===0;


}





function next(){


if(validate()){


router.push("/create-trip/budget");


}


}





</script>



<template>


<div class="page">



<TripNavigation

:currentStep="1"

:completedSteps="[]"

/>



<!-- <TripPlanningMode

v-model="planningMode"

/> -->
<AIPlanningIndicator
:score="planningScore"
/>



<h1>
创建你的旅行
</h1>


<p class="sub">
填写越详细，AI生成计划越贴合。
</p>



<div class="card">


<!-- 名称 -->


<div class="field">


<label>

旅行名称

</label>


<input

v-model="travel.title"

placeholder="可不填写，AI可以生成"

/>


</div>





<!-- 出发地 -->


<div class="field">


<label>

出发地 *

<span v-if="activeField==='origin'">
可填写城市或具体地点
</span>


</label>


<input

v-model="travel.origin"

:class="{
errorInput:errors.origin
}"

@focus="activeField='origin'"

placeholder="例如：深圳"

/>


<p
class="error"
v-if="errors.origin"
>
⚠ {{errors.origin}}
</p>


</div>





<!-- 目的地 -->


<div class="field">


<label>

目的地 *

<span v-if="activeField==='destination'">
支持城市、国家、景区
</span>

</label>



<input

v-model="travel.destination"

:class="{
errorInput:errors.destination
}"

@focus="activeField='destination'"

placeholder="例如：香港"

/>



<p
class="error"
v-if="errors.destination"
>
⚠ {{errors.destination}}
</p>



</div>






<!-- 目标 -->


<div class="field">


<label>
旅行目标
</label>



<input

v-model="travel.goal"

placeholder="例如：演唱会、美食、摄影"

/>


<div class="goals">


<button

v-for="goal in goals"

:key="goal"

@click="chooseGoal(goal)"

>

{{goal}}

</button>


</div>


</div>







<!-- 日期 -->


<div class="field">


<label>
旅行日期
</label>



<div class="date">


<input
type="date"
v-model="travel.start_date"
/>


<span>
至
</span>


<input
type="date"
v-model="travel.end_date"
/>


</div>



</div>







<!-- 人数 -->


<div class="field">


<label>
同行人数 *
</label>



<div class="people">


<button
@click="travel.people=Math.max(1,travel.people-1)"
>
-
</button>


<span>
{{travel.people}}
</span>


<button
@click="travel.people++"
>
+
</button>


</div>



</div>



</div>





<button

class="next"

@click="next"

>

下一步：预算设置 →

</button>




</div>


</template>




<style scoped>


.page{

max-width:720px;

margin:auto;

padding:30px 20px;

}



h1{

font-size:32px;

}



.sub{

color:#64748b;

}



.card{

background:white;

padding:25px;

border-radius:20px;

box-shadow:0 8px 25px rgba(0,0,0,.06);

}



.field{

display:flex;

flex-direction:column;

gap:8px;

margin-bottom:20px;

}



label{

font-weight:600;

}



label span{

font-size:12px;

color:#2563eb;

margin-left:8px;

}



input{

padding:13px;

border-radius:12px;

border:1px solid #ddd;

}



.error{

color:red;

font-size:14px;

}



.date{

display:flex;

align-items:center;

gap:10px;

}



.goals{

display:flex;

gap:10px;

margin-top:10px;

flex-wrap:wrap;

}



.goals button{

border:1px solid #ddd;

background:white;

padding:8px 12px;

border-radius:20px;

cursor:pointer;

}



.people{

display:flex;

gap:20px;

align-items:center;

}



.people button{

width:35px;

height:35px;

border-radius:50%;

}



.next{

margin-top:25px;

width:100%;

padding:15px;

border:none;

border-radius:15px;

background:#2563eb;

color:white;

font-size:16px;

}

.errorInput{

border:2px solid #ef4444;

background:#fff7f7;

}

</style>