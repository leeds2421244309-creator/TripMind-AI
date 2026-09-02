import { reactive } from "vue";

// 创建旅行全流程共享状态（模块级单例）
const tripData = reactive({
  title: "",
  origin: "",
  destination: "",
  goal: "",
  start_date: "",
  end_date: "",
  people: 1,
  totalBudget: 0,
});

export function useTripData() {
  return tripData;
}
