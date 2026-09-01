import { createRouter, createWebHistory } from "vue-router";

import CreateTravelPage from "../views/create-trip/CreateTravelPage.vue";
import BudgetPage from "../views/create-trip/BudgetPage.vue";
import PreferencePage from "../views/create-trip/PreferencePage.vue";
import DecisionCenterPage from "../views/create-trip/DecisionCenterPage.vue";
import GeneratePlanPage from "../views/create-trip/GeneratePlanPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/create-trip",
    },
    {
      path: "/create-trip",
      name: "CreateTravel",
      component: CreateTravelPage,
    },
    {
      path: "/create-trip/budget",
      name: "Budget",
      component: BudgetPage,
    },
    {
      path: "/create-trip/preference",
      name: "Preference",
      component: PreferencePage,
    },
    {
      path: "/create-trip/decision",
      name: "DecisionCenter",
      component: DecisionCenterPage,
    },
    {
      path: "/create-trip/generate",
      name: "GeneratePlan",
      component: GeneratePlanPage,
    },
  ],
});

export default router;