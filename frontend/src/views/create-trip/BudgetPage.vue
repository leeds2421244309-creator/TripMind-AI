<script setup lang="ts">

import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import TripNavigation from "@/components/create-trip/TripNavigation.vue";
import { useTripCreateStore } from "@/stores/tripCreate";
import { checkBudgetRisks } from "@/data/budgetRiskRules";

const router = useRouter();
const tripStore = useTripCreateStore();

// 从 store 读人数、天数、目的地
const people = computed(() => tripStore.people_count || 1);
const tripDays = computed(() => {
  if (!tripStore.start_date || !tripStore.end_date) return 1;
  const s = new Date(tripStore.start_date);
  const e = new Date(tripStore.end_date);
  return Math.max(1, Math.ceil((e.getTime() - s.getTime()) / 86400000) + 1);
});
const destination = computed(() => tripStore.destination || "");

// 总预算（普通 ref + watch 同步到 store）
const totalBudget = ref(tripStore.budget || 0);

watch(totalBudget, (val) => {
  tripStore.budget = val;
});

// 状态选项
const statusOptions = ["待分配", "已规划", "已支付", "待定中"];

// 预算分类（showPerPerson 控制人均列是否显示）
const budgetItems = ref([
  { name: "餐饮", amount: 0, status: "待分配", showPerPerson: true },
  { name: "住宿", amount: 0, status: "待分配", showPerPerson: true },
  { name: "大交通", amount: 0, status: "待分配", showPerPerson: false },
  { name: "市内交通", amount: 0, status: "待分配", showPerPerson: true },
  { name: "门票娱乐", amount: 0, status: "待分配", showPerPerson: false },
  { name: "事前准备", amount: 0, status: "待分配", showPerPerson: false },
  { name: "其他备用", amount: 0, status: "待分配", showPerPerson: true },
]);

const customItems = ref<any[]>([]);

function addCustom() {
  customItems.value.push({
    name: "新预算项",
    amount: 0,
    status: "待分配",
    showPerPerson: true,
  });
}

function deleteCustom(index: number) {
  customItems.value.splice(index, 1);
}

// ==============================
// 计算逻辑
// ==============================

// 人数 × 天数
const divisor = computed(() => people.value * tripDays.value);

// 人均每天预算
const perPersonBudget = computed(() => {
  if (divisor.value === 0) return 0;
  return Math.round(totalBudget.value / divisor.value);
});

// 已规划金额（含已支付，已支付是已规划的子集）
const plannedAmount = computed(() =>
  [...budgetItems.value, ...customItems.value]
    .filter((item) => item.status === "已规划" || item.status === "已支付")
    .reduce((sum, item) => sum + item.amount, 0)
);

// 已支付（已规划的子集，仅用于展示）
const paidAmount = computed(() =>
  [...budgetItems.value, ...customItems.value]
    .filter((item) => item.status === "已支付")
    .reduce((sum, item) => sum + item.amount, 0)
);

// 待定中
const determinedAmount = computed(() =>
  [...budgetItems.value, ...customItems.value]
    .filter((item) => item.status === "待定中")
    .reduce((sum, item) => sum + item.amount, 0)
);

// 待分配金额 = 总预算 - 已规划（含已支付）
const unallocatedAmount = computed(() =>
  Math.max(totalBudget.value - plannedAmount.value, 0)
);

// 百分比
function calcPercent(amount: number): number {
  if (totalBudget.value === 0) return 0;
  return Math.round((amount / totalBudget.value) * 100);
}

// 人均
function calcPerPerson(amount: number): number {
  if (divisor.value === 0) return 0;
  return Math.round(amount / divisor.value);
}

// 三列互转
function onPerPersonChange(item: any, e: Event) {
  const val = Number((e.target as HTMLInputElement).value) || 0;
  item.amount = Math.round(val * divisor.value);
  onAmountChange(item);
}

function onPercentChange(item: any, e: Event) {
  const val = Number((e.target as HTMLInputElement).value) || 0;
  item.amount = Math.round((val / 100) * totalBudget.value);
  onAmountChange(item);
}

// amount 填了 → 自动设为"已规划"
function onAmountChange(item: any) {
  if (item.amount > 0 && item.status === "待分配") {
    item.status = "已规划";
  }
}

// ==============================
// 风险提醒（基于规则配置，可叠加，可关闭，自动消失）
// ==============================

// 用户手动关闭的风险标题
const dismissedRisks = ref<Set<string>>(new Set());

const allRisks = computed(() => {
  if (totalBudget.value <= 0) return [];
  const result = checkBudgetRisks({
    destination: destination.value,
    totalBudget: totalBudget.value,
    peopleCount: people.value,
    tripDays: tripDays.value,
    perPersonDaily: perPersonBudget.value,
    items: [...budgetItems.value, ...customItems.value].map((i) => ({
      name: i.name,
      amount: i.amount,
    })),
  });

  // 超预算检查（规则库未覆盖的通用检查）
  if (plannedAmount.value > totalBudget.value && totalBudget.value > 0) {
    result.unshift({
      level: "danger",
      title: "预算超支",
      text: `已规划 ¥${plannedAmount.value}，超出总预算 ¥${plannedAmount.value - totalBudget.value}`,
    });
  }

  return result;
});

// 过滤掉已关闭的风险
const risks = computed(() =>
  allRisks.value.filter((r) => !dismissedRisks.value.has(r.title))
);

// 关闭风险提醒
function dismissRisk(title: string) {
  dismissedRisks.value.add(title);
}

// 预算变化时重置已关闭的提醒（让它们重新出现）
function resetDismissed() {
  dismissedRisks.value.clear();
}

// 总预算变化时重置
watch(totalBudget, () => resetDismissed());

// ==============================
// 跳转
// ==============================

function next() {
  router.push("/create-trip/preference");
}

</script>

<template>
  <div class="page">
    <TripNavigation :currentStep="2" :completedSteps="[1]" />

    <h1>预算设置</h1>
    <p class="desc">合理规划预算，AI会根据预算生成旅行方案</p>

    <!-- 总预算 -->
    <section class="card">
      <h2>总预算</h2>
      <div class="budget-input">
        ¥<input v-model.number="totalBudget" type="number" />
      </div>
      <div class="info">
        人均预算：¥{{ perPersonBudget }}（{{ people }}人 × {{ tripDays }}天）<br />
        目的地：{{ destination || "未填写" }}
      </div>
    </section>

    <!-- 状态条 -->
    <section class="card">
      <h2>预算状态</h2>
      <div class="bar">
        <div
          class="planned"
          :style="{
            width: Math.min((plannedAmount / (totalBudget || 1)) * 100, 100) + '%',
          }"
        />
      </div>
      <div class="status">
        <span>已规划 {{ calcPercent(plannedAmount) }}%</span>
        <span>已支付 {{ calcPercent(paidAmount) }}%</span>
        <span>待分配 {{ calcPercent(unallocatedAmount) }}%</span>
        <span>待定中 {{ calcPercent(determinedAmount) }}%</span>
      </div>
    </section>

    <!-- 风险提醒 -->
    <section class="card" v-if="risks.length">
      <h2>预算风险提醒</h2>
      <div
        v-for="(risk, i) in risks"
        :key="risk.title + i"
        class="risk"
        :class="risk.level"
      >
        <span class="risk-content">
          <span v-if="risk.level === 'danger'">🔴</span>
          <span v-else-if="risk.level === 'warning'">🟠</span>
          <span v-else-if="risk.level === 'safe'">🟢</span>
          <span v-else>ℹ️</span>
          <strong>{{ risk.title }}</strong> — {{ risk.text }}
        </span>
        <button class="risk-close" @click="dismissRisk(risk.title)">×</button>
      </div>
    </section>

    <!-- 分类预算 -->
    <section class="card">
      <div class="title-row">
        <h2>预算分配</h2>
        <button @click="addCustom">+ 添加自定义</button>
      </div>

      <table class="budget-table">
        <thead>
          <tr>
            <th style="width:14%">类别</th>
            <th style="width:15%">金额(¥)</th>
            <th style="width:15%">人均(元/人/天)</th>
            <th style="width:12%">比例(%)</th>
            <th style="width:16%">状态</th>
            <th style="width:10%">操作</th>
          </tr>
        </thead>

        <tbody>
          <!-- 固定分类 -->
          <tr v-for="item in budgetItems" :key="item.name">
            <td>{{ item.name }}</td>
            <td>
              <input
                v-model.number="item.amount"
                type="number"
                @change="onAmountChange(item)"
              />
            </td>
            <td>
              <input
                v-if="item.showPerPerson"
                type="number"
                :value="calcPerPerson(item.amount)"
                @change="onPerPersonChange(item, $event)"
              />
              <span v-else>—</span>
            </td>
            <td>
              <input
                type="number"
                :value="calcPercent(item.amount)"
                @change="onPercentChange(item, $event)"
              />
            </td>
            <td>
              <select v-model="item.status">
                <option v-for="s in statusOptions" :key="s" :value="s">
                  {{ s }}
                </option>
              </select>
            </td>
            <td>
              <button
                class="toggle-btn"
                @click="item.showPerPerson = !item.showPerPerson"
                :title="item.showPerPerson ? '关闭人均' : '开启人均'"
              >
                {{ item.showPerPerson ? "👤" : "🚫" }}
              </button>
            </td>
          </tr>

          <!-- 自定义项 -->
          <tr
            v-for="(item, index) in customItems"
            :key="index"
            class="custom-row"
          >
            <td><input v-model="item.name" /></td>
            <td>
              <input
                v-model.number="item.amount"
                type="number"
                @change="onAmountChange(item)"
              />
            </td>
            <td>
              <input
                v-if="item.showPerPerson"
                type="number"
                :value="calcPerPerson(item.amount)"
                @change="onPerPersonChange(item, $event)"
              />
              <span v-else>—</span>
            </td>
            <td>
              <input
                type="number"
                :value="calcPercent(item.amount)"
                @change="onPercentChange(item, $event)"
              />
            </td>
            <td>
              <select v-model="item.status">
                <option v-for="s in statusOptions" :key="s" :value="s">
                  {{ s }}
                </option>
              </select>
            </td>
            <td>
              <div class="row-actions">
                <button
                  class="toggle-btn"
                  @click="item.showPerPerson = !item.showPerPerson"
                >
                  {{ item.showPerPerson ? "👤" : "🚫" }}
                </button>
                <button class="del-btn" @click="deleteCustom(index)">×</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <button class="next" @click="next">下一步：旅行偏好 →</button>
  </div>
</template>

<style scoped>
.page {
  max-width: 900px;
  margin: auto;
  padding: 30px;
}

h1 {
  font-size: 32px;
}

.desc {
  color: #666;
}

.card {
  background: white;
  border-radius: 20px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 5px 20px #00000010;
}

.budget-input {
  font-size: 30px;
}

.budget-input input {
  width: 150px;
  font-size: 30px;
  border: none;
}

.info {
  margin-top: 10px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.8;
}

.bar {
  height: 16px;
  overflow: hidden;
  background: #eee;
  border-radius: 20px;
}

.planned {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}

.status {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  font-size: 14px;
}

.risk {
  margin-top: 10px;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.risk-content {
  flex: 1;
}

.risk.danger {
  color: #dc2626;
  background: #fef2f2;
}

.risk.warning {
  color: #c2410c;
  background: #fff7ed;
}

.risk.safe {
  color: #16a34a;
  background: #f0fdf4;
}

.risk.info {
  color: #2563eb;
  background: #eff6ff;
}

.risk-close {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  padding: 0;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: inherit;
  opacity: 0.5;
}

.risk-close:hover {
  opacity: 1;
  background: rgba(0, 0, 0, 0.08);
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  padding: 10px 15px;
  cursor: pointer;
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
}

table.budget-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
  table-layout: fixed;
}

th,
td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  color: #64748b;
  font-size: 13px;
}

td input,
td select {
  width: 100%;
  padding: 6px 8px;
  font-size: 14px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.row-actions {
  display: flex;
  gap: 6px;
  align-items: center;
}

.toggle-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 28px;
  height: 28px;
  padding: 0;
  cursor: pointer;
  background: #f3f4f6;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.del-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 28px;
  height: 28px;
  padding: 0;
  color: white;
  font-size: 16px;
  cursor: pointer;
  background: #ef4444;
  border: none;
  border-radius: 50%;
}

.custom-row {
  background: #f9fafb;
}

.next {
  width: 100%;
  margin-top: 30px;
  padding: 15px;
  color: white;
  font-size: 18px;
  cursor: pointer;
  background: #2563eb;
  border: none;
  border-radius: 15px;
}
</style>
