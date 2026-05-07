# ReelOS — Multi-tenant Reel automation SaaS

## Product Vision

**"DIY 版 HI Studio."**

任何本地小生意(健身房 / 美甲店 / 房产经纪 / 律所 / 咖啡店 / 瑜伽馆)都需要短视频内容。
他们没钱请代理($1-5K/月太贵),也没时间自己学。

**ReelOS 是 SaaS 工具:用户上传照片 + 选模板 + 输入文案,系统每周自动生成 5-10 条 Reel + 同步发到他们的 IG/TT/YT。**

差异于代运营:**自助、$30-100/月,大家都用得起**。

---

## 目标用户(MVP 阶段聚焦)

排序 by 「最痛 + 最愿付」:

1. **健身房/工作室教练** — 每天发 1 条 Reel 是行业标配,但他们普遍痛苦;愿付 $50-100/月
2. **房产经纪人** — 每个房源 + 每个区域都需要 Reel;$50-200/月
3. **美甲/纹身师/美发** — 作品照天天有,缺的是包装 + 发布;$30-50/月
4. **律所/会计师** — 内容驱动获客,大律所自己有团队但小律所是空白;$100-200/月
5. **本地咖啡店/烘焙坊** — 类似 HI 的客户群;$30-50/月

**MVP 目标用户**:健身房教练 + 美甲师(最大量 + 决策快)

---

## MVP 范围(最小可付费产品)

### 必有(Phase 1, 2-3 周)
- ✅ 用户注册 / 登录 (Clerk)
- ✅ 上传 4-10 张照片(行业模板对应)
- ✅ 选模板(预设 4 个:fitness / beauty / real-estate / general)
- ✅ 输入品牌信息(名字 / 颜色 / IG handle)
- ✅ 输入本周内容主题(2-3 行)
- ✅ 系统生成 5 条 Reel(用现有 publisher 流水线 + 多租户改造)
- ✅ 用户预览 + 批准
- ✅ 系统自动发到他们的 IG / TT(OAuth 接通)
- ✅ Stripe 月费订阅($30 / $50 / $100 三档)
- ✅ 简单 dashboard:本周发了几条、views

### 可推迟(Phase 2)
- AI 自动建议本周主题
- 自定义 BGM / 音乐库选择
- 多平台高级:YT Shorts / TikTok 同步
- A/B 测试不同模板
- 团队协作(多 user 一 brand)
- 视频分析(实际表现 vs 同行)
- White-label(代理商版本)

---

## 技术栈

```
Frontend:        Next.js 16 App Router + Tailwind + shadcn/ui
Auth:            Clerk (Vercel Marketplace 一键)
Database:        Neon Postgres (Vercel Marketplace)
Storage:         Vercel Blob (用户照片 + 渲染产出 mp4)
Background Jobs: Vercel Cron + Inngest 或 BullMQ
LLM:             AI Gateway → Llama 3.3 70B (caption gen)
Render:          内部:复用 publisher 的 HyperFrames 流水线 + Sandbox
Payment:         Stripe Subscriptions
IG / TT / YT:    现有的 OAuth + upload 代码
Deploy:          Vercel
```

**关键决策**:渲染要 OFF-Vercel,因为 Puppeteer + ffmpeg 太重。
- 选项 A:Vercel Sandbox(Firecracker microVM,新)
- 选项 B:私有 Mac mini / 自托管渲染机 (性价比高,但运维)
- 选项 C:Render Worker on AWS / Railway(传统)
- **建议:先用 Mac mini + ngrok exposed worker** 验证后再迁

---

## 数据模型(简化)

```typescript
// users (Clerk-managed)
// orgs / brands (multi-tenant)
type Brand = {
  id: string;
  name: string;           // "Sunset Yoga Brooklyn"
  industry: 'fitness' | 'beauty' | 'real_estate' | 'food' | 'legal' | 'other';
  brand_color: string;    // hex
  ig_user_id?: string;
  ig_token?: string;       // encrypted
  tt_user_id?: string;
  tt_token?: string;
  stripe_subscription_id?: string;
  plan: 'starter' | 'growth' | 'signature';
  created_at: timestamp;
};

type Asset = {
  id: string;
  brand_id: string;
  url: string;            // Vercel Blob URL
  type: 'photo' | 'video';
  uploaded_at: timestamp;
  used_in_reels: string[]; // reel ids
};

type Reel = {
  id: string;
  brand_id: string;
  template_id: string;
  status: 'pending' | 'rendering' | 'ready' | 'published' | 'failed';
  scheduled_at: timestamp;
  caption_yt?: jsonb;
  caption_ig?: text;
  caption_tt?: text;
  render_url?: string;     // Vercel Blob
  ig_url?: string;
  yt_url?: string;
  tt_url?: string;
};

type Template = {
  id: string;
  industry: string;
  hyperframes_spec: jsonb;
  fields_required: string[];
};
```

---

## 用户体验流程(MVP)

```
1. 注册 → 选行业 → 选模板 (Fitness / Beauty / RealEstate / General)
2. 上传 10 张照片 (drag-drop)
3. 输入品牌信息:名字、颜色、IG/TT handle
4. OAuth IG + TT (一键)
5. 进入 dashboard:看到本周 5 条 Reel 草稿
   - 每条:封面预览 + 文案编辑 + "approve" / "skip"
6. Approve → 自动按 schedule 发布(系统按 TOS 自动间隔 ≥2h)
7. 每周一系统自动用上传过的照片生成下周 5 条草稿,推送通知用户审核
```

**关键 UX 决策**:第一周用户上传 10 张,系统能滚 4 周。每月用户补 5 张就够。

---

## 定价

| Plan | 价格 | 月条数 | 平台 |
|---|---|---|---|
| **STARTER** | $30/mo | 8 | IG only |
| **GROWTH** | $60/mo | 20 | IG + TT |
| **PRO** | $120/mo | 40 | IG + TT + YT + 自定义 BGM |

**免费试用 7 天** + **首单 50% off** 第一个月。

---

## 单位经济(单位:每用户)

GROWTH 用户 $60/月:
- 渲染成本(Mac mini share):$2-5/mo
- Vercel Blob 存储:$1-3/mo
- AI Gateway(caption gen):$2-5/mo
- Stripe 手续费 2.9% + $0.30:$2/mo
- 客服 / 运营时间:~$5/mo (按低估算)
- **净利润 ~$40/mo per user**

100 用户 = $4K/mo 净
500 用户 = $20K/mo 净
1000 用户 = $40K/mo 净

---

## Build Phases

### Phase 0:产品化决策 (本周 — 已完成此文档)
- ✅ 定位 + MVP 范围 + 技术栈

### Phase 1:第一版 (3 周)
- Week 1:Next.js + Clerk + Neon 搭好骨架,brand CRUD,文件上传
- Week 2:渲染 worker(复用 publisher 代码,改 multi-tenant 路径),IG OAuth 接进来
- Week 3:Stripe + dashboard + 5 个真实用户内测

### Phase 2:商业化打磨 (3 周)
- A/B 模板,YT/TT 加进来
- 推送通知,referral
- 上 ProductHunt + 找 5 个本地工作室合作内推

### Phase 3:增长 (持续)
- SEO 着陆页 (per industry / per city)
- 付费投放小测
- 找 Vertical-specific 红人合作

---

## 关键风险 + 应对

1. **渲染成本失控** — 一个用户 100 条/月渲染 ≈ $50 算力。**应对**:模板预编译 + 缓存共用元素;Mac mini 自营优于云
2. **IG/TT 平台风控** — 多用户共用一个 token? **不行**。每个用户必须用自己的 OAuth token,我们只是 Schedule API 调用方。
3. **同质化** — 模板少 → 用户视频长得像。**应对**:第一年只保留 4-6 个核心模板,但每个有 10+ 风格变体。Phase 2 加 AI 生成模板。
4. **客户流失(churn)** — 小生意 SaaS 的 churn 通常 ~5-10%/月。**应对**:首月免费 → 第二月自动续费,第一周给客户看到 Reel 实际表现,降低退费冲动。
5. **法律 / 版权** — 用户上传的照片,平台不审核 → 出事谁背锅?**应对**:ToS 写清「用户负责所有上传内容版权」,平台不审核但会 takedown。

---

## 命名候选

- **ReelOS** ✅(主推 — 平台感,工具感)
- LocalReels
- ReelShop
- Brandloop
- HI Loop
- newhi.studio (但太接近代理 brand)

---

## 上线前 checklist

- [ ] Vercel 项目创建 + Neon + Clerk
- [ ] 域名:reelos.app 或类似(reelos.com 可能要花钱)
- [ ] Stripe 测试模式 → 生产模式
- [ ] IG 商业 App 重新申请(需要 multi-tenant scope)
- [ ] TT 商业 App 申请
- [ ] 4 个模板 design 定稿
- [ ] 隐私政策 + ToS(用 Termly 模板)
- [ ] ProductHunt 草稿 + launch tweet thread
