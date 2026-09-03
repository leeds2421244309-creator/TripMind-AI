/**
 * 预算风险规则配置
 * 来源：docs/product/budget风险提醒.md
 * 所有阈值为人均/天（人民币），除非另注
 */

// ==========================
// 类型定义
// ==========================
export type RiskLevel = "danger" | "warning" | "safe" | "good" | "info";

export interface RiskItem {
  level: RiskLevel;
  title: string;
  text: string;
}

// ==========================
// 1. 地区最低预算判定（人均/天）
// ==========================
interface RegionThreshold {
  danger: number;  // < danger → 🔴
  warning: number; // danger ~ warning → 🟠
  safe: number;    // warning ~ safe → 🟢
  // > safe → 🔵
}

// 关键词 → 地区匹配
const regionKeywords: Record<string, string[]> = {
  "香港": ["香港", "hk", "hong kong", "hongkong"],
  "澳门": ["澳门", "macau", "macao"],
  "日本东京": ["东京", "tokyo"],
  "日本大阪": ["大阪", "京都", "osaka", "kyoto"],
  "韩国首尔": ["首尔", "seoul"],
  "韩国釜山": ["釜山", "busan", "pusan"],
  "中国内地一二线": ["北京", "上海", "广州", "深圳", "杭州", "成都", "南京", "武汉", "西安", "重庆", "苏州", "天津"],
};

const regionThresholds: Record<string, RegionThreshold> = {
  "中国内地三四线": { danger: 150, warning: 220, safe: 400 },
  "中国内地一二线": { danger: 220, warning: 300, safe: 550 },
  "香港": { danger: 500, warning: 700, safe: 1200 },
  "澳门": { danger: 450, warning: 650, safe: 1000 },
  "韩国首尔": { danger: 600, warning: 800, safe: 1300 },
  "韩国釜山": { danger: 450, warning: 650, safe: 1000 },
  "日本东京": { danger: 700, warning: 900, safe: 1500 },
  "日本大阪": { danger: 650, warning: 850, safe: 1400 },
};

/** 根据目的地字符串匹配地区 */
export function detectRegion(destination: string): string {
  const lower = destination.toLowerCase();
  for (const [region, keywords] of Object.entries(regionKeywords)) {
    if (keywords.some(kw => lower.includes(kw.toLowerCase()))) {
      return region;
    }
  }
  return "中国内地三四线";
}

/** 获取地区阈值 */
export function getRegionThreshold(region: string): RegionThreshold {
  return regionThresholds[region] || regionThresholds["中国内地三四线"];
}

// ==========================
// 2. 住宿占比判定
// ==========================
interface RatioThreshold {
  ranges: { min: number; max: number; level: RiskLevel; label: string }[];
}

const hotelRatioRules: RatioThreshold = {
  ranges: [
    { min: 0, max: 0, level: "danger", label: "未规划" },
    { min: 0, max: 15, level: "danger", label: "严重偏低" },
    { min: 15, max: 25, level: "warning", label: "偏低" },
    { min: 25, max: 40, level: "safe", label: "推荐区间" },
    { min: 40, max: 50, level: "warning", label: "偏高" },
    { min: 50, max: 100, level: "danger", label: "过高" },
  ],
};

// 地区特殊住宿推荐占比
const hotelRatioByRegion: Record<string, [number, number]> = {
  "中国内地三四线": [20, 35],
  "中国内地一二线": [20, 35],
  "香港": [30, 45],
  "澳门": [30, 45],
  "日本东京": [30, 45],
  "日本大阪": [30, 45],
  "韩国首尔": [30, 45],
  "韩国釜山": [30, 45],
};

// ==========================
// 3. 餐饮占比判定
// ==========================
const foodRatioRules: RatioThreshold = {
  ranges: [
    { min: 0, max: 0, level: "danger", label: "未规划" },
    { min: 0, max: 8, level: "danger", label: "严重不足" },
    { min: 8, max: 12, level: "warning", label: "偏低" },
    { min: 12, max: 25, level: "safe", label: "推荐区间" },
    { min: 25, max: 35, level: "warning", label: "较高" },
    { min: 35, max: 100, level: "danger", label: "过高" },
  ],
};

// 每日餐饮最低值（人均/天）
const foodDailyByRegion: Record<string, { min: number; comfort: [number, number] }> = {
  "中国内地三四线": { min: 50, comfort: [80, 150] },
  "中国内地一二线": { min: 60, comfort: [100, 180] },
  "香港": { min: 120, comfort: [180, 320] },
  "澳门": { min: 100, comfort: [150, 280] },
  "日本东京": { min: 150, comfort: [220, 420] },
  "日本大阪": { min: 150, comfort: [220, 420] },
  "韩国首尔": { min: 120, comfort: [200, 350] },
  "韩国釜山": { min: 120, comfort: [200, 350] },
};

// ==========================
// 4. 大交通占比判定
// ==========================
const transportRatioRules: RatioThreshold = {
  ranges: [
    { min: 0, max: 0, level: "danger", label: "未规划" },
    { min: 0, max: 10, level: "warning", label: "偏低" },
    { min: 10, max: 30, level: "safe", label: "推荐区间" },
    { min: 30, max: 40, level: "warning", label: "偏高" },
    { min: 40, max: 100, level: "danger", label: "过高" },
  ],
};

// ==========================
// 5. 市内交通每日预算判定
// ==========================
const cityTransportDailyByRegion: Record<string, { low: number; good: [number, number] }> = {
  "中国内地三四线": { low: 20, good: [20, 60] },
  "中国内地一二线": { low: 20, good: [20, 60] },
  "香港": { low: 35, good: [35, 80] },
  "澳门": { low: 35, good: [35, 80] },
  "日本东京": { low: 50, good: [50, 120] },
  "日本大阪": { low: 50, good: [50, 120] },
  "韩国首尔": { low: 50, good: [50, 120] },
  "韩国釜山": { low: 50, good: [50, 120] },
};

// ==========================
// 6. 景点门票占比判定
// ==========================
const ticketRatioRules: RatioThreshold = {
  ranges: [
    { min: 0, max: 0, level: "info", label: "无门票景点" },
    { min: 1, max: 8, level: "safe", label: "城市漫游" },
    { min: 8, max: 20, level: "safe", label: "推荐区间" },
    { min: 20, max: 30, level: "warning", label: "偏高" },
    { min: 30, max: 100, level: "danger", label: "高门票消费" },
  ],
};

// ==========================
// 7. 备用金占比判定
// ==========================
const reserveRatioRules: RatioThreshold = {
  ranges: [
    { min: 0, max: 0, level: "danger", label: "无备用金" },
    { min: 1, max: 5, level: "warning", label: "偏低" },
    { min: 5, max: 10, level: "safe", label: "推荐区间" },
    { min: 10, max: 15, level: "good", label: "宽裕" },
    { min: 15, max: 100, level: "info", label: "较高备用预算" },
  ],
};

// ==========================
// 辅助函数
// ==========================

/** 按占比查等级 */
function checkRatio(rules: RatioThreshold, ratio: number): { level: RiskLevel; label: string } | null {
  for (const r of rules.ranges) {
    if (ratio >= r.min && ratio < r.max) {
      return { level: r.level, label: r.label };
    }
  }
  // 处理 100% 边界
  const last = rules.ranges[rules.ranges.length - 1];
  if (ratio >= last.min) return { level: last.level, label: last.label };
  return null;
}

// ==========================
// 综合风险检查入口
// ==========================

export interface BudgetCheckInput {
  destination: string;
  totalBudget: number;
  peopleCount: number;
  tripDays: number;
  perPersonDaily: number;       // 人均/天
  items: {
    name: string;
    amount: number;
  }[];
}

export function checkBudgetRisks(input: BudgetCheckInput): RiskItem[] {
  const risks: RiskItem[] = [];
  const region = detectRegion(input.destination);
  const threshold = getRegionThreshold(region);
  const total = input.totalBudget;
  const perPersonDaily = input.perPersonDaily;

  // 只有总预算 > 0 才检查
  if (total <= 0) return risks;

  // --- 1. 地区人均每日预算 ---
  if (perPersonDaily > 0) {
    if (perPersonDaily < threshold.danger) {
      risks.push({
        level: "danger",
        title: "人均预算过低",
        text: `${region}人均每日建议 ≥ ¥${threshold.warning}，当前仅 ¥${perPersonDaily}/天`,
      });
    } else if (perPersonDaily < threshold.warning) {
      risks.push({
        level: "warning",
        title: "人均预算偏低",
        text: `${region}人均每日建议 ¥${threshold.warning}~${threshold.safe}，当前 ¥${perPersonDaily}/天`,
      });
    }
  }

  // --- 2. 总预算覆盖率 ---
  const recommendedMin = threshold.warning * input.peopleCount * input.tripDays;
  if (recommendedMin > 0 && total > 0) {
    const coverage = (total / recommendedMin) * 100;
    if (coverage < 80) {
      risks.push({
        level: "danger",
        title: "预算严重不足",
        text: `建议最低预算 ¥${recommendedMin}（${region}），当前 ¥${total}（覆盖率 ${Math.round(coverage)}%）`,
      });
    } else if (coverage < 95) {
      risks.push({
        level: "warning",
        title: "预算略低",
        text: `建议最低预算 ¥${recommendedMin}，当前 ¥${total}（覆盖率 ${Math.round(coverage)}%）`,
      });
    }
  }

  // --- 辅助：按名称找金额 ---
  const findItem = (name: string) => input.items.find(i => i.name === name);
  const getRatio = (item: { name: string; amount: number } | undefined) =>
    item && total > 0 ? (item.amount / total) * 100 : 0;

  // --- 3. 住宿占比 ---
  const hotel = findItem("住宿");
  const hotelRatio = getRatio(hotel);
  const hotelCheck = checkRatio(hotelRatioRules, hotelRatio);
  if (hotelCheck && hotelCheck.level !== "safe" && hotelCheck.level !== "good" && hotelCheck.level !== "info") {
    risks.push({
      level: hotelCheck.level,
      title: `住宿预算${hotelCheck.label}`,
      text: `住宿占比 ${hotelRatio.toFixed(1)}%，${region}推荐 ${hotelRatioByRegion[region]?.[0] || 20}~${hotelRatioByRegion[region]?.[1] || 40}%`,
    });
  }

  // --- 4. 餐饮占比 ---
  const food = findItem("餐饮");
  const foodRatio = getRatio(food);
  const foodCheck = checkRatio(foodRatioRules, foodRatio);
  if (foodCheck && foodCheck.level !== "safe" && foodCheck.level !== "good" && foodCheck.level !== "info") {
    risks.push({
      level: foodCheck.level,
      title: `餐饮预算${foodCheck.label}`,
      text: `餐饮占比 ${foodRatio.toFixed(1)}%，推荐 12%~25%`,
    });
  }
  // 餐饮每日最低值
  if (food && food.amount > 0 && perPersonDaily > 0) {
    const foodDaily = foodDailyByRegion[region];
    const foodPerPersonDaily = food.amount / (input.peopleCount * input.tripDays);
    if (foodDaily && foodPerPersonDaily < foodDaily.min) {
      risks.push({
        level: "warning",
        title: "餐饮每日预算不足",
        text: `${region}每日餐饮建议 ≥ ¥${foodDaily.min}/人，当前约 ¥${Math.round(foodPerPersonDaily)}/人`,
      });
    }
  }

  // --- 5. 大交通占比 ---
  const transport = findItem("大交通");
  const transportRatio = getRatio(transport);
  const transportCheck = checkRatio(transportRatioRules, transportRatio);
  if (transportCheck && transportCheck.level !== "safe" && transportCheck.level !== "good" && transportCheck.level !== "info") {
    risks.push({
      level: transportCheck.level,
      title: `大交通预算${transportCheck.label}`,
      text: `交通占比 ${transportRatio.toFixed(1)}%，推荐 10%~30%`,
    });
  }

  // --- 6. 市内交通每日预算 ---
  const cityTransport = findItem("市内交通");
  if (cityTransport && cityTransport.amount > 0 && input.tripDays > 0) {
    const cityDaily = cityTransport.amount / input.tripDays;
    const cityRules = cityTransportDailyByRegion[region];
    if (cityRules && cityDaily < cityRules.low) {
      risks.push({
        level: "danger",
        title: "市内交通预算偏低",
        text: `${region}每日市内交通建议 ≥ ¥${cityRules.low}，当前约 ¥${Math.round(cityDaily)}/天`,
      });
    } else if (cityRules && cityDaily > cityRules.good[1]) {
      risks.push({
        level: "warning",
        title: "市内交通预算偏高",
        text: `${region}每日市内交通建议 ¥${cityRules.good[0]}~${cityRules.good[1]}，当前约 ¥${Math.round(cityDaily)}/天`,
      });
    }
  }

  // --- 7. 景点门票占比 ---
  const tickets = findItem("门票娱乐") || findItem("门票");
  if (tickets && tickets.amount > 0) {
    const ticketRatio = getRatio(tickets);
    const ticketCheck = checkRatio(ticketRatioRules, ticketRatio);
    if (ticketCheck && ticketCheck.level !== "safe" && ticketCheck.level !== "good" && ticketCheck.level !== "info") {
      risks.push({
        level: ticketCheck.level,
        title: `景点预算${ticketCheck.label}`,
        text: `景点占比 ${ticketRatio.toFixed(1)}%，推荐 8%~20%`,
      });
    }
  }

  // --- 8. 备用金占比 ---
  const reserve = findItem("其他备用") || findItem("备用金");
  const reserveRatio = getRatio(reserve);
  const reserveCheck = checkRatio(reserveRatioRules, reserveRatio);
  if (reserveCheck && reserveCheck.level !== "safe" && reserveCheck.level !== "good" && reserveCheck.level !== "info") {
    risks.push({
      level: reserveCheck.level,
      title: `备用金${reserveCheck.label}`,
      text: `备用金占比 ${reserveRatio.toFixed(1)}%，推荐 5%~10%`,
    });
  }

  return risks;
}
