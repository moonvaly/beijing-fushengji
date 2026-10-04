# 《北京浮生记》Ren'Py 设计落地

## 源

- 模拟真相：`/Users/bruce/Documents/projects/beijing_fushengji`（郭祥昊，GPL-2.0）
- 文案语料：`/Users/bruce/Documents/projects/beijing-fushengji-gpt`
- 运行：Ren'Py 8.5.0，`beijing_fushengji/`

## 一天流程

换地点 → 刷新市价（缺 3 种；最后两天全开）→ 债务 ×1.10、存款 ×1.01 → 地点旁白 → 故事节拍 → 商业事件（950 模）→ 健康事件（1000 模，第一条）→ 强制住院 / 死亡 → 劫财 → 黑客（可选）→ 高利贷报复 → 天数 −1。

## 文件

- `game/fushengji_sim.py` 纯 Python 模拟
- `game/engine/events.json` 事件目录
- `game/script.rpy` 开场、日循环、结局
- `game/screens_play.rpy` 黑市 / 地图 / 设施
- `tools/test_sim.py` 单测
- `tools/gen_assets.py` 即梦画布 `dreamina-canvas` 批量生图

启动：

```bash
python3 tools/test_sim.py
/Users/bruce/Documents/renpy-8.5.0-sdk/renpy.sh beijing_fushengji
```

生图走 `dreamina-canvas`（旧 `dreamina text2image` 已退役）。先 `auth status`，用 `--credit-ceiling` 批准积分后再跑：

```bash
dreamina-canvas auth status --format json
python3 tools/gen_assets.py --dry-run --only hero_normal bg_market_station
python3 tools/gen_assets.py --only hero_normal bg_market_station --credit-ceiling 200
```

默认模型 `seedream_5.0_lite`、分辨率 `2K`，以 `dreamina-canvas model list --type image` 为准。每张图一个画布节点，产物下载到 `beijing_fushengji/game/images/`。
