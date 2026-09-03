<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import TripNavigation from "@/components/create-trip/TripNavigation.vue";
import { useTripCreateStore } from "@/stores/tripCreate";

const router = useRouter();
const tripStore = useTripCreateStore();

// ==============================
// 从 Store 读取已有数据
// ==============================
const destination = computed(() => tripStore.destination || "");
const people = computed(() => tripStore.people_count || 1);

// ==============================
// 模块一：旅行主题（Chip 多选）
// ==============================
const travelThemes = [
  "🚶 特种兵旅行",
  "🏙️ City Walk",
  "🌿 深度体验",
  "🍜 美食探索",
  "📸 摄影旅行",
  "🛍️ 购物旅行",
  "🎤 演唱会旅行",
  "🏔️ 自然风景",
  "🏛️ 博物馆",
  "🌃 夜景",
  "☕ 咖啡店巡礼",
];
const selectedThemes = ref<string[]>([]);

function toggleTheme(theme: string) {
  const clean = theme.replace(/[^\u4e00-\u9fa5a-zA-Z\s]/g, "").trim();
  const idx = selectedThemes.value.indexOf(clean);
  if (idx > -1) {
    selectedThemes.value.splice(idx, 1);
  } else {
    selectedThemes.value.push(clean);
  }
}

function isThemeActive(theme: string) {
  const clean = theme.replace(/[^\u4e00-\u9fa5a-zA-Z\s]/g, "").trim();
  return selectedThemes.value.includes(clean);
}

// ==============================
// 模块二：美食偏好（Chip 多选 + 限制项）
// ==============================
const foodOptions = [
  "🍲 火锅",
  "🍢 烧烤",
  "🍣 日料",
  "🍲 韩餐",
  "☕ 咖啡",
  "🧋 奶茶",
  "🦐 海鲜",
  "🥟 小吃",
  "🍰 甜品",
  "🥗 素食",
];
const selectedFoods = ref<string[]>([]);

const foodRestrictions = ["不吃辣", "不吃香菜", "清真", "素食"];
const selectedRestrictions = ref<string[]>([]);

function toggleFood(food: string) {
  const clean = food.replace(/[^\u4e00-\u9fa5]/g, "");
  const idx = selectedFoods.value.indexOf(clean);
  if (idx > -1) {
    selectedFoods.value.splice(idx, 1);
  } else {
    selectedFoods.value.push(clean);
  }
}

function isFoodActive(food: string) {
  const clean = food.replace(/[^\u4e00-\u9fa5]/g, "");
  return selectedFoods.value.includes(clean);
}

function toggleRestriction(item: string) {
  const idx = selectedRestrictions.value.indexOf(item);
  if (idx > -1) {
    selectedRestrictions.value.splice(idx, 1);
  } else {
    selectedRestrictions.value.push(item);
  }
}

// ==============================
// 模块三：住宿偏好（二选一）
// ==============================
const accommodationMode = ref<"preference" | "booked">("preference");

const accommodationOptions = [
  "🏨 酒店",
  "🏠 民宿",
  "🎒 青旅",
  "📍 市中心",
  "🚇 地铁附近",
  "🗺️ 景点附近",
  "🤫 安静区域",
  "💰 高性价比",
];
const selectedAccommodation = ref<string[]>([]);

function toggleAccommodation(opt: string) {
  const clean = opt.replace(/[^\u4e00-\u9fa5]/g, "");
  const idx = selectedAccommodation.value.indexOf(clean);
  if (idx > -1) {
    selectedAccommodation.value.splice(idx, 1);
  } else {
    selectedAccommodation.value.push(clean);
  }
}

function isAccommodationActive(opt: string) {
  const clean = opt.replace(/[^\u4e00-\u9fa5]/g, "");
  return selectedAccommodation.value.includes(clean);
}

// TODO: 住宿 Booking 上传 OCR — Day20+ 接入 OCR API
function uploadAccommodationBooking() {
  // TODO: 调用 OCR API 识别 Booking 截图
}

// ==============================
// 模块四：交通偏好（二选一）
// ==============================
const transportMode = ref<"preference" | "booked">("preference");

const transportOptions = ["公交优先", "地铁优先", "少换乘", "可以打车", "步行优先"];
const selectedTransport = ref<string[]>([]);

function toggleTransport(opt: string) {
  const idx = selectedTransport.value.indexOf(opt);
  if (idx > -1) {
    selectedTransport.value.splice(idx, 1);
  } else {
    selectedTransport.value.push(opt);
  }
}

// TODO: 交通 Booking 上传 OCR — Day20+ 接入 OCR API
function uploadTransportBooking() {
  // TODO: 调用 OCR API 识别机票/火车票截图
}

// ==============================
// 模块五：已预订活动（Booking 卡片列表）
// ==============================
interface BookingItem {
  name: string;
  type: string;
  time: string;
  location: string;
  amount: number;
}

const bookingList = ref<BookingItem[]>([]);

const bookingTypeOptions = [
  "景点门票",
  "演唱会",
  "展览",
  "乐园",
  "酒店",
  "餐厅预约",
];

function addBooking() {
  bookingList.value.push({
    name: "",
    type: "景点门票",
    time: "",
    location: "",
    amount: 0,
  });
}

function removeBooking(index: number) {
  bookingList.value.splice(index, 1);
}

// TODO: Booking 截图上传 OCR — Day20+ 接入 OCR API
function uploadBookingScreenshot() {
  // TODO: 调用 OCR API 自动解析时间、地点、金额
}

// ==============================
// 模块六：特殊偏好（Chip + 输入）
// ==============================
const specialOptions = ["看日落", "看夜景", "买手办", "打卡机位", "购物退税", "学生优惠", "网红餐厅"];
const selectedSpecials = ref<string[]>([]);
const customSpecial = ref("");

function toggleSpecial(opt: string) {
  const idx = selectedSpecials.value.indexOf(opt);
  if (idx > -1) {
    selectedSpecials.value.splice(idx, 1);
  } else {
    selectedSpecials.value.push(opt);
  }
}

function addCustomSpecial() {
  if (customSpecial.value.trim()) {
    selectedSpecials.value.push(customSpecial.value.trim());
    customSpecial.value = "";
  }
}

function removeSpecial(opt: string) {
  const idx = selectedSpecials.value.indexOf(opt);
  if (idx > -1) {
    selectedSpecials.value.splice(idx, 1);
  }
}

// ==============================
// 跳转
// ==============================
function next() {
  // 将全部偏好数据写入 store（后续 AI Prompt Builder 使用）
  tripStore.patchForm({
    goal: selectedThemes.value.join("；"),
    food_prefs: [...selectedFoods.value],
    food_restrictions: [...selectedRestrictions.value],
    accommodation_mode: accommodationMode.value,
    accommodation_prefs: [...selectedAccommodation.value],
    transport_mode: transportMode.value,
    transport_prefs: [...selectedTransport.value],
    bookings: bookingList.value.map((b) => ({ ...b })),
    special_prefs: [...selectedSpecials.value],
  });
  router.push("/create-trip/decision");
}

function previous() {
  router.push("/create-trip/budget");
}
</script>

<template>
  <div class="page">
    <TripNavigation :currentStep="3" :completedSteps="[1, 2]" />

    <h1>吃住行偏好</h1>
    <p class="sub">告诉 AI 你这次旅行喜欢怎样安排，生成计划更贴合你的需求。</p>

    <!-- 模块一：旅行主题 -->
    <div class="card">
      <h2>旅行主题</h2>
      <p class="hint">支持多选，点击追加到输入框</p>
      <div class="chips">
        <button
          v-for="theme in travelThemes"
          :key="theme"
          class="chip"
          :class="{ chipActive: isThemeActive(theme) }"
          @click="toggleTheme(theme)"
        >
          {{ theme }}
        </button>
      </div>
    </div>

    <!-- 模块二：美食偏好 -->
    <div class="card">
      <h2>美食偏好</h2>
      <div class="chips">
        <button
          v-for="food in foodOptions"
          :key="food"
          class="chip"
          :class="{ chipActive: isFoodActive(food) }"
          @click="toggleFood(food)"
        >
          {{ food }}
        </button>
      </div>

      <label class="sub-label">饮食限制</label>
      <div class="chips">
        <button
          v-for="rest in foodRestrictions"
          :key="rest"
          class="chip"
          :class="{ chipActive: selectedRestrictions.includes(rest) }"
          @click="toggleRestriction(rest)"
        >
          {{ rest }}
        </button>
      </div>
    </div>

    <!-- 模块三：住宿偏好 -->
    <div class="card">
      <h2>住宿偏好</h2>
      <div class="toggle-group">
        <button
          class="toggle-btn"
          :class="{ toggleActive: accommodationMode === 'preference' }"
          @click="accommodationMode = 'preference'"
        >
          填写偏好
        </button>
        <button
          class="toggle-btn"
          :class="{ toggleActive: accommodationMode === 'booked' }"
          @click="accommodationMode = 'booked'"
        >
          已预订住宿
        </button>
      </div>

      <!-- 偏好模式 -->
      <div v-if="accommodationMode === 'preference'" class="chips">
        <button
          v-for="opt in accommodationOptions"
          :key="opt"
          class="chip"
          :class="{ chipActive: isAccommodationActive(opt) }"
          @click="toggleAccommodation(opt)"
        >
          {{ opt }}
        </button>
      </div>

      <!-- 已预订模式 -->
      <div v-else class="upload-area">
        <!-- TODO: OCR API — 上传住宿 Booking 截图自动识别 -->
        <button class="upload-btn" @click="uploadAccommodationBooking">
          📷 上传住宿订单截图
        </button>
        <p class="upload-hint">OCR 自动识别酒店名称、入住时间、地址</p>
      </div>
    </div>

    <!-- 模块四：交通偏好 -->
    <div class="card">
      <h2>交通偏好</h2>
      <div class="toggle-group">
        <button
          class="toggle-btn"
          :class="{ toggleActive: transportMode === 'preference' }"
          @click="transportMode = 'preference'"
        >
          填写偏好
        </button>
        <button
          class="toggle-btn"
          :class="{ toggleActive: transportMode === 'booked' }"
          @click="transportMode = 'booked'"
        >
          已预订交通
        </button>
      </div>

      <!-- 偏好模式 -->
      <div v-if="transportMode === 'preference'" class="chips">
        <button
          v-for="opt in transportOptions"
          :key="opt"
          class="chip"
          :class="{ chipActive: selectedTransport.includes(opt) }"
          @click="toggleTransport(opt)"
        >
          {{ opt }}
        </button>
      </div>

      <!-- 已预订模式 -->
      <div v-else class="upload-area">
        <!-- TODO: OCR API — 上传机票/火车票截图自动识别 -->
        <button class="upload-btn" @click="uploadTransportBooking">
          📷 上传交通票据截图
        </button>
        <p class="upload-hint">支持飞机票、火车票、高铁票、巴士票</p>
      </div>
    </div>

    <!-- 模块五：已预订活动 -->
    <div class="card">
      <div class="title-row">
        <h2>已预订活动</h2>
        <button class="add-btn" @click="addBooking">+ 添加</button>
      </div>

      <div v-if="bookingList.length === 0" class="empty-hint">
        暂无已预订活动，点击"添加"手动添加
      </div>

      <div v-for="(item, index) in bookingList" :key="index" class="booking-card">
        <div class="booking-header">
          <select v-model="item.type" class="booking-type">
            <option v-for="t in bookingTypeOptions" :key="t" :value="t">
              {{ t }}
            </option>
          </select>
          <button class="del-btn" @click="removeBooking(index)">×</button>
        </div>
        <div class="booking-fields">
          <input v-model="item.name" placeholder="活动名称" class="booking-input" />
          <input v-model="item.time" placeholder="时间 如：09-01 14:00" class="booking-input" />
          <input v-model="item.location" placeholder="地点" class="booking-input" />
          <input v-model.number="item.amount" type="number" placeholder="金额 ¥" class="booking-input" />
        </div>
        <!-- TODO: OCR API — 上传截图自动解析 Booking 信息 -->
        <button class="upload-small" @click="uploadBookingScreenshot">
          📷 截图识别
        </button>
      </div>
    </div>

    <!-- 模块六：特殊偏好 -->
    <div class="card">
      <h2>本次旅行特殊偏好</h2>
      <div class="chips">
        <button
          v-for="opt in specialOptions"
          :key="opt"
          class="chip"
          :class="{ chipActive: selectedSpecials.includes(opt) }"
          @click="toggleSpecial(opt)"
        >
          {{ opt }}
        </button>
      </div>

      <!-- 已选特殊偏好（可删除） -->
      <div v-if="selectedSpecials.length" class="chips" style="margin-top: 12px">
        <span
          v-for="opt in selectedSpecials.filter(o => !specialOptions.includes(o))"
          :key="opt"
          class="chip-tag"
          @click="removeSpecial(opt)"
        >
          {{ opt }} ×
        </span>
      </div>

      <!-- 自定义输入 -->
      <div class="custom-input-row">
        <input
          v-model="customSpecial"
          placeholder="输入自定义偏好，回车添加"
          class="custom-input"
          @keyup.enter="addCustomSpecial"
        />
        <button class="add-special-btn" @click="addCustomSpecial">添加</button>
      </div>
    </div>

    <!-- 导航按钮 -->
    <div class="nav-buttons">
      <button class="prev" @click="previous">← 上一步</button>
      <button class="next" @click="next">下一步：确认安排 →</button>
    </div>
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
  margin-bottom: 15px;
}

.hint {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 12px;
}

.sub-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-top: 20px;
  margin-bottom: 10px;
  color: #475569;
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

.chip-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: #eff6ff;
  color: #2563eb;
  border-radius: 16px;
  font-size: 13px;
  cursor: pointer;
}

/* 二选一切换 */
.toggle-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.toggle-btn {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.toggleActive {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

/* 上传区域 */
.upload-area {
  text-align: center;
  padding: 30px 20px;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
}

.upload-btn {
  padding: 12px 24px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
}

.upload-hint {
  margin-top: 10px;
  font-size: 13px;
  color: #94a3b8;
}

/* Booking 卡片 */
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-btn {
  padding: 8px 16px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
}

.empty-hint {
  text-align: center;
  padding: 20px;
  color: #94a3b8;
  font-size: 14px;
}

.booking-card {
  background: #f8fafc;
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 12px;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.booking-type {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.booking-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.booking-input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
  width: 100%;
}

.upload-small {
  margin-top: 10px;
  padding: 6px 14px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
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

/* 自定义输入 */
.custom-input-row {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.custom-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 14px;
}

.add-special-btn {
  padding: 12px 20px;
  background: #f1f5f9;
  border: 1px solid #ddd;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

/* 导航按钮 */
.nav-buttons {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.prev {
  flex: 1;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 15px;
  background: white;
  color: #64748b;
  font-size: 16px;
  cursor: pointer;
}

.next {
  flex: 2;
  padding: 15px;
  border: none;
  border-radius: 15px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>
