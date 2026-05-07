# HI Things — 大纽约活动 Reel feed 策略

## 一句话定位

**"@HIThingsNY · 这周末大纽约都在干啥 · 每天 3 条 30 秒视频"**

复用 HI 的发布流水线,但内容垂类完全不同 — HI 是「吃」,HI Things 是「玩」。

---

## 数据源(免费 + 公开)

| 来源 | 类别 | 抓法 |
|---|---|---|
| **Eventbrite Public API** | 演唱会/展览/课程 | API key 免费,城市 + 日期搜 |
| **Fever** (feverup.com/new-york) | 高端体验/打卡活动 | 网页抓取 |
| **SeatGeek API** | 体育/演唱会 | API key,合作分成 |
| **NYC Parks 官网** (nycgovparks.org) | 户外/免费活动 | RSS feed |
| **Time Out NY** | 编辑挑选 | 网页抓取 |
| **Brooklyn Vegan / Resident Advisor** | 音乐 | RSS |
| **Reddit r/NYCEvents r/NYC r/AskNYC** | 用户提示 | API |
| **Yelp Events** | 本地 happenings | API key |
| **Town/library 官网 (NJ/LI/CT)** | 小镇活动 | 手动选 + RSS |

实施:写一个 `event_research_worker.py`(类比现有的 `research-worker.py`),每天早上自动抓取 + Llama 选择 + 输出 3 条精选。

---

## 视频模板设计

每条 30 秒结构(类似 HI 餐厅模板):
- **0-3s**: 标题大字 + 城市 emoji ("布鲁克林 · 这周六")
- **3-8s**: 活动名 + 时间(动画进入)
- **8-18s**: 活动照片(从官方 / Eventbrite 抓)
- **18-25s**: 票价 / 链接 / 看点
- **25-30s**: "@hithingsny · 关注获取每周更新"

复用 HyperFrames 模板,微调字段。

---

## 第一个月 Action Plan

### Week 1
- [ ] IG 账号 `@hithingsny` 注册 + Bio + 头像
- [ ] YouTube 频道 `HI Things NY` 创建
- [ ] TikTok `@hithingsny` 创建
- [ ] 改 publisher 模板,加 events 变体
- [ ] 写 `event_research_worker.py`(API 抓 Eventbrite + Fever)

### Week 2
- [ ] 第一周 21 条视频(3/天)上线
- [ ] Bio 链接到 hithings.vercel.app
- [ ] IG 故事每条转,加投票贴纸 "你会去吗?"
- [ ] 评论区主动回复(算法权重)

### Week 3-4
- [ ] 联系 5 个活动方 — 免费做一条 + 故事置顶,问是否愿意付 $50 升级
- [ ] 加 SeatGeek 联盟链接,看转化率
- [ ] 第一个付费置顶尝试($50)

---

## 月度收入预期

### 第 1 个月(冷启动,亏损可接受)
- 0-2 个付费置顶 = $0-100
- 联盟分成:可忽略
- **预期 -$50 净亏**(含工具费)

### 第 3 个月(假设有 1-2K IG 粉丝)
- 4-6 个付费置顶 / 周 = $200-300/周 = $800-1200/月
- 联盟分成:$100-300/月
- **预期 $700-1300/月**

### 第 6 个月(5K 粉丝 + 流量稳)
- 周精选 1-2 个 × $200 = $200-400
- 置顶 8-10 / 周 × $50 = $400-500/周
- 票务分成:$300-800/月
- **预期 $2-4K/月**

### 第 12 个月
- IG 10K+ 粉丝 → CPM $5-15
- 估算 $5-10K/月

---

## 核心差异化(为什么会有人关注)

1. **三州一岛全覆盖** — 大部分本地号只覆盖纽约市,我们 cover NJ/CT/LI(很多新泽西/长岛人通勤)
2. **每天 3 条不重复** — 大部分号一周更几条
3. **平台同步** — 滑哪个都是同一份精选
4. **中英双语** — 华人圈可能是缺口

---

## 相对 HI(本品牌)的差异

| 维度 | HI (food) | HI Things (events) |
|---|---|---|
| 频率 | 5/天 | 3/天 |
| 平台 | YT + IG + TikTok | YT + IG + TikTok |
| 内容来源 | Google + 官网照 | Eventbrite + 官方 + 票务 |
| 监码 | 真餐厅照片 | 官方活动宣传图 |
| 转化目标 | YT 订阅 + IG 粉丝 | IG 粉丝 + 联盟点击 |
| 商业化 | 餐厅自费(代运营) | 活动方置顶 + 票务分成 |

---

## 风险点

- **版权**:用 Eventbrite/官方宣传图大概率没问题(promotional use 默认),但要写 disclaimer
- **同质化**:Time Out / DoNYC / Secret NYC 已经存在。我们的差异是:**频率高 + 多州 + 双语**
- **冷启动**:0 粉丝起步,前 3 个月只能依赖算法 + IG 找 niche tag
- **工作量**:event scraping 需要每天稳定运行 — research-worker 框架已有,改一改即可
