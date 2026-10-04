# -*- coding: utf-8 -*-
"""Beijing Fushengji simulation — original C++ rules, no Ren'Py dependency."""

from __future__ import annotations

import json
import random
from copy import deepcopy
from pathlib import Path

TOTAL_DAYS = 40
START_CASH = 2000
START_DEBT = 5000
START_BANK = 0
START_HEALTH = 100
START_FAME = 100
START_CAPACITY = 100
MAX_CAPACITY = 140
HOUSE_STEP = 10
HOUSE_MIN_CASH = 30000
HOSPITAL_COST_PER_POINT = 3500
WANGBA_MAX_VISITS = 3
WANGBA_MIN_CASH = 15
DEBT_PUNISH_THRESHOLD = 100000
DEBT_PUNISH_HEALTH = 30
INTEREST_DEBT = 0.10
INTEREST_BANK = 0.01
LEAVEOUT_NORMAL = 3
PHONE_EVENT_DEBT = 2500

GOODS = [
    {"id": "CIGARETTE", "name": "进口香烟", "base": 100, "span": 350, "fame_hit": 0},
    {"id": "CAR", "name": "走私汽车", "base": 15000, "span": 15000, "fame_hit": 0},
    {"id": "CD", "name": "盗版 VCD / 游戏", "base": 5, "span": 50, "fame_hit": 0},
    {"id": "ALCOHOL", "name": "假白酒（剧毒）", "base": 1000, "span": 2500, "fame_hit": 10},
    {"id": "BABY", "name": "《上海小宝贝》盗版刊物", "base": 5000, "span": 9000, "fame_hit": 7},
    {"id": "TOY", "name": "进口玩具", "base": 250, "span": 600, "fame_hit": 0},
    {"id": "PHONES", "name": "水货手机", "base": 750, "span": 750, "fame_hit": 0},
    {"id": "COSMETIC", "name": "伪劣化妆品", "base": 65, "span": 180, "fame_hit": 0},
]

GOODS_BY_ID = {g["id"]: g for g in GOODS}
GOODS_ORDER = [g["id"] for g in GOODS]

LOCATIONS = [
    {"id": "jianguomen", "name": "建国门", "bg": "market_east"},
    {"id": "beijingzhan", "name": "北京站", "bg": "market_station"},
    {"id": "xizhimen", "name": "西直门", "bg": "market_north"},
    {"id": "chongwenmen", "name": "崇文门", "bg": "market_inner"},
    {"id": "dongzhimen", "name": "东直门", "bg": "market_northeast"},
    {"id": "fuxingmen", "name": "复兴门", "bg": "market_center"},
    {"id": "jishuitan", "name": "积水潭", "bg": "market_north"},
    {"id": "changchunjie", "name": "长椿街", "bg": "market_inner"},
    {"id": "gongzhufen", "name": "公主坟", "bg": "market_west"},
    {"id": "pingguoyuan", "name": "苹果园", "bg": "market_west"},
    {"id": "yonganli", "name": "永安里", "bg": "market_east"},
    {"id": "fangzhuang", "name": "方庄", "bg": "market_south"},
    {"id": "haidian", "name": "海淀大街", "bg": "market_haidian"},
    {"id": "yongdingmen", "name": "永定门", "bg": "market_south"},
    {"id": "sanyuan", "name": "三元东桥", "bg": "market_ring"},
    {"id": "wenjin", "name": "文津街", "bg": "market_haidian"},
    {"id": "beichen", "name": "北辰西路", "bg": "market_ring"},
    {"id": "caihuying", "name": "菜户营", "bg": "market_south"},
    {"id": "cuiwei", "name": "翠微路", "bg": "market_west"},
    {"id": "bajiao", "name": "八角地铁", "bg": "market_west"},
]

LOC_BY_ID = {loc["id"]: loc for loc in LOCATIONS}

LOCATION_FLAVOR = {
    "jianguomen": "建国门立交桥底下，倒爷们把货物码成一堵墙。",
    "beijingzhan": "北京站出站口人潮把俺挤得转不过身，黑市就藏在过街地道里。",
    "xizhimen": "西直门城墙根儿，风沙里飘着烤地瓜和盗版碟的味道。",
    "chongwenmen": "崇文门新世界旁边，红袖章老太太正盯着外地人。",
    "dongzhimen": "东直门长途汽车站，东北口音和假烟箱子挤在一块。",
    "fuxingmen": "复兴门金融街还没起来，地下通道里全是卖水货的。",
    "jishuitan": "积水潭医院门口，有人低声问俺要不要进口药。",
    "changchunjie": "长椿街夜市收摊，剩货都往俺怀里塞。",
    "gongzhufen": "公主坟城乡结合部，军大衣和走私车广告贴满电线杆。",
    "pingguoyuan": "苹果园是西边尽头，黑市跟煤矿似的，黑、乱、便宜。",
    "yonganli": "永安里的写字楼玻璃反光，楼下地摊一样敢卖汽车钥匙。",
    "fangzhuang": "方庄小区自行车棚后头，民工和大学生抢同一箱VCD。",
    "haidian": "海淀大街中关村，村姑一字排开全是盗版碟。",
    "yongdingmen": "永定门城楼还在，城根下的货比城楼还杂。",
    "sanyuan": "三元东桥堵车堵到天黑，俺在车缝里把货倒了出去。",
    "wenjin": "文津街靠近中南海，巡逻多，买卖都得快。",
    "beichen": "北辰西路亚运村边，有钱人路过也敢问水货手机。",
    "caihuying": "菜户营货场尘土大，箱子一开全是广东来的私货。",
    "cuiwei": "翠微路商场对面，假化妆品包装比真的还亮。",
    "bajiao": "八角地铁口风大，俺把货压在砖头底下等买主。",
}

HOSPITAL_SPOTS = [
    "发廊里", "早点摊上", "报摊上", "烤羊肉摊上", "公共汽车里",
    "人力车上", "电话亭里", "出租车里", "小巴里", "美容院里",
    "小商亭里", "小商场门口", "民工脚下", "无照游商摊里", "草地上",
    "小饭馆里", "马路边", "人行道上", "街心公园里", "广告牌下",
    "公共汽车站里", "长途汽车站里", "卖盗版游戏的旁边",
]


def _events_path():
    here = Path(__file__).resolve().parent
    return here / "engine" / "events.json"


def load_events(path=None):
    p = Path(path) if path else _events_path()
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def new_state():
    return {
        "location": "beijingzhan",
        "cash": START_CASH,
        "debt": START_DEBT,
        "bank": START_BANK,
        "health": START_HEALTH,
        "fame": START_FAME,
        "capacity": START_CAPACITY,
        "days_left": TOTAL_DAYS,
        "inventory": {gid: 0 for gid in GOODS_ORDER},
        "prices": {gid: 0 for gid in GOODS_ORDER},
        "total_goods": 0,
        "wangba_visits": 0,
        "hacker": False,
        "dead": False,
        "game_over": False,
        "seen_flags": [],
        "cooldowns": {},
        "bad_fame_baby": False,
        "bad_fame_alcohol": False,
        "day_index": 0,
        "last_events": [],
    }


def total_goods(state):
    return sum(state["inventory"].values())


def score(state):
    return int(state["cash"] + state["bank"] - state["debt"])


def _clamp_health(state):
    if state["health"] > 100:
        state["health"] = 100


def _clamp_fame(state):
    if state["health"] < 0:
        pass
    if state["fame"] < 0:
        state["fame"] = 0


def _event(ev_id, ev_type, text, **kwargs):
    out = {"id": ev_id, "type": ev_type, "text": text, "speaker": kwargs.get("speaker", "news")}
    for key in ("sfx", "speaker", "goods", "extra", "bg", "sprite"):
        if key in kwargs and kwargs[key] is not None:
            out[key] = kwargs[key]
    return out


def _roll(rng, modulus, freq):
    if not freq:
        return False
    return rng.randrange(modulus) % int(freq) == 0


def refresh_prices(state, rng):
    leaveout = 0 if state["days_left"] <= 2 else LEAVEOUT_NORMAL
    for g in GOODS:
        state["prices"][g["id"]] = g["base"] + rng.randrange(g["span"])
    for _ in range(leaveout):
        gid = GOODS_ORDER[rng.randrange(len(GOODS_ORDER))]
        state["prices"][gid] = 0


def apply_interest(state):
    state["debt"] = int(state["debt"] + state["debt"] * INTEREST_DEBT)
    state["bank"] = int(state["bank"] + state["bank"] * INTEREST_BANK)


def max_buy(state, gid):
    price = state["prices"].get(gid, 0)
    if price <= 0:
        return 0
    room = state["capacity"] - total_goods(state)
    if room <= 0 or state["cash"] < price:
        return 0
    return min(room, state["cash"] // price)


def buy(state, gid, qty):
    messages = []
    if gid not in GOODS_BY_ID:
        return messages
    price = state["prices"].get(gid, 0)
    if price <= 0:
        messages.append(_event(
            "no_market", "system",
            "哦？仿佛没有人在这里做%s生意。" % GOODS_BY_ID[gid]["name"],
            speaker="me",
        ))
        return messages
    actual = min(int(qty), max_buy(state, gid))
    if actual <= 0:
        return messages
    state["cash"] -= actual * price
    state["inventory"][gid] += actual
    state["total_goods"] = total_goods(state)
    return messages


def sell(state, gid, qty):
    messages = []
    if gid not in GOODS_BY_ID:
        return messages
    price = state["prices"].get(gid, 0)
    have = state["inventory"].get(gid, 0)
    if have <= 0:
        return messages
    if price <= 0:
        messages.append(_event(
            "no_buyer", "system",
            "哦？仿佛没有人在这里做%s生意。" % GOODS_BY_ID[gid]["name"],
            speaker="me",
        ))
        return messages
    actual = min(int(qty), have)
    if actual <= 0:
        return messages
    state["inventory"][gid] -= actual
    state["cash"] += actual * price
    state["total_goods"] = total_goods(state)
    hit = GOODS_BY_ID[gid]["fame_hit"]
    if hit:
        flag = "bad_fame_baby" if gid == "BABY" else "bad_fame_alcohol"
        harm = "污染社会,俺的名声变坏了啊!" if gid == "BABY" else "危害社会，俺的名声下降了."
        if not state[flag]:
            state[flag] = True
            messages.append(_event(
                flag, "system",
                "买卖%s，%s" % (GOODS_BY_ID[gid]["name"], harm),
                speaker="me",
            ))
        state["fame"] -= hit
        _clamp_fame(state)
    return messages


def deposit(state, amount):
    amount = max(0, min(int(amount), state["cash"]))
    state["cash"] -= amount
    state["bank"] += amount
    return amount


def withdraw(state, amount):
    amount = max(0, min(int(amount), state["bank"]))
    state["bank"] -= amount
    state["cash"] += amount
    return amount


def repay_debt(state, amount):
    messages = []
    amount = max(0, min(int(amount), state["debt"], state["cash"]))
    if amount <= 0:
        messages.append(_event(
            "cant_repay", "system",
            "村长老婆狂吞“雪中丐”补钙片，冷笑道：“你还得起吗?”",
            speaker="wife",
        ))
        return messages
    state["cash"] -= amount
    state["debt"] -= amount
    return messages


def heal(state, points):
    messages = []
    if state["health"] >= 100:
        messages.append(_event(
            "hospital_ok", "system",
            "小护士笑咪咪地望着俺：“大哥！神经科这边挂号。”",
            speaker="nurse",
            sfx="opendoor.wav",
        ))
        return messages
    points = max(0, min(int(points), 100 - state["health"]))
    cost = points * HOSPITAL_COST_PER_POINT
    if cost > state["cash"]:
        messages.append(_event(
            "hospital_broke", "system",
            "医生说，“钱不够哎! 拒绝治疗。”",
            speaker="doctor",
        ))
        return messages
    state["health"] += points
    state["cash"] -= cost
    _clamp_health(state)
    return messages


def visit_wangba(state, rng):
    messages = []
    if state["wangba_visits"] >= WANGBA_MAX_VISITS:
        messages.append(_event(
            "wangba_ban", "system",
            "村长放出话来：你别总是在网吧里鬼混，快去做正经买卖!",
            speaker="chief",
        ))
        return messages
    if state["cash"] < WANGBA_MIN_CASH:
        messages.append(_event(
            "wangba_broke", "system",
            "进网吧至少身上要带15元，呵呵，取钱再来。",
            speaker="netbar",
        ))
        return messages
    state["wangba_visits"] += 1
    gain = 1 + rng.randrange(10)
    state["cash"] += gain
    messages.append(_event(
        "wangba_ad", "system",
        "感谢电信改革，可以免费上网! 还挣了美国网络广告费%d元，嘿嘿!" % gain,
        speaker="me",
        sfx="opendoor.wav",
    ))
    return messages


def rent_house(state):
    messages = []
    if state["capacity"] >= MAX_CAPACITY:
        messages.append(_event(
            "house_max", "system",
            "中介说，您的房子比局长的还大!还租房?",
            speaker="agent",
        ))
        return messages
    if state["cash"] < HOUSE_MIN_CASH:
        messages.append(_event(
            "house_broke", "system",
            "中介说，您没有三万现金就想租房? 一边凉快去!",
            speaker="agent",
        ))
        return messages
    if state["cash"] <= HOUSE_MIN_CASH:
        state["cash"] -= 25000
    else:
        state["cash"] = state["cash"] // 2 - 2000
    state["capacity"] += HOUSE_STEP
    messages.append(_event(
        "house_ok", "system",
        "我的房子可以放%d个物品了!可是，好象中介公司骗了我一些钱..." % state["capacity"],
        speaker="me",
    ))
    return messages


def post_no_debt_line(state):
    wealth = state["cash"] + state["bank"]
    if wealth < 1000:
        return "村长嘿嘿笑道：“你没钱,有神经病!”"
    if wealth < 100000:
        return "村长朝俺点头：“兄弟,您想支援家乡1000元吗？”"
    if wealth < 10000000:
        return "村长在电话中朝俺鞠躬:“富豪!我想把我女儿嫁给您.”..."
    return "村长在电话中朝俺下跪，说：“您简直是我亲爹！”"


def _add_goods(state, gid, qty):
    room = state["capacity"] - total_goods(state)
    addcount = min(qty, room)
    if addcount <= 0:
        return 0
    state["inventory"][gid] += addcount
    state["total_goods"] = total_goods(state)
    return addcount


def _event_allowed(state, spec):
    if spec.get("once") and spec["id"] in state["seen_flags"]:
        return False
    cd = state["cooldowns"].get(spec["id"], 0)
    if cd > 0:
        return False
    cond = spec.get("conditions") or {}
    day = TOTAL_DAYS - state["days_left"]
    if day < cond.get("min_day", 0):
        return False
    if cond.get("max_day") is not None and day > cond["max_day"]:
        return False
    locs = cond.get("locations") or []
    if locs and state["location"] not in locs:
        return False
    if state["fame"] < cond.get("min_fame", -9999):
        return False
    if "max_fame" in cond and state["fame"] > cond["max_fame"]:
        return False
    if "max_health" in cond and state["health"] > cond["max_health"]:
        return False
    if "min_debt" in cond and state["debt"] < cond["min_debt"]:
        return False
    for flag in cond.get("flags_all") or []:
        if flag not in state["seen_flags"]:
            return False
    return True


def _apply_commercial(state, spec, rng):
    messages = []
    gid = spec.get("goods")
    if gid and state["prices"].get(gid, 0) == 0:
        return messages
    text = spec["text"]
    if spec["id"] == "chief_phone":
        state["debt"] += PHONE_EVENT_DEBT
    effects = spec.get("effects") or {}
    if effects.get("multiply") and gid:
        state["prices"][gid] *= int(effects["multiply"])
    if effects.get("divide") and gid:
        state["prices"][gid] = int(state["prices"][gid] / int(effects["divide"]))
    add = int(effects.get("add") or 0)
    if add and gid:
        added = _add_goods(state, gid, add)
        if added == 0:
            messages.append(_event(
                spec["id"], spec["type"], text, speaker=spec.get("speaker", "news"),
                sfx=spec.get("sfx"), goods=gid,
            ))
            messages.append(_event(
                "house_full", "system",
                "可惜!俺租的房子太小，只能放%d个物品。" % state["capacity"],
                speaker="me",
            ))
            return messages
    messages.append(_event(
        spec["id"], spec["type"], text,
        speaker=spec.get("speaker", "news"),
        sfx=spec.get("sfx"),
        goods=gid,
        sprite=spec.get("sprite"),
        bg=spec.get("bg"),
    ))
    return messages


def _apply_health(state, spec):
    hunt = int((spec.get("effects") or {}).get("health") or 0)
    state["health"] += hunt
    text = spec["text"]
    if hunt < 0:
        text = "%s俺的健康减少了%d点。" % (text, -hunt)
    return [_event(
        spec["id"], "health", text,
        speaker=spec.get("speaker", "me"),
        sfx=spec.get("sfx"),
    )]


def _apply_cash_or_bank(state, spec):
    ratio = int((spec.get("effects") or {}).get("ratio") or 0)
    target = spec.get("type")
    messages = []
    text = spec["text"]
    if target == "cash":
        text += "俺的银子减少了%d%%。" % ratio
        state["cash"] = int((state["cash"] / 100) * (100 - ratio))
        if state["cash"] < 0:
            state["cash"] = 0
    elif target == "bank":
        if state["bank"] <= 0:
            return messages
        text += "俺的存款减少了%d%%。，哎呀!" % ratio
        state["bank"] = int((state["bank"] / 100) * (100 - ratio))
    messages.append(_event(
        spec["id"], target, text,
        speaker=spec.get("speaker", "me"),
        sfx=spec.get("sfx"),
    ))
    return messages


def _tick_cooldowns(state):
    dead = []
    for k, v in list(state["cooldowns"].items()):
        nv = v - 1
        if nv <= 0:
            dead.append(k)
        else:
            state["cooldowns"][k] = nv
    for k in dead:
        state["cooldowns"].pop(k, None)


def _mark_seen(state, spec):
    if spec.get("once"):
        if spec["id"] not in state["seen_flags"]:
            state["seen_flags"].append(spec["id"])
    cd = spec.get("cooldown") or 0
    if cd:
        state["cooldowns"][spec["id"]] = cd


def run_catalog(state, catalog, rng, kinds, modulus, stop_on_first):
    messages = []
    for spec in catalog:
        if spec.get("type") not in kinds:
            continue
        if not _event_allowed(state, spec):
            continue
        freq = spec.get("weight") or spec.get("freq") or 0
        if not _roll(rng, modulus, freq):
            continue
        kind = spec["type"]
        if kind in ("price", "goods"):
            chunk = _apply_commercial(state, spec, rng)
        elif kind == "health":
            chunk = _apply_health(state, spec)
        elif kind in ("cash", "bank"):
            chunk = _apply_cash_or_bank(state, spec)
        elif kind == "story":
            chunk = [_event(
                spec["id"], "story", spec["text"],
                speaker=spec.get("speaker", "chief"),
                sfx=spec.get("sfx"),
                sprite=spec.get("sprite"),
                bg=spec.get("bg"),
            )]
        else:
            chunk = []
        if chunk:
            _mark_seen(state, spec)
            messages.extend(chunk)
            if stop_on_first:
                break
            if any(m["id"] == "house_full" for m in chunk):
                break
    return messages


def maybe_hospital(state, rng):
    messages = []
    if state["health"] >= 85 or state["days_left"] <= 3:
        return messages
    delay = 1 + rng.randrange(2)
    loc = LOC_BY_ID.get(state["location"], {}).get("name", "北京")
    spot = HOSPITAL_SPOTS[rng.randrange(len(HOSPITAL_SPOTS))]
    load = delay * (1000 + rng.randrange(8500))
    msg1 = "好心的市民把我抬到医院，医生让我治疗%d天。" % delay
    msg2 = "由于不注意身体,我被人发现昏迷在%s附近的%s。" % (loc, spot)
    msg3 = "村长让人为我垫付了住院费用%d元。" % load
    state["debt"] += load
    state["health"] += 10
    _clamp_health(state)
    state["days_left"] -= delay
    if state["days_left"] < 0:
        state["days_left"] = 0
    messages.append(_event("forced_hospital", "system", msg1, speaker="doctor"))
    messages.append(_event("forced_hospital_2", "system", msg2, speaker="me"))
    messages.append(_event("forced_hospital_3", "system", msg3, speaker="chief"))
    return messages


def maybe_hacker(state, rng):
    messages = []
    if not state.get("hacker"):
        return messages
    if rng.randrange(1000) % 25 != 0:
        return messages
    if state["bank"] < 1000:
        return messages
    if state["bank"] > 100000:
        num = int(state["bank"] / (2 + rng.randrange(20)))
        if rng.randrange(20) % 3 != 0:
            state["bank"] -= num
            text = "黑客入侵银行网络，疯狂修改数据库，我的存款减少了%d" % num
        else:
            state["bank"] += num
            text = "黑客入侵银行网络，疯狂修改数据库，我的存款增加了%d" % num
    else:
        num = int(state["bank"] / (1 + rng.randrange(15)))
        state["bank"] += num
        text = "黑客入侵银行网络，疯狂修改数据库，我的存款增加了%d" % num
    messages.append(_event("hacker", "bank", text, speaker="news"))
    return messages


def force_sell_all(state):
    gained = 0
    names = []
    for gid, qty in list(state["inventory"].items()):
        if qty <= 0:
            continue
        price = state["prices"].get(gid, 0)
        gained += qty * price
        names.append(GOODS_BY_ID[gid]["name"])
        state["inventory"][gid] = 0
    state["cash"] += gained
    state["total_goods"] = 0
    return names, gained


def story_beats(state, catalog, rng):
    """Deterministic story beats by day, independent of freq rolls."""
    messages = []
    day = TOTAL_DAYS - state["days_left"]
    for spec in catalog:
        if spec.get("type") != "story":
            continue
        cond = spec.get("conditions") or {}
        if cond.get("exact_day") is None:
            continue
        if day != cond["exact_day"]:
            continue
        if not _event_allowed(state, spec):
            continue
        extra = spec.get("variants") or []
        text = spec["text"]
        speaker = spec.get("speaker", "chief")
        if extra:
            if state["debt"] >= 20000 and extra:
                text = extra[0].get("text", text)
                speaker = extra[0].get("speaker", speaker)
            elif state["debt"] == 0 and len(extra) > 1:
                text = extra[1].get("text", text)
                speaker = extra[1].get("speaker", speaker)
        messages.append(_event(
            spec["id"], "story", text,
            speaker=speaker,
            sprite=spec.get("sprite"),
        ))
        _mark_seen(state, spec)
    return messages


def move_to(state, location_id, rng, catalog):
    """Change location, spend a day, return event list."""
    messages = []
    if location_id not in LOC_BY_ID:
        return messages
    if location_id == state["location"] and state["day_index"] > 0:
        return messages

    state["location"] = location_id
    refresh_prices(state, rng)
    apply_interest(state)

    flavor = LOCATION_FLAVOR.get(location_id)
    if flavor:
        messages.append(_event("flavor", "flavor", flavor, speaker="me"))

    messages.extend(story_beats(state, catalog, rng))
    messages.extend(run_catalog(state, catalog, rng, ("price", "goods"), 950, False))
    messages.extend(run_catalog(state, catalog, rng, ("health",), 1000, True))

    hospital = maybe_hospital(state, rng)
    if hospital:
        messages.extend(hospital)
    else:
        if 0 < state["health"] < 20:
            messages.append(_event(
                "health_warn", "system",
                "俺的健康..健康危机..快去医..",
                speaker="me",
            ))
        if state["health"] < 0:
            state["dead"] = True
            messages.append(_event(
                "death", "ending",
                "俺倒在街头,身边日记本上写着：“北京，我将再来!”",
                speaker="me",
                sfx="death.wav",
            ))
            return messages

    messages.extend(run_catalog(state, catalog, rng, ("cash", "bank"), 1000, True))
    messages.extend(maybe_hacker(state, rng))

    if state["debt"] > DEBT_PUNISH_THRESHOLD:
        state["health"] -= DEBT_PUNISH_HEALTH
        messages.append(_event(
            "debt_thugs", "health",
            "俺欠钱太多，村长叫一群老乡揍了俺一顿!",
            speaker="chief",
            sfx="kill.wav",
        ))
        if state["health"] < 0:
            state["dead"] = True
            messages.append(_event(
                "death", "ending",
                "俺倒在街头,身边日记本上写着：“北京，我将再来!”",
                speaker="me",
                sfx="death.wav",
            ))
            return messages

    _tick_cooldowns(state)
    state["days_left"] -= 1
    state["day_index"] = TOTAL_DAYS - state["days_left"]
    if state["cash"] < 0:
        state["cash"] = 0

    if state["days_left"] == 1:
        messages.append(_event(
            "tomorrow_home", "story",
            "俺明天回家乡，快把全部货物卖掉。",
            speaker="me",
        ))
    if state["days_left"] <= 0:
        names, gained = force_sell_all(state)
        messages.append(_event(
            "day40", "story",
            "俺已经在北京40天了，该回去结婚去了。",
            speaker="me",
        ))
        if names:
            messages.append(_event(
                "autosell", "system",
                "系统替我卖了剩余货物: %s。换得%d元。" % ("、".join(names), gained),
                speaker="news",
            ))
        state["game_over"] = True
    state["last_events"] = [m["id"] for m in messages]
    state["total_goods"] = total_goods(state)
    return messages


def reset(rng=None):
    state = new_state()
    rng = rng or random.Random()
    refresh_prices(state, rng)
    return state


def ending_rank(state):
    s = score(state)
    if state.get("dead"):
        return "death", "倒在北京街头", s
    if s < 0:
        return "broke", "两手空空回乡", s
    if s < 50000:
        return "ok", "还清债务，勉强回家结婚", s
    if s < 500000:
        return "rich", "荣登北京小富人榜", s
    return "tycoon", "北京富人排行榜前列", s


def snapshot(state):
    return deepcopy(state)
