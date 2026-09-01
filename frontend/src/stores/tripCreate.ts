import { defineStore } from "pinia";


export const useTripCreateStore = defineStore(
"tripCreate",
{

state:()=>({

title:"",

origin:"",

destination:"",

goal:"",

start_date:"",

end_date:"",

people_count:1,


budget:0,


planning_mode:50,


}),

actions:{


setPeople(count:number){

this.people_count=count;

}


}


}

)