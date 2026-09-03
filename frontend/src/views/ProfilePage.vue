<script setup lang="ts">
import { ref, computed } from "vue";

// ==============================
// 模块一：个人旅行档案（Mock）
// ==============================
interface UserProfile {
  avatar: string;
  nickname: string;
  travelCount: number;
  joinDate: string;
}

const profile = ref<UserProfile>({
  avatar: "🧳",
  nickname: "旅行家小张",
  travelCount: 12,
  joinDate: "2026-01",
});

const profileStats = computed(() => [
  { label: "旅行次数", value: profile.value.travelCount },
  { label: "国家/地区", value: 5 },
  { label: "累计天数", value: 38 },
]);

// ==============================
// 模块二：长期饮食偏好（多选）
// ==============================
const dietOptions = [
  { key: "no_spicy", label: "不吃辣", icon: "🌶️" },
  { key: "vegetarian", label: "素食", icon: "🥗" },
  { key: "halal", label: "清真", icon: "🍖" },
  { key: "no_seafood", label: "不吃海鲜", icon: "🦐" },
  { key: "no_coriander", label: "不吃香菜", icon: "🌿" },
  { key: "lactose_free", label: "乳糖不耐", icon: "🥛" },
  { key: "low_sugar", label: "低糖", icon: "🍰" },
  { key: "no_raw", label: "不吃生食", icon: "🍣" },
];
const selectedDiets = ref<string[]>(["no_spicy", "no_coriander"]);

function toggleDiet(key: string) {
  const idx = selectedDiets.value.indexOf(key);
  if (idx > -1) selectedDiets.value.splice(idx, 1);
  else selectedDiets.value.push(key);
}

// ==============================
// 模块三：默认预算
// ==============================
const defaultBudget = ref(5000);
const budgetPresets = [
  { label: "穷游", value: 1500 },
  { label: "经济", value: 3000 },
  { label: "舒适", value: 5000 },
  { label: "轻奢", value: 10000 },
  { label: "豪华", value: 20000 },
];

function setBudgetPreset(value: number) {
  defaultBudget.value = value;
}

// ==============================
// 模块四：默认住宿偏好（多选）
// ==============================
const accommodationOptions = [
  { key: "hotel", label: "酒店", icon: "🏨" },
  { key: "bnb", label: "民宿", icon: "🏠" },
  { key: "hostel", label: "青旅", icon: "🛏️" },
  { key: "resort", label: "度假村", icon: "🏖️" },
  { key: "apartment", label: "公寓", icon: "🏢" },
  { key: "capsule", label: "胶囊", icon: "💊" },
];
const selectedAccommodations = ref<string[]>(["hotel", "bnb"]);

function toggleAccommodation(key: string) {
  const idx = selectedAccommodations.value.indexOf(key);
  if (idx > -1) selectedAccommodations.value.splice(idx, 1);
  else selectedAccommodations.value.push(key);
}

// ==============================
// 模块五：默认出发地
// ==============================
const defaultOrigin = ref("深圳");
const commonOrigins = ["深圳", "广州", "北京", "上海", "成都", "杭州", "西安"];

function selectOrigin(city: string) {
  defaultOrigin.value = city;
}

// ==============================
// 模块六：常用语言
// ==============================
const languageOptions = [
  { key: "zh", label: "中文", icon: "🇨🇳" },
  { key: "en", label: "English", icon: "🇬🇧" },
  { key: "ja", label: "日本語", icon: "🇯🇵" },
  { key: "ko", label: "한국어", icon: "🇰🇷" },
  { key: "fr", label: "Français", icon: "🇫🇷" },
  { key: "es", label: "Español", icon: "🇪🇸" },
];
const selectedLanguages = ref<string[]>(["zh", "en"]);

function toggleLanguage(key: string) {
  const idx = selectedLanguages.value.indexOf(key);
  if (idx > -1) selectedLanguages.value.splice(idx, 1);
  else selectedLanguages.value.push(key);
}

// ==============================
// 模块七：通知设置
// ==============================
const notifications = ref({
  travel_reminder: true,
  weather_alert: true,
  budget_warning: true,
  todo_checklist: false,
  new_feature: false,
  ai_suggestion: true,
});

const notificationLabels: Record<string, { label: string; desc: string }> = {
  travel_reminder: { label: "旅行提醒", desc: "出发前、行程中关键节点提醒" },
  weather_alert: { label: "天气预警", desc: "目的地恶劣天气提前告知" },
  budget_warning: { label: "预算预警", desc: "支出接近预算阈值时提醒" },
  todo_checklist: { label: "待办清单", desc: "每日待办事项推送" },
  new_feature: { label: "新功能", desc: "产品更新通知" },
  ai_suggestion: { label: "AI 建议", desc: "行程优化建议推送" },
};

function toggleNotification(key: keyof typeof notifications.value) {
  notifications.value[key] = !notifications.value[key];
}

// ==============================
// 保存（Mock）
// ==============================
function save() {
  // TODO: Day20+ 对接 Users API
  // 长期偏好写入数据库，跨旅行复用
  console.log("保存个人偏好", {
    diets: selectedDiets.value,
    defaultBudget: defaultBudget.value,
    accommodations: selectedAccommodations.value,
    defaultOrigin: defaultOrigin.value,
    languages: selectedLanguages.value,
    notifications: notifications.value,
  });
  alert("已保存（Mock）");
}
</script>

<template>
  <div class="page">
    <h1>个人中心</h1>
    <p class="sub">长期旅行偏好，跨旅行复用，非本次行程设置。</p>

    <!-- 模块一：个人旅行档案 -->
    <div class="card profile-card">
      <div class="avatar">{{ profile.avatar }}</div>
      <div class="profile-info">
        <div class="nickname">{{ profile.nickname }}</div>
        <div class="join-date">加入时间：{{ profile.joinDate }}</div>
      </div>
      <div class="profile-stats">
        <div v-for="stat in profileStats" :key="stat.label" class="stat">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- 模块二：长期饮食偏好 -->
    <div class="card">
      <div class="title-row">
        <h2>长期饮食偏好</h2>
        <span class="badge">多选</span>
      </div>
      <p class="hint">AI 会自动避开你忌口的食物</p>
      <div class="chips">
        <button
          v-for="opt in dietOptions"
          :key="opt.key"
          class="chip"
          :class="{ chipActive: selectedDiets.includes(opt.key) }"
          @click="toggleDiet(opt.key)"
        >
          {{ opt.icon }} {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- 模块三：默认预算 -->
    <div class="card">
      <h2>默认预算</h2>
      <p class="hint">新建旅行时的默认预算参考</p>
      <div class="budget-input-row">
        <span>¥</span>
        <input type="number" v-model.number="defaultBudget" class="budget-input" min="0" />
        <span>/ 次</span>
      </div>
      <div class="budget-presets">
        <button
          v-for="preset in budgetPresets"
          :key="preset.label"
          class="preset-chip"
          :class="{ presetActive: defaultBudget === preset.value }"
          @click="setBudgetPreset(preset.value)"
        >
          {{ preset.label }} ¥{{ preset.value.toLocaleString() }}
        </button>
      </div>
    </div>

    <!-- 模块四：默认住宿偏好 -->
    <div class="card">
      <div class="title-row">
        <h2>默认住宿偏好</h2>
        <span class="badge">多选</span>
      </div>
      <p class="hint">AI 推荐住宿时优先这些类型</p>
      <div class="chips">
        <button
          v-for="opt in accommodationOptions"
          :key="opt.key"
          class="chip"
          :class="{ chipActive: selectedAccommodations.includes(opt.key) }"
          @click="toggleAccommodation(opt.key)"
        >
          {{ opt.icon }} {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- 模块五：默认出发地 -->
    <div class="card">
      <h2>默认出发地</h2>
      <p class="hint">新建旅行自动填入</p>
      <div class="chips">
        <button
          v-for="city in commonOrigins"
          :key="city"
          class="chip"
          :class="{ chipActive: defaultOrigin === city }"
          @click="selectOrigin(city)"
        >
          📍 {{ city }}
        </button>
      </div>
      <div class="origin-custom">
        <label class="block-label">或自定义</label>
        <input v-model="defaultOrigin" placeholder="输入城市名" class="text-input" />
      </div>
    </div>

    <!-- 模块六：常用语言 -->
    <div class="card">
      <div class="title-row">
        <h2>常用语言</h2>
        <span class="badge">多选</span>
      </div>
      <p class="hint">翻译工具与 AI 对话优先使用</p>
      <div class="chips">
        <button
          v-for="opt in languageOptions"
          :key="opt.key"
          class="chip"
          :class="{ chipActive: selectedLanguages.includes(opt.key) }"
          @click="toggleLanguage(opt.key)"
        >
          {{ opt.icon }} {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- 模块七：通知设置 -->
    <div class="card">
      <h2>通知设置</h2>
      <div class="notify-list">
        <div
          v-for="(value, key) in notifications"
          :key="key"
          class="notify-item"
          @click="toggleNotification(key as keyof typeof notifications)"
        >
          <div class="notify-text">
            <div class="notify-label">{{ notificationLabels[key].label }}</div>
            <div class="notify-desc">{{ notificationLabels[key].desc }}</div>
          </div>
          <div class="switch" :class="{ switchOn: value }">
            <div class="switch-knob"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 保存按钮 -->
    <button class="save-btn" @click="save">保存偏好</button>
  </div>
</template>

<style scoped>
.page {
  max-width: 720px;
  margin: auto;
  padding: 30px 20px;
}

h1 {
  font-size: 32px;
}

.sub {
  color: #64748b;
  margin-bottom: 20px;
}

.card {
  background: white;
  padding: 25px;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
  margin-top: 20px;
}

h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
}

.hint {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 12px;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.badge {
  font-size: 12px;
  color: #2563eb;
  background: #eff6ff;
  padding: 4px 10px;
  border-radius: 10px;
}

/* 个人档案 */
.profile-card {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #eff6ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
}

.profile-info {
  flex: 1;
  min-width: 120px;
}

.nickname {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.join-date {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 4px;
}

.profile-stats {
  display: flex;
  gap: 20px;
  width: 100%;
  border-top: 1px solid #f1f5f9;
  padding-top: 16px;
  margin-top: 4px;
}

.stat {
  flex: 1;
  text-align: center;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #2563eb;
}

.stat-label {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

/* Chip 通用 */
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chip {
  border: 1px solid #ddd;
  background: white;
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.chip:hover {
  border-color: #93c5fd;
}

.chipActive {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

/* 预算 */
.budget-input-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.budget-input-row span {
  font-size: 16px;
  color: #64748b;
}

.budget-input {
  flex: 1;
  padding: 13px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 18px;
  font-weight: 600;
}

.budget-presets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preset-chip {
  border: 1px solid #ddd;
  background: white;
  padding: 6px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  color: #475569;
  transition: all 0.2s;
}

.preset-chip:hover {
  border-color: #2563eb;
}

.presetActive {
  background: #eff6ff;
  color: #2563eb;
  border-color: #2563eb;
  font-weight: 600;
}

/* 出发自定义 */
.origin-custom {
  margin-top: 14px;
}

.block-label {
  display: block;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
  color: #475569;
}

.text-input {
  width: 100%;
  padding: 13px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 14px;
  box-sizing: border-box;
}

/* 通知 */
.notify-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notify-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
}

.notify-item:last-child {
  border-bottom: none;
}

.notify-label {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.notify-desc {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

.switch {
  width: 44px;
  height: 24px;
  border-radius: 12px;
  background: #e5e7eb;
  position: relative;
  transition: all 0.2s;
  flex-shrink: 0;
}

.switchOn {
  background: #2563eb;
}

.switch-knob {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: white;
  transition: all 0.2s;
}

.switchOn .switch-knob {
  left: 22px;
}

/* 保存按钮 */
.save-btn {
  margin-top: 25px;
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 15px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn:hover {
  background: #1d4ed8;
}
</style>
