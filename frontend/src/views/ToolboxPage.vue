<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

interface ToolItem {
  key: string;
  icon: string;
  label: string;
  desc: string;
  color: string;
}

// ==============================
// 九宫格工具入口
// ==============================
const tools: ToolItem[] = [
  {
    key: "ai_chat",
    icon: "💬",
    label: "AI 助手",
    desc: "旅行任意问题",
    color: "#eff6ff",
  },
  {
    key: "ocr",
    icon: "📷",
    label: "OCR 识别",
    desc: "拍菜单/路牌",
    color: "#fef2f2",
  },
  {
    key: "translate",
    icon: "🌐",
    label: "拍照翻译",
    desc: "图片/文字翻译",
    color: "#f0fdf4",
  },
  {
    key: "exchange",
    icon: "💱",
    label: "汇率换算",
    desc: "实时换算",
    color: "#fffbeb",
  },
  {
    key: "weather",
    icon: "🌤️",
    label: "天气查询",
    desc: "目的地天气",
    color: "#ecfeff",
  },
  {
    key: "expense",
    icon: "💰",
    label: "记账",
    desc: "新增/统计消费",
    color: "#f5f3ff",
  },
  {
    key: "diary",
    icon: "📖",
    label: "旅行日记",
    desc: "记录每一段",
    color: "#fff7ed",
  },
  {
    key: "todo",
    icon: "✅",
    label: "待办清单",
    desc: "旅行任务管理",
    color: "#f1f5f9",
  },
  {
    key: "map",
    icon: "🗺️",
    label: "地图导航",
    desc: "路线/导航",
    color: "#fdf2f8",
  },
];

function openTool(tool: ToolItem) {
  // TODO: Day20+ 按工具类型路由分发
  // - ai_chat → /chat
  // - ocr → /toolbox/ocr
  // - translate → /toolbox/translate
  // - exchange → /toolbox/exchange
  // - weather → /toolbox/weather
  // - expense → /toolbox/expense
  // - diary → /toolbox/diary
  // - todo → /toolbox/todo
  // - map → /toolbox/map
  // 当前仅打印，不跳转（路由未定义）
  console.log("open tool:", tool.key);
}
</script>

<template>
  <div class="page">
    <header class="header">
      <button class="back-btn" @click="router.back()">←</button>
      <h1>旅行工具箱</h1>
    </header>
    <p class="sub">所有旅行工具，一站式入口</p>

    <div class="grid">
      <button
        v-for="tool in tools"
        :key="tool.key"
        class="tool-card"
        @click="openTool(tool)"
      >
        <div class="tool-icon-wrap" :style="{ background: tool.color }">
          <span class="tool-icon">{{ tool.icon }}</span>
        </div>
        <div class="tool-label">{{ tool.label }}</div>
        <div class="tool-desc">{{ tool.desc }}</div>
      </button>
    </div>

    <!-- TODO: Day20+ 各工具子页面接入 -->
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
  margin-bottom: 25px;
  margin-left: 48px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.tool-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 12px;
  background: white;
  border-radius: 18px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s;
}

.tool-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(37, 99, 235, 0.12);
  border-color: #bfdbfe;
}

.tool-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-icon {
  font-size: 28px;
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
