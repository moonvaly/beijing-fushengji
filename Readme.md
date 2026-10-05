# 北京浮生记（Ren'Py）

把郭祥昊 2000 年 Win32 经营游戏《北京浮生记》迁到 Ren'Py 8.5：像素风黑市、四十天还债、随机事件用对话演出。

原作 GPL-2.0。本移植同样 GPL-2.0。

## 下载

正式包在 GitHub Releases（Windows / macOS）：

https://github.com/moonvaly/beijing-fushengji/releases

Windows 解压后运行 `beijing_fushengji.exe`。macOS 未公证，第一次请右键 → 打开。

源码即本仓库，满足 GPL-2.0 的对应源码义务。打包步骤见 `docs/RELEASE.md`。

## 网页版

第二轮重构在 `web/`（Vite + TypeScript），浏览器可玩：

```bash
cd web && npm install && npm run dev
```

正式页：https://moonvaly.github.io/beijing-fushengji/

## 运行

需要本机 [Ren'Py 8.5.0 SDK](https://www.renpy.org/latest.html)，默认路径：

`/Users/bruce/Documents/renpy-8.5.0-sdk`

```bash
/Users/bruce/Documents/renpy-8.5.0-sdk/renpy.sh beijing_fushengji
```

也可把 `beijing_fushengji` 加进 Launcher 的 Projects Directory。

## 玩法

外地青年进京，2000 元现金，欠村长 5000，房子容量 100，共 40 天。在地铁口黑市买卖八种货物，去银行、医院、邮局、网吧、房产中介。每次换地点过一天，债务每天 10% 利息。

## 工程

| 路径 | 作用 |
|---|---|
| `beijing_fushengji/game/` | Ren'Py 游戏 |
| `beijing_fushengji/game/fushengji_sim.py` | 模拟引擎（无 Ren'Py 依赖） |
| `beijing_fushengji/game/engine/events.json` | 数据驱动事件 |
| `tools/test_sim.py` | 模拟单测 |
| `tools/gen_assets.py` | 即梦画布 `dreamina-canvas` 生图 |
| `docs/DESIGN.md` | 设计说明 |

```bash
python3 tools/test_sim.py
```

## 资产

画面用即梦画布 CLI `dreamina-canvas`（旧版 `dreamina` 已退役）按 `tools/assets/manifest.yaml` 生成。未生成前游戏用纯色占位。音效用原作 `sound/*.wav`（GPL）。

```bash
dreamina-canvas auth status --format json
python3 tools/gen_assets.py --dry-run --only hero_normal bg_market_station
python3 tools/gen_assets.py --only hero_normal bg_market_station --credit-ceiling 200
```

`--credit-ceiling` 是积分上限；不传则停在报价、不扣费。画布状态写在 `tools/assets/job_state.json`。

## 来源

- 原作：`/Users/bruce/Documents/projects/beijing_fushengji`（郭祥昊）
- GPT 版语料：`/Users/bruce/Documents/projects/beijing-fushengji-gpt`
