# 北京浮生记 — 场景与对话主循环

init python:
    import random
    import fushengji_sim

    EVENT_CATALOG = fushengji_sim.load_events()

    def fs_play_sfx(name):
        path = "audio/" + name
        if renpy.loadable(path):
            renpy.sound.play(path)


define me = Character("俺", color="#f4ead4")
define news = Character("北京晚报", color="#d4a017")
define chief = Character("村长", color="#e07040")
define doctor = Character("大夫", color="#c8d8d0")
define nurse = Character("小护士", color="#e8a0b0")
define wife = Character("村长老婆", color="#c07070")
define agent = Character("中介", color="#c0a060")
define netbar = Character("网管", color="#80a0c0")
define xiebufeng = Character("谢不疯", color="#e090b0")
define teller = Character("柜员", color="#90c090")
define stallkeep = Character("摊主", color="#d0b080")

default gs = None
default pending_events = []
default loc_name = "北京站"


label start:
    python:
        gs = fushengji_sim.reset(random.Random())
        pending_events = []
        loc_name = fushengji_sim.LOC_BY_ID[gs["location"]]["name"]
    call intro from _call_intro
    show screen hud
    jump location_menu


label intro:
    scene bg market_station
    with fade
    show hero normal at fs_left
    with dissolve
    me "一九九八年。俺从村里来北京，口袋里两千块，肩上压着村长的五千块债。"
    me "利息一天一分。四十天内还不完，老乡就会来北京找俺。"
    show npc chief at fs_right
    with dissolve
    chief "铁牛，听清楚。五千块，四十天。别在城里花天酒地。"
    hide npc
    with dissolve
    me "房子只能塞一百件货。倒什么、去哪儿，都写在这一页北京里。"
    return


label location_menu:
    if gs is None:
        $ gs = fushengji_sim.reset(random.Random())
    if gs.get("dead") or gs.get("game_over"):
        jump ending

    $ loc_name = fushengji_sim.LOC_BY_ID[gs["location"]]["name"]
    scene expression fs_bg_name()
    show hero normal at fs_left
    window auto

    menu:
        "人在[loc_name]，风沙还没停。俺要——"

        "去货摊看看今天卖什么。":
            jump stall_scene

        "换个黑市，过一天。":
            jump travel_scene

        "去银行。":
            jump bank_scene

        "去医院。":
            jump hospital_scene

        "去邮局给村长汇钱。":
            jump post_scene

        "钻进网吧。":
            jump wangba_scene

        "找租房中介。":
            jump house_scene

        "翻翻口袋和日记。":
            jump diary_scene


label stall_scene:
    scene expression fs_bg_name()
    show hero normal at fs_left
    me "摊主把报纸盖在货上，只露出一个角。价码一天一个样。"
    call screen stall_board
    $ act = _return
    if act == "leave" or not act:
        jump location_menu
    $ kind, gid = act
    $ gname = fushengji_sim.GOODS_BY_ID[gid]["name"]
    $ price = gs["prices"][gid]
    $ have = gs["inventory"][gid]
    show expression GOOD_IMAGE[gid] as stallgood at truecenter:
        zoom 0.28
        yoffset -80
    if kind == "look":
        if price > 0 and have > 0:
            stallkeep "[gname]，今天 [price] 元一件。你口袋里还有 [have] 件。"
            menu:
                "买一点。" if fushengji_sim.max_buy(gs, gid) > 0:
                    jump stall_buy
                "出手。" if have > 0:
                    jump stall_sell
                "再看看。":
                    hide stallgood
                    jump stall_scene
        elif price > 0:
            stallkeep "[gname]，[price] 元。要不要？"
            menu:
                "还价，买。" if fushengji_sim.max_buy(gs, gid) > 0:
                    jump stall_buy
                "兜里空，走了。":
                    hide stallgood
                    jump stall_scene
        else:
            stallkeep "这地方今儿没人收 [gname]。"
            if have > 0:
                me "口袋里还压着 [have] 件，只能等到有市再抛。"
            hide stallgood
            jump stall_scene
    jump location_menu


label stall_buy:
    $ mx = fushengji_sim.max_buy(gs, gid)
    if mx <= 0:
        me "钱不够，或者屋子满了。"
        hide stallgood
        jump stall_scene
    call screen qty_pick("买多少件" + gname + "？每件 %d 元。" % price, mx)
    $ n = _return
    if n:
        $ pending_events = fushengji_sim.buy(gs, gid, n)
        $ fs_play_sfx("buy.wav")
        stallkeep "成交。拿走吧。"
        call play_events from _call_play_events
    hide stallgood
    jump stall_scene


label stall_sell:
    $ have = gs["inventory"][gid]
    if have <= 0 or price <= 0:
        hide stallgood
        jump stall_scene
    call screen qty_pick("抛出多少件" + gname + "？", have)
    $ n = _return
    if n:
        $ pending_events = fushengji_sim.sell(gs, gid, n)
        $ fs_play_sfx("money.wav")
        stallkeep "货我收下了。"
        call play_events from _call_play_events_1
    hide stallgood
    jump stall_scene


label travel_scene:
    scene bg map_beijing
    with fade
    me "北京城那么大。下一站去哪儿？"
    call screen map_select
    $ dest = _return
    if not dest or dest == "cancel":
        jump location_menu
    $ dest_name = fushengji_sim.LOC_BY_ID[dest]["name"]
    $ fs_play_sfx("shutdoor.wav")
    scene black
    with fade
    me "俺挤上地铁，去[dest_name]。一天又过去了。"
    $ pending_events = fushengji_sim.move_to(gs, dest, random.Random(), EVENT_CATALOG)
    $ loc_name = fushengji_sim.LOC_BY_ID[gs["location"]]["name"]
    scene expression fs_bg_name()
    with fade
    show hero normal at fs_left
    call play_events from _call_play_events_2
    jump location_menu


label bank_scene:
    scene bg bank
    with fade
    $ fs_play_sfx("opendoor.wav")
    show npc teller at fs_right
    $ cash = gs["cash"]
    $ bank = gs["bank"]
    teller "客户您好。现金 [cash] 元，存款 [bank] 元。请问您要……"
    menu:
        "把钱存进去。" if gs["cash"] > 0:
            call screen qty_pick("存多少？", gs["cash"])
            $ n = _return
            if n:
                $ fushengji_sim.deposit(gs, n)
                teller "已经入账。您慢走。"
        "把钱取出来。" if gs["bank"] > 0:
            call screen qty_pick("取多少？", gs["bank"])
            $ n = _return
            if n:
                $ fushengji_sim.withdraw(gs, n)
                teller "给您。点清楚。"
        "走错了。":
            teller "下一个。"
    hide npc
    jump location_menu


label hospital_scene:
    scene bg hospital
    with fade
    $ fs_play_sfx("opendoor.wav")
    $ need = 100 - gs["health"]
    $ hp = gs["health"]
    if need <= 0:
        show npc nurse at fs_right
        $ pending_events = fushengji_sim.heal(gs, 0)
        call play_events from _call_play_events_3
        hide npc
        jump location_menu
    show npc doctor at fs_right
    doctor "您的健康是 [hp] 点，还差 [need] 点。一点三千五。"
    menu:
        "治。" if gs["cash"] >= 3500:
            call screen qty_pick("治几点？每点三千五。", need)
            $ pts = _return
            if pts:
                $ pending_events = fushengji_sim.heal(gs, pts)
                call play_events from _call_play_events_4
        "没钱，走。":
            doctor "下次早点来。"
    hide npc
    jump location_menu


label post_scene:
    scene bg post
    with fade
    $ fs_play_sfx("opendoor.wav")
    show npc chief at fs_right
    if gs["debt"] <= 0:
        $ line = fushengji_sim.post_no_debt_line(gs)
        chief "[line]"
        hide npc
        jump location_menu
    $ d = gs["debt"]
    chief "铁牛，你欠俺 [d] 元，快还！"
    menu:
        "汇出去。" if gs["cash"] > 0:
            call screen qty_pick("汇多少给村长？", min(gs["cash"], gs["debt"]))
            $ amt = _return
            if amt:
                $ pending_events = fushengji_sim.repay_debt(gs, amt)
                call play_events from _call_play_events_5
        "挂了。":
            chief "利息可没睡着。"
    hide npc
    jump location_menu


label wangba_scene:
    scene bg wangba
    with fade
    $ fs_play_sfx("opendoor.wav")
    show npc netbar at fs_right
    $ pending_events = fushengji_sim.visit_wangba(gs, random.Random())
    call play_events from _call_play_events_6
    hide npc
    jump location_menu


label house_scene:
    scene bg house
    with fade
    $ fs_play_sfx("opendoor.wav")
    show npc agent at fs_right
    $ pending_events = fushengji_sim.rent_house(gs)
    call play_events from _call_play_events_7
    hide npc
    jump location_menu


label diary_scene:
    call screen diary
    jump location_menu


label play_events:
    window show
    python:
        evs = list(pending_events or [])
        pending_events = []
    while evs:
        $ ev = evs.pop(0)
        $ ev_text = ev.get("text", "")
        $ who = ev.get("speaker", "news")
        $ sfx = ev.get("sfx")
        if sfx:
            $ fs_play_sfx(sfx)
        hide npc
        if who == "me":
            show hero normal at fs_left
            me "[ev_text]"
        elif who == "chief":
            show npc chief at fs_right
            chief "[ev_text]"
        elif who == "doctor":
            show npc doctor at fs_right
            doctor "[ev_text]"
        elif who == "nurse":
            show npc nurse at fs_right
            nurse "[ev_text]"
        elif who == "wife":
            show npc chief at fs_right
            wife "[ev_text]"
        elif who == "agent":
            show npc agent at fs_right
            agent "[ev_text]"
        elif who == "netbar":
            show npc netbar at fs_right
            netbar "[ev_text]"
        elif who == "xiebufeng":
            show npc xiebufeng at fs_right
            xiebufeng "[ev_text]"
        elif who == "teller":
            show npc teller at fs_right
            teller "[ev_text]"
        else:
            news "[ev_text]"
    hide npc
    show hero normal at fs_left
    window hide
    return


label ending:
    hide screen hud
    python:
        kind, title, sc = fushengji_sim.ending_rank(gs)
    if kind == "death":
        scene bg ending_death
        with fade
        $ fs_play_sfx("death.wav")
        me "俺倒在街头。日记本最后一页写着：北京，我将再来。"
    else:
        scene bg ending_home
        with fade
        show hero normal at fs_left
        $ hp = gs["health"]
        $ fm = gs["fame"]
        me "四十天到了。现金加存款减去负债，还剩 [sc] 元。"
        me "这就是俺在北京的分数。[title]"
        me "健康 [hp]，名声 [fm]。该回家了。"
    "《北京浮生记》。原作郭祥昊，GPL-2.0。"
    return
