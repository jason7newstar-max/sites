# HI Beats — 短视频音乐库策略

## 决策:两条路

### 路 A · 投稿 Artlist / Epidemic (低投入,被动)

**优点**
- 不用自建站、不管支付、不管获客
- Artlist 投稿审核通过后 → 每次被使用拿分成
- 适合先验证音乐是否被市场接受

**缺点**
- 分成比例 30-50%(平台拿大头)
- 审核严格,Suno 生成的"AI 痕迹"可能被拒
- 单条收入低($0.05-2 / 使用),需要海量曲子才有收入

**收入预期(乐观)**
- 100 首 × 月均 5 次使用 × $1.50 = $750/月,要 6-12 个月堆库
- 12 个月稳态:$2-5K/月

### 路 B · 自建订阅站 (高投入,主动)

**优点**
- 100% 收入留下
- 完全控制定价、分类、品牌
- 客户一旦订阅,边际成本接近 0(月费 × N 用户)

**缺点**
- 需要自己获客(SEO + 红人合作 + 付费投放)
- 需要支付集成、用户系统、CDN
- 上线 1-3 个月才看到第一个付费用户

**收入预期(乐观)**
- 100 用户 × $15/月 = $1500/月
- 6 个月稳态:$3-8K/月
- 上限远高于路 A,但启动慢

---

## 推荐:**路 A + 路 B 同时跑**

- 路 A 现在投稿(2 周内开通 Artlist + Epidemic 账号),6-12 个月堆库被动收入
- 路 B 同时自建 hibeats.vercel.app,先做免费版聚人 → 3 个月后转付费
- 同一批 Suno 生成的曲子,两边复用

---

## Action Plan(第一个月)

### Week 1
- [ ] 用 Suno Pro **生成 30 首** starter 曲(下面 30 个 prompt 已写好)
- [ ] **混音 + 标签** 每首(BPM/mood/use-case/duration)
- [ ] 申请 Artlist 投稿 + Epidemic Sound 投稿账号

### Week 2
- [ ] **首批投稿** Artlist 30 首
- [ ] 上线 hibeats.vercel.app(免费试听 + Email 注册收集)
- [ ] 在 IG/TT 发 5 条「短视频找不到合适的音乐?」教程引流

### Week 3-4
- [ ] **再生成 30 首**(共 60)
- [ ] 接 Stripe + 上线付费版($9.99 / 月,无限下载)
- [ ] 第一批红人合作:发免费下载邀请码 → 让他们用在视频里
- [ ] 监控 Artlist 第一首通过审核情况

---

## 30 个 Suno Prompts(按短视频常用 mood 分)

> 每首 60-90 秒,带清晰 hook,可被剪 6-15-30 秒 cut。

### 🔥 Energy / Hype-up (10)

**1. Subway Burst**
```
[Style: hip-hop trap, 95 BPM, 808 sub-bass, hi-hats rapid, brass stab, NYC subway energy]
30-sec instrumental hook, no vocals. Build into drop at :15.
```

**2. Glow Up**
```
[Style: indie-pop electronic, 120 BPM, female ad-lib vocals, synth pluck, bright snare claps, transformation vibe]
60-sec, intro / verse / drop / outro structure.
```

**3. Block by Block**
```
[Style: boom-bap hip-hop, 90 BPM, jazzy piano sample, vinyl crackle, head-nod groove, no vocals]
60-sec instrumental.
```

**4. First Day Energy**
```
[Style: synthwave, 110 BPM, retro arpeggiated synth, gated reverb drums, optimistic, no vocals]
60-sec full arc.
```

**5. Run It Back**
```
[Style: drum-and-bass, 174 BPM, fast breakbeat, sub-bass wobble, energetic instrumental, no vocals]
30-sec impact piece.
```

**6. Big City Tonight**
```
[Style: electro-pop, 124 BPM, female vocal "ah-ah" hook, 4-on-floor kick, glittery synths, NYC nightlife]
60-sec, hook-forward.
```

**7. Win Streak**
```
[Style: orchestral hip-hop, 100 BPM, epic strings + 808s, motivational drop, no vocals]
60-sec sports/win montage.
```

**8. Pull Up**
```
[Style: trap, 140 BPM (half-time feel), bouncy 808s, pitched-up vocal chops, swag energy]
30-sec instrumental loop.
```

**9. Bright Lights**
```
[Style: pop-rock, 130 BPM, driving guitar riff, anthemic chorus la-la-la, no lyrics, festival vibe]
60-sec.
```

**10. Stack the Wins**
```
[Style: tech-house, 124 BPM, four-on-floor, stab synths, building tension + release, no vocals]
60-sec build/drop.
```

### 🌙 Chill / Lo-fi / Background (10)

**11. After Hours Coffee**
```
[Style: lo-fi hip-hop, 75 BPM, jazzy piano + sax loop, rainy night, vinyl warmth, no vocals]
60-sec ambient.
```

**12. Sunday Slow**
```
[Style: jazzy chill-hop, 80 BPM, mellow Rhodes electric piano, brushed drums, no vocals]
60-sec.
```

**13. Brunch Plate**
```
[Style: bossa nova lite, 90 BPM, classical guitar + soft shaker, warm major key, no vocals]
60-sec.
```

**14. Window Seat**
```
[Style: ambient piano, 60 BPM, sparse minor 7th chords, cinematic pads, contemplative, no vocals]
90-sec slow build.
```

**15. Park Bench Vibe**
```
[Style: indie-folk lo-fi, 85 BPM, fingerpicked acoustic guitar + hum vocals (no words), warm tape feel]
60-sec.
```

**16. Cozy Hour**
```
[Style: lo-fi jazz, 70 BPM, soft saxophone melody, brushed snare, vintage compression, no vocals]
60-sec.
```

**17. Slow Night**
```
[Style: trip-hop ambient, 70 BPM, dreamy female "oo" vocal pad, downtempo beat, no real lyrics]
90-sec.
```

**18. Light Snow**
```
[Style: ambient pop, 80 BPM, music box-like piano + chimes, soft pad, peaceful, no vocals]
60-sec.
```

**19. Nine to Five Done**
```
[Style: chill house, 90 BPM, soft kick + filtered piano stab, deep bass, evening unwind, no vocals]
60-sec.
```

**20. Empty Subway**
```
[Style: dark ambient, 75 BPM, sparse synth drone + minimal percussion, late-night NYC, no vocals]
90-sec atmospheric.
```

### 🎬 Cinematic / Reveal / Drop (5)

**21. Big Reveal**
```
[Style: epic cinematic orchestral, 90 BPM, tension build with strings, drum hits at climax, no vocals]
30-sec impact piece for "before/after" reveals.
```

**22. Plot Twist**
```
[Style: hybrid trailer, 100 BPM, riser → drum hit → bass drop, dramatic, no vocals]
30-sec for storytelling pivots.
```

**23. Slow Mo Moment**
```
[Style: cinematic piano, 70 BPM, swelling strings, builds to release, emotional, no vocals]
60-sec.
```

**24. Night Run**
```
[Style: synth-cinematic, 110 BPM, pulsing bass + arpeggios, neon mood, building, no vocals]
60-sec for action montages.
```

**25. The Drop In**
```
[Style: trailer hybrid, 120 BPM, riser + impact drop at :08 and :15, percussion-heavy, no vocals]
30-sec.
```

### 🎉 Comedy / Quirky / Bouncy (5)

**26. Goofy Walk**
```
[Style: ukulele pop, 120 BPM, whistling melody + finger snaps + bouncy bass, playful, no vocals]
60-sec.
```

**27. Awkward Moment**
```
[Style: indie-pop quirky, 100 BPM, plucked strings + glockenspiel, slightly off-kilter, no vocals]
30-sec.
```

**28. Scheme Time**
```
[Style: jazzy comedy, 110 BPM, walking bass + clarinet, cartoonish, no vocals]
30-sec.
```

**29. Mic Drop**
```
[Style: funk swagger, 95 BPM, slap bass + horn stabs, confident, no vocals]
30-sec.
```

**30. Beep Boop Robot**
```
[Style: 8-bit chiptune, 130 BPM, square wave melody + arpeggios, video game vibe, no vocals]
30-sec.
```

---

## 标签维度(每首入库时填)

```yaml
title: "Subway Burst"
file: subway-burst-001.mp3
duration_sec: 30
bpm: 95
key: A minor
mood: [energy, urban, hype]
genre: [hip-hop, trap]
use_case: [montage, transition, hook]
has_vocal: false
vocal_type: null  # or [male, female, ad-lib, hum]
loopable: true
created_at: 2026-05-07
suno_url: https://suno.com/song/...
license_tier: [free, paid_personal, paid_commercial]
```

---

## 落地页设计要点(已建)

- 试听器:30 首样品播放器
- Filter:按 mood / bpm / duration 筛
- Free preview · 付费下载 watermark-free
- 价格:$9.99/月(基础 50 首) · $19.99/月(全库 + 商用) · $49 一次性买单首

---

## 关键风险

- **Suno 商业许可**:Pro 才商用。投稿 Artlist 必须确认上传的歌全用 Pro 生成
- **AI 检测**:Artlist 据传更新了 AI 检测,Suno 痕迹大的歌会被拒。混音环节关键 — 不能直接发 raw Suno
- **同质化**:Suno 出来的曲子彼此可能太像。30 首要尽量风格分散,不要全是 trap
