################################################################################
## 场景叠加：日记条、货摊、地图、数量、口袋
################################################################################

style fs_text:
    font "SourceHanSansLite.ttf"
    color "#f4ead4"
    size 18

style fs_label is fs_text:
    size 20
    color "#d4a017"

style fs_small is fs_text:
    size 16
    color "#c8bca8"

style fs_card_btn:
    background "#1a1612dd"
    hover_background "#5a4020ee"
    padding (8, 8)
    xsize 210
    ysize 250

style fs_card_btn_text is fs_text:
    size 16
    text_align 0.5
    xalign 0.5

style fs_chip:
    background "#2a2418cc"
    hover_background "#6a5020cc"
    padding (12, 7)

style fs_chip_text is fs_text:
    size 18
    hover_color "#ffe08a"


screen hud():
    zorder 80
    if gs:
        frame:
            background "#120e0acc"
            xalign 0.5
            ypos 10
            padding (18, 7)
            hbox:
                spacing 20
                text "第 %d 天 / 40" % (gs.get("day_index", 0) + 1) style "fs_label"
                text fushengji_sim.LOC_BY_ID[gs["location"]]["name"] style "fs_text" color "#ffe08a"
                text "现金 %d" % gs["cash"] style "fs_text"
                text "债 %d" % gs["debt"] style "fs_text" color "#e07070"
                text "健康 %d" % gs["health"] style "fs_text" color "#8dcc6a"
                text "名声 %d" % gs["fame"] style "fs_text"


screen stall_board():
    modal True
    frame:
        background "#00000000"
        xalign 0.5
        yalign 0.62
        xsize 1180
        padding (8, 8)
        vbox:
            spacing 10
            text "摊上今天有这些。点一件，跟摊主谈。" style "fs_label" xalign 0.5
            hbox:
                spacing 12
                xalign 0.5
                for g in fushengji_sim.GOODS:
                    $ gid = g["id"]
                    $ price = gs["prices"][gid]
                    $ have = gs["inventory"][gid]
                    if price > 0 or have > 0:
                        button:
                            style "fs_card_btn"
                            action Return(("look", gid))
                            vbox:
                                spacing 6
                                xalign 0.5
                                add GOOD_IMAGE[gid]:
                                    xysize (160, 140)
                                    fit "cover"
                                text g["name"] style "fs_small" xalign 0.5
                                if price > 0:
                                    text "%d 元" % price style "fs_text" color "#ffe08a" xalign 0.5
                                else:
                                    text "今日无市" style "fs_small" xalign 0.5
                                if have:
                                    text "口袋里 %d 件" % have style "fs_small" color "#9ccc8a" xalign 0.5
            textbutton "离开货摊" style "fs_chip" text_style "fs_chip_text" action Return("leave") xalign 0.5


screen map_select():
    modal True
    add "bg map_beijing"
    add "#00000055"

    frame:
        background "#120e0add"
        xalign 0.5
        yalign 0.06
        padding (16, 8)
        hbox:
            spacing 24
            text "下一站去哪儿？出城就算过一天。" style "fs_label"
            textbutton "还是留下" style "fs_chip" text_style "fs_chip_text" action Return("cancel")

    frame:
        background "#120e0acc"
        xalign 0.5
        yalign 0.98
        xsize 1240
        padding (14, 10)
        vbox:
            spacing 8
            for title, ids in MAP_GROUPS:
                hbox:
                    spacing 8
                    text title style "fs_small" yalign 0.5 xsize 64
                    for lid in ids:
                        $ loc = fushengji_sim.LOC_BY_ID[lid]
                        $ here = lid == gs["location"]
                        textbutton loc["name"]:
                            style "fs_chip"
                            text_style "fs_chip_text"
                            sensitive not here
                            action Return(lid)


screen qty_pick(prompt, maxn):
    modal True
    default n = maxn
    add "#00000099"
    frame:
        background "#1a1612ee"
        xalign 0.5
        yalign 0.5
        xsize 560
        padding (28, 24)
        vbox:
            spacing 14
            text prompt style "fs_label"
            hbox:
                spacing 16
                textbutton "−" action SetScreenVariable("n", max(0, n - 1))
                text "[n] / [maxn]" style "fs_text" yalign 0.5
                textbutton "+" action SetScreenVariable("n", min(maxn, n + 1))
                textbutton "全部" action SetScreenVariable("n", maxn)
            hbox:
                spacing 20
                textbutton "就这些" action Return(n)
                textbutton "算了" action Return(0)


screen diary():
    modal True
    add "#00000088"
    frame:
        background "#1a1612ee"
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 560
        padding (28, 24)
        vbox:
            spacing 10
            text "铁牛的日记" style "fs_label"
            text "人在 %s。还剩 %d 天。" % (fushengji_sim.LOC_BY_ID[gs["location"]]["name"], gs["days_left"]) style "fs_text"
            text "现金 %d　存款 %d　负债 %d" % (gs["cash"], gs["bank"], gs["debt"]) style "fs_text"
            text "健康 %d　名声 %d　屋子 %d/%d" % (gs["health"], gs["fame"], gs["total_goods"], gs["capacity"]) style "fs_text"
            null height 8
            text "口袋里的货" style "fs_label"
            $ held = [g for g in fushengji_sim.GOODS if gs["inventory"][g["id"]] > 0]
            if not held:
                text "空空如也。" style "fs_small"
            for g in held:
                $ gid = g["id"]
                hbox:
                    spacing 12
                    add GOOD_IMAGE[gid]:
                        xysize (64, 64)
                        fit "cover"
                    text "%s  ×%d" % (g["name"], gs["inventory"][gid]) style "fs_text" yalign 0.5
            null height 12
            textbutton "合上日记" style "fs_chip" text_style "fs_chip_text" action Return(True)
