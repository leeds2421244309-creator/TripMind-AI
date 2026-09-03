import { defineStore } from "pinia";


export const useTripCreateStore = defineStore(
"tripCreate",
{

state:()=>({

// ==============================
// Step 1：基本信息（CreateTravelPage）
// ==============================
title:"",

origin:"",

destination:"",

goal:"",

start_date:"",

end_date:"",

people_count:1,


// ==============================
// Step 2：预算（BudgetPage）
// ==============================
budget:0,


// ==============================
// Step 3：偏好（PreferencePage）
// ==============================
food_prefs:[] as string[],

food_restrictions:[] as string[],

accommodation_mode:"preference" as "preference"|"booked",

accommodation_prefs:[] as string[],

transport_mode:"preference" as "preference"|"booked",

transport_prefs:[] as string[],

bookings:[] as Array<{
name:string;
type:string;
time:string;
location:string;
amount:number;
}>,

special_prefs:[] as string[],


// ==============================
// Step 4：决策上下文（DecisionCenterPage）
// ==============================
planning_mode:50,

travel_role:"",

luggage_type:"",

shoe_type:"",

energy_level:2,

walk_distance:10,

today_goals:[] as string[],

activity_start_time:"09:00",

activity_end_time:"21:00",

wishlist:[] as Array<{
name:string;
category:string;
isMustVisit:boolean;
}>,

weather_prefs:[] as string[],

health_prefs:[] as string[],

need_nap:false,

equipment:[] as string[],

group_prefs:[] as string[],

special_needs:[] as string[],

}),


  getters: {
    tripDays: (state): number => {
      if (!state.start_date || !state.end_date) return 1;
      const s = new Date(state.start_date);
      const e = new Date(state.end_date);
      return Math.max(
        1,
        Math.ceil((e.getTime() - s.getTime()) / 86400000) + 1
      );
    },
    peopleDivisor(): number {
      return this.tripDays * Math.max(1, this.people_count);
    },
    perPersonBudget(): number {
      if (this.peopleDivisor === 0 || this.budget === 0) return 0;
      return Math.round(this.budget / this.peopleDivisor);
    },
  },

  
actions:{

setPeople(count:number){
this.people_count=count;
},

patchForm(payload: Record<string, any>){
Object.assign(this, payload);
}

}


}

)
