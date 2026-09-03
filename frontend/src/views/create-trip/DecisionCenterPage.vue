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
const destination = computed(() => tripStore.destination || "未填写");
const startDate = computed(() => tripStore.start_date || "未填写");
const endDate = computed(() => tripStore.end_date || "未填写");
const people = computed(() => tripStore.people_count || 1);
const budget = computed(() => tripStore.budget || 0);

// ==============================
// 模块二：AI 已识别信息（静态展示）
// ==============================
// TODO: Day20+ 接入 Weather API + Rule Engine 自动识别
const aiRecognizedInfo = ref([
  { icon: "📍", label: "目的地", value: destination.value },
  { icon: "📅", label: "日期", value: `${startDate.value} ~ ${endDate.value}` },
  { icon: "🌦️", label: "天气概览", value: "23-29°C 有降雨概率" },
  { icon: "🛂", label: "签注/签证", value: "港澳通行证需有效签注" },
  { icon: "💱", label: "汇率", value: "1 CNY ≈ 1.08 HKD" },
  { icon: "🟡", label: "旺季提醒", value: "周末酒店价格较高" },
  { icon: "🚇", label: "交通卡", value: "推荐八达通" },
  { icon: "🔌", label: "转换插头", value: "香港使用英标插头" },
]);

// ==============================
// 模块三：旅行角色（四选一）
// ==============================
const travelRoles = [
  { key: "hardcore", label: "特种兵", icon: "🚶", desc: "高强度、多景点、早起" },
  { key: "citywalk", label: "City Walk", icon: "🏙️", desc: "随性漫步、不强求" },
  { key: "deep", label: "深度体验", icon: "🌿", desc: "少而精、慢慢品" },
  { key: "relax", label: "休闲度假", icon: "😎", desc: "睡到自然醒" },
];
const selectedRole = ref("");

function selectRole(key: string) {
  selectedRole.value = key;
  // 角色联动预设
  if (key === "hardcore") {
    walkDistance.value = 20;
    energyLevel.value = 3;
    startTime.value = "08:00";
    endTime.value = "22:00";
    luggageType.value = "backpack";
    needNap.value = false;
  } else if (key === "citywalk") {
    walkDistance.value = 12;
    energyLevel.value = 2;
    startTime.value = "09:00";
    endTime.value = "20:00";
  } else if (key === "deep") {
    walkDistance.value = 8;
    energyLevel.value = 2;
    startTime.value = "10:00";
    endTime.value = "21:00";
  } else if (key === "relax") {
    walkDistance.value = 5;
    energyLevel.value = 1;
    startTime.value = "11:00";
    endTime.value = "19:00";
    needNap.value = true;
  }
}

// ==============================
// 模块四：核心决策（6 个问题）
// ==============================

// 1. 行李
const luggageOptions = [
  { key: "backpack", label: "背包", icon: "🎒" },
  { key: "20inch", label: "20寸行李箱", icon: "🧳" },
  { key: "24inch", label: "24寸行李箱", icon: "🧳" },
  { key: "28inch", label: "28寸行李箱", icon: "🧳" },
  { key: "multiple", label: "两个及以上", icon: "🎒" },
];
const luggageType = ref("");

// 2. 鞋子
const shoeOptions = [
  { key: "sneaker", label: "运动鞋", icon: "👟" },
  { key: "casual", label: "休闲鞋", icon: "👞" },
  { key: "sandal", label: "凉鞋", icon: "🩴" },
  { key: "leather", label: "皮鞋", icon: "👞" },
  { key: "heel", label: "高跟鞋", icon: "👠" },
];
const shoeType = ref("");

// 3. 今日体力
const energyOptions = [
  { key: 1, label: "疲惫", icon: "😴" },
  { key: 2, label: "一般", icon: "🙂" },
  { key: 3, label: "精力满满", icon: "💪" },
];
const energyLevel = ref(2);

// 4. 每日步行接受程度
const walkDistance = ref(10); // km，范围 3-25

// 5. 今日特殊目标
const goalOptions = ["拍照", "美食", "购物", "演唱会", "日落夜景", "乐园", "咖啡店办公"];
const selectedGoals = ref<string[]>([]);

function toggleGoal(opt: string) {
  const idx = selectedGoals.value.indexOf(opt);
  if (idx > -1) selectedGoals.value.splice(idx, 1);
  else selectedGoals.value.push(opt);
}

// 6. 时间
const startTime = ref("09:00");
const endTime = ref("21:00");

// ==============================
// 模块五：Wishlist（占位）
// ==============================
interface WishlistItem {
  name: string;
  category: string;
  isMustVisit: boolean;
}
const wishlist = ref<WishlistItem[]>([]);

const wishlistCategoryOptions = ["景点", "美食", "购物", "文化", "其他"];

function addWishlist() {
  wishlist.value.push({ name: "", category: "景点", isMustVisit: false });
}

function removeWishlist(index: number) {
  wishlist.value.splice(index, 1);
}

// TODO: Day20+ 对接 Wishlist API
// GET /api/travel/{travel_id}/wishlist
// POST /api/travel/{travel_id}/wishlist
// PATCH /api/wishlist/{wishlist_id}
// DELETE /api/wishlist/{wishlist_id}

// ==============================
// 模块六：风险提醒（占位）
// ==============================
const risks = ref<any[]>([]);
// TODO: Day20+ 对接 Risk API
// GET /api/travel/{travel_id}/risk-check

// ==============================
// 模块七：高级决策（折叠）
// ==============================
const showAdvanced = ref(false);

// A. 天气适应
const weatherPrefs = ["怕晒", "怕热", "怕雨", "带雨伞", "带防晒", "带外套"];
const selectedWeatherPrefs = ref<string[]>([]);

// B. 身体状态
const healthPrefs = ["晕车", "晕船", "恐高", "低血糖", "需要午休"];
const selectedHealthPrefs = ref<string[]>([]);
const needNap = ref(false);

// C. 装备
const equipmentOptions = ["相机", "三脚架", "自拍杆", "电脑/iPad", "保温杯", "充电宝"];
const selectedEquipment = ref<string[]>([]);

// D. 同行人
const groupOptions = ["老人同行", "儿童同行", "婴儿车", "宠物同行"];
const selectedGroup = ref<string[]>([]);

// E. 特殊需求
const specialNeeds = ["无障碍路线", "素食", "清真", "安静环境", "怕排队"];
const selectedSpecialNeeds = ref<string[]>([]);

function toggleItem(list: string[], item: string) {
  const idx = list.indexOf(item);
  if (idx > -1) list.splice(idx, 1);
  else list.push(item);
}

// ==============================
// 模块八：生成
// ==============================
function generate() {
  // TODO: 检查必填 + 高风险 → 弹出 AI 修改建议
  // 将全部决策上下文写入 store（后续 AI Prompt Builder 使用）
  tripStore.patchForm({
    planning_mode: 50,
    travel_role: selectedRole.value,
    luggage_type: luggageType.value,
    shoe_type: shoeType.value,
    energy_level: energyLevel.value,
    walk_distance: walkDistance.value,
    today_goals: [...selectedGoals.value],
    activity_start_time: startTime.value,
    activity_end_time: endTime.value,
    wishlist: wishlist.value.map((w) => ({ ...w })),
    weather_prefs: [...selectedWeatherPrefs.value],
    health_prefs: [...selectedHealthPrefs.value],
    need_nap: needNap.value,
    equipment: [...selectedEquipment.value],
    group_prefs: [...selectedGroup.value],
    special_needs: [...selectedSpecialNeeds.value],
  });
  router.push("/create-trip/generate");
}

function previous() {
  router.push("/create-trip/preference");
}
</script>

<template>
  <div class="page">
    <TripNavigation :currentStep="4" :completedSteps="[1, 2, 3]" />

    <h1>AI 决策中心</h1>
    <p class="sub">告诉 AI 这一次旅行的实时状态，AI 会动态调整路线和节奏。</p>

    <!-- 模块二：AI 已识别信息 -->
    <div class="card">
      <div class="title-row">
        <h2>AI 已识别信息</h2>
        <span class="badge">自动识别</span>
      </div>
      <div class="info-grid">
        <div v-for="item in aiRecognizedInfo" :key="item.label" class="info-card">
          <span class="info-icon">{{ item.icon }}</span>
          <div>
            <div class="info-label">{{ item.label }}</div>
            <div class="info-value">{{ item.value }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 模块三：旅行角色 -->
    <div class="card">
      <h2>旅行角色</h2>
      <p class="hint">一句话决定今天怎么玩</p>
      <div class="role-grid">
        <button
          v-for="role in travelRoles"
          :key="role.key"
          class="role-card"
          :class="{ roleActive: selectedRole === role.key }"
          @click="selectRole(role.key)"
        >
          <span class="role-icon">{{ role.icon }}</span>
          <span class="role-label">{{ role.label }}</span>
          <span class="role-desc">{{ role.desc }}</span>
        </button>
      </div>
    </div>

    <!-- 模块四：核心决策 -->
    <div class="card">
      <h2>核心决策</h2>

      <!-- 1. 行李 -->
      <div class="decision-block">
        <label class="decision-label">行李情况</label>
        <div class="chips">
          <button
            v-for="opt in luggageOptions"
            :key="opt.key"
            class="chip"
            :class="{ chipActive: luggageType === opt.key }"
            @click="luggageType = opt.key"
          >
            {{ opt.icon }} {{ opt.label }}
          </button>
        </div>
      </div>

      <!-- 2. 鞋子 -->
      <div class="decision-block">
        <label class="decision-label">今日穿着</label>
        <div class="chips">
          <button
            v-for="opt in shoeOptions"
            :key="opt.key"
            class="chip"
            :class="{ chipActive: shoeType === opt.key }"
            @click="shoeType = opt.key"
          >
            {{ opt.icon }} {{ opt.label }}
          </button>
        </div>
      </div>

      <!-- 3. 体力 -->
      <div class="decision-block">
        <label class="decision-label">今日体力</label>
        <div class="energy-row">
          <button
            v-for="opt in energyOptions"
            :key="opt.key"
            class="energy-btn"
            :class="{ energyActive: energyLevel === opt.key }"
            @click="energyLevel = opt.key"
          >
            {{ opt.icon }} {{ opt.label }}
          </button>
        </div>
      </div>

      <!-- 4. 步行接受程度 -->
      <div class="decision-block">
        <label class="decision-label">每日步行接受程度</label>
        <div class="slider-row">
          <span>3km</span>
          <input type="range" min="3" max="25" v-model.number="walkDistance" class="slider" />
          <span>25km</span>
        </div>
        <div class="slider-value">当前：{{ walkDistance }}km/天</div>
      </div>

      <!-- 5. 今日特殊目标 -->
      <div class="decision-block">
        <label class="decision-label">今日特殊目标</label>
        <div class="chips">
          <button
            v-for="opt in goalOptions"
            :key="opt"
            class="chip"
            :class="{ chipActive: selectedGoals.includes(opt) }"
            @click="toggleGoal(opt)"
          >
            {{ opt }}
          </button>
        </div>
      </div>

      <!-- 6. 时间 -->
      <div class="decision-block">
        <label class="decision-label">活动时间</label>
        <div class="time-row">
          <input type="time" v-model="startTime" class="time-input" />
          <span>至</span>
          <input type="time" v-model="endTime" class="time-input" />
        </div>
      </div>
    </div>

    <!-- 模块五：Wishlist -->
    <div class="card">
      <div class="title-row">
        <h2>愿望清单 Wishlist</h2>
        <button class="add-btn" @click="addWishlist">+ 添加地点</button>
      </div>
      <div v-if="wishlist.length === 0" class="empty-hint">
        暂无愿望地点，添加你想去但没有具体安排的地方
      </div>
      <div v-for="(item, index) in wishlist" :key="index" class="wishlist-row">
        <input v-model="item.name" placeholder="地点名称" class="wishlist-input" />
        <select v-model="item.category" class="wishlist-select">
          <option v-for="c in wishlistCategoryOptions" :key="c" :value="c">{{ c }}</option>
        </select>
        <label class="must-visit">
          <input type="checkbox" v-model="item.isMustVisit" />
          必去
        </label>
        <button class="del-btn" @click="removeWishlist(index)">×</button>
      </div>
      <!-- TODO: Day20+ 对接 Wishlist API -->
    </div>

    <!-- 模块六：风险提醒 -->
    <div class="card" v-if="risks.length">
      <h2>风险提醒</h2>
      <div v-for="(risk, i) in risks" :key="i" class="risk-item" :class="risk.level">
        <span v-if="risk.level === 'high'">🔴</span>
        <span v-else-if="risk.level === 'medium'">🟠</span>
        <span v-else>ℹ️</span>
        <strong>{{ risk.type }}</strong> — {{ risk.message }}
      </div>
    </div>
    <!-- TODO: Day20+ 对接 Risk API -->
    <!-- GET /api/travel/{travel_id}/risk-check -->

    <!-- 模块七：高级决策 -->
    <div class="card">
      <button class="collapse-header" @click="showAdvanced = !showAdvanced">
        <span>高级决策（可选）</span>
        <span>{{ showAdvanced ? "▾" : "▸" }}</span>
      </button>

      <div v-show="showAdvanced" class="advanced-content">
        <!-- A. 天气适应 -->
        <div class="decision-block">
          <label class="decision-label">天气适应</label>
          <div class="chips">
            <button
              v-for="opt in weatherPrefs"
              :key="opt"
              class="chip"
              :class="{ chipActive: selectedWeatherPrefs.includes(opt) }"
              @click="toggleItem(selectedWeatherPrefs, opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>

        <!-- B. 身体状态 -->
        <div class="decision-block">
          <label class="decision-label">身体状态</label>
          <div class="chips">
            <button
              v-for="opt in healthPrefs"
              :key="opt"
              class="chip"
              :class="{ chipActive: selectedHealthPrefs.includes(opt) }"
              @click="toggleItem(selectedHealthPrefs, opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>

        <!-- C. 装备 -->
        <div class="decision-block">
          <label class="decision-label">装备</label>
          <div class="chips">
            <button
              v-for="opt in equipmentOptions"
              :key="opt"
              class="chip"
              :class="{ chipActive: selectedEquipment.includes(opt) }"
              @click="toggleItem(selectedEquipment, opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>

        <!-- D. 同行人 -->
        <div class="decision-block">
          <label class="decision-label">同行人</label>
          <div class="chips">
            <button
              v-for="opt in groupOptions"
              :key="opt"
              class="chip"
              :class="{ chipActive: selectedGroup.includes(opt) }"
              @click="toggleItem(selectedGroup, opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>

        <!-- E. 特殊需求 -->
        <div class="decision-block">
          <label class="decision-label">特殊需求</label>
          <div class="chips">
            <button
              v-for="opt in specialNeeds"
              :key="opt"
              class="chip"
              :class="{ chipActive: selectedSpecialNeeds.includes(opt) }"
              @click="toggleItem(selectedSpecialNeeds, opt)"
            >
              {{ opt }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 模块八：生成按钮 -->
    <div class="nav-buttons">
      <button class="prev" @click="previous">← 上一步</button>
      <button class="generate-btn" @click="generate">生成旅行计划 →</button>
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

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.badge {
  font-size: 12px;
  color: #2563eb;
  background: #eff6ff;
  padding: 4px 10px;
  border-radius: 10px;
}

/* AI 已识别信息 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8fafc;
  padding: 12px;
  border-radius: 12px;
}

.info-icon {
  font-size: 20px;
}

.info-label {
  font-size: 12px;
  color: #94a3b8;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
}

/* 旅行角色 */
.role-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.role-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.role-card:hover {
  border-color: #93c5fd;
}

.roleActive {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.role-icon {
  font-size: 24px;
}

.role-label {
  font-size: 15px;
  font-weight: 600;
}

.role-desc {
  font-size: 12px;
  opacity: 0.7;
}

/* 核心决策 */
.decision-block {
  margin-bottom: 20px;
}

.decision-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
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

/* 体力 */
.energy-row {
  display: flex;
  gap: 10px;
}

.energy-btn {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.energyActive {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

/* Slider */
.slider-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.slider {
  flex: 1;
  height: 6px;
}

.slider-value {
  margin-top: 6px;
  font-size: 13px;
  color: #64748b;
}

/* 时间 */
.time-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-input {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
}

/* Wishlist */
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

.wishlist-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.wishlist-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
}

.wishlist-select {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 14px;
}

.must-visit {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  white-space: nowrap;
  cursor: pointer;
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

/* 风险 */
.risk-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 14px;
}

.risk-item.high {
  color: #dc2626;
  background: #fef2f2;
}

.risk-item.medium {
  color: #c2410c;
  background: #fff7ed;
}

.risk-item.low {
  color: #2563eb;
  background: #eff6ff;
}

/* 折叠 */
.collapse-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 12px 0;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}

.advanced-content {
  margin-top: 15px;
  border-top: 1px solid #eee;
  padding-top: 15px;
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

.generate-btn {
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
