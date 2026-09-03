<script setup lang="ts">
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// ==============================
// 旅行生命周期阶段
// ==============================
type StageKey =
  | "creating"
  | "ai_planning"
  | "preparing"
  | "ongoing"
  | "completed";

interface Stage {
  key: StageKey;
  index: number;
  icon: string;
  label: string;
  desc: string;
  targetPage: string;
}

const stages: Stage[] = [
  {
    key: "creating",
    index: 1,
    icon: "✍️",
    label: "创建中",
    desc: "继续填写 Create Flow",
    targetPage: "CreateTravelPage",
  },
  {
    key: "ai_planning",
    index: 2,
    icon: "🤖",
    label: "AI 规划中",
    desc: "等待 AI 生成旅行计划",
    targetPage: "GeneratePlanPage",
  },
  {
    key: "preparing",
    index: 3,
    icon: "🎒",
    label: "出发准备",
    desc: "查看待办 / 订单 / 心愿清单",
    targetPage: "TripPreparationPage",
  },
  {
    key: "ongoing",
    index: 4,
    icon: "🧭",
    label: "行程进行中",
    desc: "今日行程 / 实时提醒 / 记账",
    targetPage: "TripDashboardPage",
  },
  {
    key: "completed",
    index: 5,
    icon: "🏁",
    label: "行程结束",
    desc: "查看总结 / 日记 / 花费",
    targetPage: "TripSummaryPage",
  },
];

// Mock 当前状态（行程进行中）
const currentStage = ref<StageKey>("ongoing");
const currentIndex = computed(() =>
  stages.findIndex((s) => s.key === currentStage.value)
);

// 每个阶段状态：completed / active / pending
function stageStatus(stage: Stage): "completed" | "active" | "pending" {
  const idx = stage.index - 1;
  if (idx < currentIndex.value) return "completed";
  if (idx === currentIndex.value) return "active";
  return "pending";
}

// Mock 旅行信息
const mockTrips = ref([
  {
    id: 1,
    title: "香港三日游",
    destination: "香港",
    startDate: "2026-10-01",
    endDate: "2026-10-03",
    stage: "ongoing" as StageKey,
  },
  {
    id: 2,
    title: "杭州周末游",
    destination: "杭州",
    startDate: "2026-09-20",
    endDate: "2026-09-21",
    stage: "preparing" as StageKey,
  },
  {
    id: 3,
    title: "京都深度游",
    destination: "京都",
    startDate: "2026-08-10",
    endDate: "2026-08-15",
    stage: "completed" as StageKey,
  },
]);

const activeTravel = ref(mockTrips.value[0]);

function selectTravel(id: number) {
  const found = mockTrips.value.find((t) => t.id === id);
  if (found) {
    activeTravel.value = found;
    currentStage.value = found.stage;
  }
}

function enterStage(stage: Stage) {
  // TODO: Day20+ 按阶段进入对应页面
  // - creating → /create-trip
  // - ai_planning → /create-trip/generate
  // - preparing → /travel/{id}/preparation（待新增）
  // - ongoing → /travel/{id}/dashboard（待新增）
  // - completed → /travel/{id}/summary（待新增）
  console.log("enter stage", stage.key, "→", stage.targetPage);
}

function back() {
  router.push("/");
}
</script>

<template>
  <div class="page">
    <header class="header">
      <button class="back-btn" @click="back">←</button>
      <h1>旅行状态中心</h1>
    </header>
    <p class="sub">查看每段旅行的生命周期，按阶段进入对应页面</p>

    <!-- 旅行切换 -->
    <div class="card">
      <h2>当前旅行</h2>
      <div class="travel-tabs">
        <button
          v-for="t in mockTravels"
          :key="t.id"
          class="travel-tab"
          :class="{ tabActive: t.id === activeTravel.id }"
          @click="selectTravel(t.id)"
        >
          {{ t.title }}
        </button>
      </div>
      <div class="travel-meta">
        📍 {{ activeTravel.destination }} ｜ 📅
        {{ activeTravel.startDate }} ~ {{ activeTravel.endDate }}
      </div>
    </div>

    <!-- Timeline -->
    <div class="card">
      <h2>生命周期</h2>
      <div class="timeline">
        <div
          v-for="stage in stages"
          :key="stage.key"
          class="timeline-item"
          :class="stageStatus(stage)"
        >
          <div class="timeline-left">
            <div class="timeline-dot">
              <span class="dot-icon">{{ stage.icon }}</span>
            </div>
            <div v-if="stage.index < stages.length" class="timeline-line"></div>
          </div>

          <div class="timeline-content">
            <div class="stage-header">
              <span class="stage-label">{{ stage.label }}</span>
              <span class="stage-tag" :class="stageStatus(stage)">
                {{
                  stageStatus(stage) === "completed"
                    ? "已完成"
                    : stageStatus(stage) === "active"
                    ? "进行中"
                    : "待进入"
                }}
              </span>
            </div>
            <div class="stage-desc">{{ stage.desc }}</div>
            <button
              class="stage-btn"
              :disabled="stageStatus(stage) === 'pending'"
              @click="enterStage(stage)"
            >
              {{
                stageStatus(stage) === "pending"
                  ? "未解锁"
                  : stageStatus(stage) === "completed"
                  ? "查看"
                  : "进入"
              }}
              →
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  max-width: 720px;
  margin: auto;
  padding: 30px 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.back-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
  font-size: 16px;
  color: #475569;
}

h1 {
  font-size: 28px;
  font-weight: 700;
}

.sub {
  color: #64748b;
  font-size: 14px;
  margin-bottom: 20px;
  margin-left: 48px;
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

/* 旅行切换 */
.travel-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.travel-tab {
  border: 1px solid #ddd;
  background: white;
  padding: 8px 14px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.travel-tab:hover {
  border-color: #93c5fd;
}

.tabActive {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.travel-meta {
  font-size: 13px;
  color: #64748b;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 10px;
}

/* Timeline */
.timeline {
  position: relative;
}

.timeline-item {
  display: flex;
  gap: 16px;
  min-height: 80px;
}

.timeline-left {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.timeline-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e2e8f0;
  flex-shrink: 0;
  transition: all 0.2s;
}

.dot-icon {
  font-size: 18px;
}

.timeline-line {
  width: 2px;
  flex: 1;
  background: #e2e8f0;
  margin: 4px 0;
}

.timeline-content {
  flex: 1;
  padding-bottom: 20px;
}

.stage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.stage-label {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.stage-tag {
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
  background: #f1f5f9;
  color: #64748b;
}

.stage-tag.completed {
  background: #dcfce7;
  color: #166534;
}

.stage-tag.active {
  background: #dbeafe;
  color: #1d4ed8;
}

.stage-tag.pending {
  background: #f1f5f9;
  color: #94a3b8;
}

.stage-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
}

.stage-btn {
  padding: 6px 14px;
  border: 1px solid #2563eb;
  background: white;
  color: #2563eb;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s;
}

.stage-btn:hover:not(:disabled) {
  background: #eff6ff;
}

.stage-btn:disabled {
  border-color: #e2e8f0;
  color: #cbd5e1;
  background: #f8fafc;
  cursor: not-allowed;
}

/* 阶段状态 */
.timeline-item.completed .timeline-dot {
  background: #dcfce7;
  border-color: #22c55e;
}

.timeline-item.active .timeline-dot {
  background: #dbeafe;
  border-color: #2563eb;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
}

.timeline-item.completed .timeline-line {
  background: #22c55e;
}

.timeline-item.active .timeline-line {
  background: linear-gradient(to bottom, #2563eb, #e2e8f0);
}
</style>
