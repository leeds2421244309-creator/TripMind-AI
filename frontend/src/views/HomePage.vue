<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// ==============================
// 模块二：AI 一句话生成
// ==============================
const aiPrompt = ref("");
const aiExamples = [
  "国庆去香港玩三天，两个人，预算3000",
  "周末杭州两日游，带娃",
  "下个月去日本京都深度游5天",
];

function fillExample(text: string) {
  aiPrompt.value = text;
}

function generateByAI() {
  // TODO: Day20+ 进入 AI Chat 页面（/chat 路由待新增）
  // 当前仅跳转到创建流程，并把 prompt 作为旅行名称传入
  if (!aiPrompt.value.trim()) return;
  // TODO: 后续对接 AI Chat 模式
  router.push("/create-trip");
}

// ==============================
// 模块三：普通创建模式
// ==============================
function goCreateFlow() {
  router.push("/create-trip");
}

// ==============================
// 模块四：最近旅行（Mock 数据）
// ==============================
interface TravelCard {
  id: number;
  title: string;
  destination: string;
  date: string;
  status: "planning" | "ongoing" | "completed";
  statusText: string;
}

const recentTravels = ref<TravelCard[]>([
  {
    id: 1,
    title: "香港三日游",
    destination: "香港",
    date: "2026-10-01 ~ 2026-10-03",
    status: "planning",
    statusText: "规划中",
  },
  {
    id: 2,
    title: "杭州周末游",
    destination: "杭州",
    date: "2026-09-20 ~ 2026-09-21",
    status: "ongoing",
    statusText: "进行中",
  },
  {
    id: 3,
    title: "日本京都深度游",
    destination: "京都",
    date: "2026-08-10 ~ 2026-08-15",
    status: "completed",
    statusText: "已完成",
  },
]);

function openTravel(item: TravelCard) {
  // 进入旅行状态中心，按阶段切换页面
  router.push("/status");
}

// ==============================
// 模块五：收藏计划（Mock 数据）
// ==============================
const favoritePlans = ref<TravelCard[]>([
  {
    id: 101,
    title: "特种兵香港",
    destination: "香港",
    date: "3 天 / 2 人",
    status: "planning",
    statusText: "收藏",
  },
  {
    id: 102,
    title: "京都慢生活",
    destination: "京都",
    date: "5 天 / 2 人",
    status: "planning",
    statusText: "收藏",
  },
]);

function openFavorite(item: TravelCard) {
  // 收藏计划也跳转状态中心
  router.push("/status");
}

// ==============================
// 模块六：常用工具入口
// ==============================
const tools = [
  { key: "chat", icon: "💬", label: "AI 问答", desc: "旅行任意问题" },
  { key: "exchange", icon: "💱", label: "汇率工具", desc: "实时换算" },
  { key: "translate", icon: "🌐", label: "翻译工具", desc: "多语言翻译" },
  { key: "diary", icon: "📖", label: "旅行日记", desc: "记录每一段" },
];

function openTool(tool: { key: string }) {
  // 进入 ToolboxPage，再由工具卡片选择具体子工具
  router.push("/toolbox");
}
</script>

<template>
  <div class="page">
    <!-- 模块一：顶部欢迎区域 -->
    <header class="hero">
      <div class="logo">TripMind AI</div>
      <h1>AI 帮你完成从旅行规划到旅行执行的全过程</h1>
      <p class="sub">一句话生成计划，或一步步定制你的专属旅程</p>
    </header>

    <!-- 模块二：AI 一句话生成 -->
    <section class="card hero-card">
      <label class="block-label">一句话生成旅行计划</label>
      <input
        v-model="aiPrompt"
        class="ai-input"
        placeholder="例如：国庆去香港玩三天，两个人，预算3000"
        @keyup.enter="generateByAI"
      />
      <div class="examples">
        <button
          v-for="ex in aiExamples"
          :key="ex"
          class="example-chip"
          @click="fillExample(ex)"
        >
          {{ ex }}
        </button>
      </div>
      <button class="primary-btn" @click="generateByAI">⚡ 立即生成</button>
    </section>

    <!-- 模块三：普通创建模式 -->
    <section class="card">
      <div class="row-between">
        <div>
          <div class="card-title">普通创建模式</div>
          <div class="card-desc">逐页填写：基础 → 预算 → 偏好 → 决策 → 生成</div>
        </div>
        <button class="outline-btn" @click="goCreateFlow">创建旅行计划 →</button>
      </div>
    </section>

    <!-- 模块四：最近旅行 -->
    <section class="card">
      <div class="title-row">
        <h2>最近旅行</h2>
        <span class="badge">Mock</span>
      </div>
      <div v-if="recentTravels.length === 0" class="empty">暂无旅行记录</div>
      <div class="travel-grid">
        <div
          v-for="item in recentTravels"
          :key="item.id"
          class="travel-card"
          :class="item.status"
          @click="openTravel(item)"
        >
          <div class="travel-top">
            <span class="travel-title">{{ item.title }}</span>
            <span class="status-tag" :class="item.status">{{ item.statusText }}</span>
          </div>
          <div class="travel-meta">📍 {{ item.destination }}</div>
          <div class="travel-meta">📅 {{ item.date }}</div>
        </div>
      </div>
    </section>

    <!-- 模块五：收藏计划 -->
    <section class="card">
      <div class="title-row">
        <h2>收藏计划</h2>
        <span class="badge">Mock</span>
      </div>
      <div v-if="favoritePlans.length === 0" class="empty">暂无收藏</div>
      <div class="travel-grid">
        <div
          v-for="item in favoritePlans"
          :key="item.id"
          class="travel-card favorite"
          @click="openFavorite(item)"
        >
          <div class="travel-top">
            <span class="travel-title">{{ item.title }}</span>
            <span class="status-tag">⭐ {{ item.statusText }}</span>
          </div>
          <div class="travel-meta">📍 {{ item.destination }}</div>
          <div class="travel-meta">👥 {{ item.date }}</div>
        </div>
      </div>
    </section>

    <!-- 模块六：常用工具入口 -->
    <section class="card">
      <h2>常用工具</h2>
      <div class="tools-grid">
        <button
          v-for="tool in tools"
          :key="tool.key"
          class="tool-card"
          @click="openTool(tool)"
        >
          <span class="tool-icon">{{ tool.icon }}</span>
          <span class="tool-label">{{ tool.label }}</span>
          <span class="tool-desc">{{ tool.desc }}</span>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page {
  max-width: 720px;
  margin: auto;
  padding: 30px 20px;
}

/* Hero */
.hero {
  text-align: center;
  margin-bottom: 25px;
}

.logo {
  display: inline-block;
  font-size: 24px;
  font-weight: 700;
  color: #2563eb;
  margin-bottom: 12px;
  letter-spacing: 1px;
}

.hero h1 {
  font-size: 26px;
  line-height: 1.4;
  margin-bottom: 8px;
}

.sub {
  color: #64748b;
  font-size: 14px;
}

/* Card 通用 */
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

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.badge {
  font-size: 12px;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 10px;
}

.block-label {
  display: block;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 10px;
  color: #475569;
}

/* AI 输入 */
.hero-card {
  background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
}

.ai-input {
  width: 100%;
  padding: 15px;
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  font-size: 15px;
  background: white;
  box-sizing: border-box;
}

.ai-input:focus {
  outline: none;
  border-color: #2563eb;
}

.examples {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.example-chip {
  border: 1px solid #ddd;
  background: white;
  padding: 6px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  color: #475569;
  transition: all 0.2s;
}

.example-chip:hover {
  border-color: #2563eb;
  color: #2563eb;
}

.primary-btn {
  margin-top: 15px;
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

.primary-btn:hover {
  background: #1d4ed8;
}

/* 普通创建 */
.row-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
}

.card-desc {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 4px;
}

.outline-btn {
  padding: 12px 18px;
  border: 1px solid #2563eb;
  background: white;
  color: #2563eb;
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s;
}

.outline-btn:hover {
  background: #eff6ff;
}

/* 旅行卡片 */
.empty {
  text-align: center;
  padding: 20px;
  color: #94a3b8;
  font-size: 14px;
}

.travel-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.travel-card {
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s;
}

.travel-card:hover {
  border-color: #93c5fd;
  background: white;
  transform: translateY(-2px);
}

.travel-card.favorite {
  background: #fffbeb;
  border-color: #fde68a;
}

.travel-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.travel-title {
  font-size: 15px;
  font-weight: 600;
}

.status-tag {
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  background: #e0e7ff;
  color: #4338ca;
}

.status-tag.planning {
  background: #e0e7ff;
  color: #4338ca;
}

.status-tag.ongoing {
  background: #dcfce7;
  color: #166534;
}

.status-tag.completed {
  background: #f1f5f9;
  color: #475569;
}

.travel-meta {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

/* 工具入口 */
.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.tool-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 14px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
}

.tool-card:hover {
  border-color: #93c5fd;
  background: #f8fafc;
}

.tool-icon {
  font-size: 22px;
}

.tool-label {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.tool-desc {
  font-size: 12px;
  color: #94a3b8;
}
</style>
