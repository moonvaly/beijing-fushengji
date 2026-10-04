# 发行 1.0

目标：Windows + macOS 桌面包，GitHub Release 分发。仓库公开以满足 GPL-2.0。

## 打包

```bash
cd /Users/bruce/Documents/grok_projects/game_maker

/Users/bruce/Documents/renpy-8.5.0-sdk/renpy.sh beijing_fushengji add_from
python3 tools/test_sim.py
/Users/bruce/Documents/renpy-8.5.0-sdk/renpy.sh beijing_fushengji test smoke_intro_to_market

/Users/bruce/Documents/renpy-8.5.0-sdk/renpy.sh launcher distribute \
  beijing_fushengji \
  --destination dist \
  --package pc --package mac --no-update
```

产物：

- `dist/beijing_fushengji-1.0.0-pc.zip`
- `dist/beijing_fushengji-1.0.0-mac.zip`

## GitHub Release

```bash
git tag v1.0.0
git push origin main v1.0.0

gh release create v1.0.0 \
  dist/beijing_fushengji-1.0.0-pc.zip \
  dist/beijing_fushengji-1.0.0-mac.zip \
  --title "北京浮生记 1.0.0" \
  --notes-file docs/release-notes.md
```

## 玩家怎么开

Windows：解压 zip，运行 `beijing_fushengji.exe`。

macOS：解压后得到 `.app`。未公证，第一次请 **右键 → 打开**，在提示里选打开。不要从隔离的下载属性里直接双击。

## 许可

GPL-2.0。原作郭祥昊。源码与二进制一并公开。
