init python:
    def fs_image(name, color):
        path = "images/" + name + ".png"
        if renpy.loadable(path):
            return path
        return Solid(color)

    def fs_bg_name():
        loc = fushengji_sim.LOC_BY_ID.get(gs["location"], {})
        return "bg " + loc.get("bg", "market_station")

    GOOD_IMAGE = {
        "CIGARETTE": "good cigarette",
        "CAR": "good car",
        "CD": "good cd",
        "ALCOHOL": "good alcohol",
        "BABY": "good baby",
        "TOY": "good toy",
        "PHONES": "good phones",
        "COSMETIC": "good cosmetic",
    }

    NPC_SPRITE = {
        "chief": "npc chief",
        "doctor": "npc doctor",
        "nurse": "npc nurse",
        "agent": "npc agent",
        "netbar": "npc netbar",
        "xiebufeng": "npc xiebufeng",
        "teller": "npc teller",
        "wife": "npc chief",
    }

    MAP_GROUPS = [
        ("西边", ["pingguoyuan", "bajiao", "cuiwei", "gongzhufen"]),
        ("北边", ["xizhimen", "jishuitan"]),
        ("东北", ["dongzhimen", "sanyuan", "beichen"]),
        ("城里", ["fuxingmen", "haidian", "wenjin"]),
        ("东边", ["jianguomen", "yonganli"]),
        ("内城", ["beijingzhan", "chongwenmen", "changchunjie"]),
        ("南边", ["yongdingmen", "fangzhuang", "caihuying"]),
    ]


image bg market_station = fs_image("bg market_station", "#4a3a28")
image bg market_east = fs_image("bg market_east", "#3d3428")
image bg market_north = fs_image("bg market_north", "#35382e")
image bg market_inner = fs_image("bg market_inner", "#3a2f2a")
image bg market_northeast = fs_image("bg market_northeast", "#403428")
image bg market_center = fs_image("bg market_center", "#2f3330")
image bg market_west = fs_image("bg market_west", "#3a3324")
image bg market_south = fs_image("bg market_south", "#403028")
image bg market_haidian = fs_image("bg market_haidian", "#2c3a32")
image bg market_ring = fs_image("bg market_ring", "#383430")
image bg hospital = fs_image("bg hospital", "#2a3a3a")
image bg bank = fs_image("bg bank", "#2a3228")
image bg post = fs_image("bg post", "#3a2a28")
image bg wangba = fs_image("bg wangba", "#1e2430")
image bg house = fs_image("bg house", "#3a3428")
image bg ending_death = fs_image("bg ending_death", "#1a1010")
image bg ending_home = fs_image("bg ending_home", "#2a2818")
image bg map_beijing = fs_image("bg map_beijing", "#243028")

image hero normal = fs_image("hero normal", "#6a5340")
image npc chief = fs_image("npc chief", "#5a3020")
image npc doctor = fs_image("npc doctor", "#d8d8d0")
image npc nurse = fs_image("npc nurse", "#c8a0a8")
image npc teller = fs_image("npc teller", "#3a4a3a")
image npc agent = fs_image("npc agent", "#4a4030")
image npc netbar = fs_image("npc netbar", "#2a3040")
image npc xiebufeng = fs_image("npc xiebufeng", "#704050")

image good cigarette = fs_image("good cigarette", "#6a4030")
image good car = fs_image("good car", "#304060")
image good cd = fs_image("good cd", "#404040")
image good alcohol = fs_image("good alcohol", "#5a3020")
image good baby = fs_image("good baby", "#5a3048")
image good toy = fs_image("good toy", "#305040")
image good phones = fs_image("good phones", "#303038")
image good cosmetic = fs_image("good cosmetic", "#603048")


transform fs_left:
    zoom 0.34
    xalign 0.0
    yalign 1.0
    yoffset 70

transform fs_right:
    zoom 0.34
    xalign 1.0
    yalign 1.0
    yoffset 70
