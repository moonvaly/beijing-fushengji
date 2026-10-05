export type Rng = { randrange: (n: number) => number };

export class SeededRng implements Rng {
  private s: number;
  constructor(seed: number) {
    this.s = seed >>> 0 || 1;
  }
  randrange(n: number): number {
    this.s += 0x6d2b79f5;
    let t = this.s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    const r = ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    return Math.floor(r * n);
  }
}

export function nativeRng(): Rng {
  return { randrange: (n) => Math.floor(Math.random() * n) };
}

export const TOTAL_DAYS = 40;
export const START_CASH = 2000;
export const START_DEBT = 5000;
export const HOSPITAL_COST_PER_POINT = 3500;
export const WANGBA_MAX_VISITS = 3;
export const WANGBA_MIN_CASH = 15;
export const HOUSE_MIN_CASH = 30000;
export const MAX_CAPACITY = 140;
export const HOUSE_STEP = 10;
export const DEBT_PUNISH_THRESHOLD = 100000;
export const DEBT_PUNISH_HEALTH = 30;
export const INTEREST_DEBT = 0.1;
export const INTEREST_BANK = 0.01;
export const LEAVEOUT_NORMAL = 3;
export const PHONE_EVENT_DEBT = 2500;

export type GoodId =
  | "CIGARETTE"
  | "CAR"
  | "CD"
  | "ALCOHOL"
  | "BABY"
  | "TOY"
  | "PHONES"
  | "COSMETIC";

export const GOODS: { id: GoodId; name: string; base: number; span: number; fame_hit: number }[] = [
  { id: "CIGARETTE", name: "进口香烟", base: 100, span: 350, fame_hit: 0 },
  { id: "CAR", name: "走私汽车", base: 15000, span: 15000, fame_hit: 0 },
  { id: "CD", name: "盗版 VCD / 游戏", base: 5, span: 50, fame_hit: 0 },
  { id: "ALCOHOL", name: "假白酒（剧毒）", base: 1000, span: 2500, fame_hit: 10 },
  { id: "BABY", name: "《上海小宝贝》盗版刊物", base: 5000, span: 9000, fame_hit: 7 },
  { id: "TOY", name: "进口玩具", base: 250, span: 600, fame_hit: 0 },
  { id: "PHONES", name: "水货手机", base: 750, span: 750, fame_hit: 0 },
  { id: "COSMETIC", name: "伪劣化妆品", base: 65, span: 180, fame_hit: 0 },
];

export const GOODS_BY_ID = Object.fromEntries(GOODS.map((g) => [g.id, g])) as Record<
  GoodId,
  (typeof GOODS)[number]
>;
export const GOODS_ORDER = GOODS.map((g) => g.id);

export const GOOD_IMAGE: Record<GoodId, string> = {
  CIGARETTE: "good cigarette.png",
  CAR: "good car.png",
  CD: "good cd.png",
  ALCOHOL: "good alcohol.png",
  BABY: "good baby.png",
  TOY: "good toy.png",
  PHONES: "good phones.png",
  COSMETIC: "good cosmetic.png",
};

export const LOCATIONS = [
  { id: "jianguomen", name: "建国门", bg: "market_east" },
  { id: "beijingzhan", name: "北京站", bg: "market_station" },
  { id: "xizhimen", name: "西直门", bg: "market_north" },
  { id: "chongwenmen", name: "崇文门", bg: "market_inner" },
  { id: "dongzhimen", name: "东直门", bg: "market_northeast" },
  { id: "fuxingmen", name: "复兴门", bg: "market_center" },
  { id: "jishuitan", name: "积水潭", bg: "market_north" },
  { id: "changchunjie", name: "长椿街", bg: "market_inner" },
  { id: "gongzhufen", name: "公主坟", bg: "market_west" },
  { id: "pingguoyuan", name: "苹果园", bg: "market_west" },
  { id: "yonganli", name: "永安里", bg: "market_east" },
  { id: "fangzhuang", name: "方庄", bg: "market_south" },
  { id: "haidian", name: "海淀大街", bg: "market_haidian" },
  { id: "yongdingmen", name: "永定门", bg: "market_south" },
  { id: "sanyuan", name: "三元东桥", bg: "market_ring" },
  { id: "wenjin", name: "文津街", bg: "market_haidian" },
  { id: "beichen", name: "北辰西路", bg: "market_ring" },
  { id: "caihuying", name: "菜户营", bg: "market_south" },
  { id: "cuiwei", name: "翠微路", bg: "market_west" },
  { id: "bajiao", name: "八角地铁", bg: "market_west" },
] as const;

export type LocId = (typeof LOCATIONS)[number]["id"];
export const LOC_BY_ID = Object.fromEntries(LOCATIONS.map((l) => [l.id, l])) as Record<
  LocId,
  (typeof LOCATIONS)[number]
>;

export const LOCATION_FLAVOR: Record<string, string> = {
  jianguomen: "建国门立交桥底下，倒爷们把货物码成一堵墙。",
  beijingzhan: "北京站出站口人潮把俺挤得转不过身，黑市就藏在过街地道里。",
  xizhimen: "西直门城墙根儿，风沙里飘着烤地瓜和盗版碟的味道。",
  chongwenmen: "崇文门新世界旁边，红袖章老太太正盯着外地人。",
  dongzhimen: "东直门长途汽车站，东北口音和假烟箱子挤在一块。",
  fuxingmen: "复兴门金融街还没起来，地下通道里全是卖水货的。",
  jishuitan: "积水潭医院门口，有人低声问俺要不要进口药。",
  changchunjie: "长椿街夜市收摊，剩货都往俺怀里塞。",
  gongzhufen: "公主坟城乡结合部，军大衣和走私车广告贴满电线杆。",
  pingguoyuan: "苹果园是西边尽头，黑市跟煤矿似的，黑、乱、便宜。",
  yonganli: "永安里的写字楼玻璃反光，楼下地摊一样敢卖汽车钥匙。",
  fangzhuang: "方庄小区自行车棚后头，民工和大学生抢同一箱VCD。",
  haidian: "海淀大街中关村，村姑一字排开全是盗版碟。",
  yongdingmen: "永定门城楼还在，城根下的货比城楼还杂。",
  sanyuan: "三元东桥堵车堵到天黑，俺在车缝里把货倒了出去。",
  wenjin: "文津街靠近中南海，巡逻多，买卖都得快。",
  beichen: "北辰西路亚运村边，有钱人路过也敢问水货手机。",
  caihuying: "菜户营货场尘土大，箱子一开全是广东来的私货。",
  cuiwei: "翠微路商场对面，假化妆品包装比真的还亮。",
  bajiao: "八角地铁口风大，俺把货压在砖头底下等买主。",
};

export const MAP_GROUPS: [string, LocId[]][] = [
  ["西边", ["pingguoyuan", "bajiao", "cuiwei", "gongzhufen"]],
  ["北边", ["xizhimen", "jishuitan"]],
  ["东北", ["dongzhimen", "sanyuan", "beichen"]],
  ["城里", ["fuxingmen", "haidian", "wenjin"]],
  ["东边", ["jianguomen", "yonganli"]],
  ["内城", ["beijingzhan", "chongwenmen", "changchunjie"]],
  ["南边", ["yongdingmen", "fangzhuang", "caihuying"]],
];

const HOSPITAL_SPOTS = [
  "发廊里", "早点摊上", "报摊上", "烤羊肉摊上", "公共汽车里",
  "人力车上", "电话亭里", "出租车里", "小巴里", "美容院里",
  "小商亭里", "小商场门口", "民工脚下", "无照游商摊里", "草地上",
  "小饭馆里", "马路边", "人行道上", "街心公园里", "广告牌下",
  "公共汽车站里", "长途汽车站里", "卖盗版游戏的旁边",
];

export type GameState = {
  location: LocId;
  cash: number;
  debt: number;
  bank: number;
  health: number;
  fame: number;
  capacity: number;
  days_left: number;
  inventory: Record<GoodId, number>;
  prices: Record<GoodId, number>;
  total_goods: number;
  wangba_visits: number;
  hacker: boolean;
  dead: boolean;
  game_over: boolean;
  seen_flags: string[];
  cooldowns: Record<string, number>;
  bad_fame_baby: boolean;
  bad_fame_alcohol: boolean;
  day_index: number;
  last_events: string[];
};

export type GameEvent = {
  id: string;
  type: string;
  text: string;
  speaker: string;
  sfx?: string;
  goods?: string;
  sprite?: string;
  bg?: string;
};

export type EventSpec = {
  id: string;
  type: string;
  weight?: number;
  freq?: number;
  goods?: GoodId;
  speaker?: string;
  sfx?: string;
  sprite?: string;
  bg?: string;
  text: string;
  once?: boolean;
  cooldown?: number;
  effects?: { multiply?: number; divide?: number; add?: number; health?: number; ratio?: number };
  conditions?: Record<string, unknown>;
  variants?: { text: string; speaker?: string }[];
};

function event(id: string, type: string, text: string, extra: Partial<GameEvent> = {}): GameEvent {
  return { id, type, text, speaker: extra.speaker ?? "news", ...extra };
}

export function newState(): GameState {
  const inventory = {} as Record<GoodId, number>;
  const prices = {} as Record<GoodId, number>;
  for (const gid of GOODS_ORDER) {
    inventory[gid] = 0;
    prices[gid] = 0;
  }
  return {
    location: "beijingzhan",
    cash: START_CASH,
    debt: START_DEBT,
    bank: 0,
    health: 100,
    fame: 100,
    capacity: 100,
    days_left: TOTAL_DAYS,
    inventory,
    prices,
    total_goods: 0,
    wangba_visits: 0,
    hacker: false,
    dead: false,
    game_over: false,
    seen_flags: [],
    cooldowns: {},
    bad_fame_baby: false,
    bad_fame_alcohol: false,
    day_index: 0,
    last_events: [],
  };
}

export function totalGoods(state: GameState): number {
  return GOODS_ORDER.reduce((s, g) => s + state.inventory[g], 0);
}

export function score(state: GameState): number {
  return Math.trunc(state.cash + state.bank - state.debt);
}

function clampHealth(state: GameState) {
  if (state.health > 100) state.health = 100;
}
function clampFame(state: GameState) {
  if (state.fame < 0) state.fame = 0;
}

function roll(rng: Rng, modulus: number, freq: number): boolean {
  if (!freq) return false;
  return rng.randrange(modulus) % Math.trunc(freq) === 0;
}

export function refreshPrices(state: GameState, rng: Rng) {
  const leaveout = state.days_left <= 2 ? 0 : LEAVEOUT_NORMAL;
  for (const g of GOODS) {
    state.prices[g.id] = g.base + rng.randrange(g.span);
  }
  for (let i = 0; i < leaveout; i++) {
    const gid = GOODS_ORDER[rng.randrange(GOODS_ORDER.length)];
    state.prices[gid] = 0;
  }
}

export function applyInterest(state: GameState) {
  state.debt = Math.trunc(state.debt + state.debt * INTEREST_DEBT);
  state.bank = Math.trunc(state.bank + state.bank * INTEREST_BANK);
}

export function maxBuy(state: GameState, gid: GoodId): number {
  const price = state.prices[gid] || 0;
  if (price <= 0) return 0;
  const room = state.capacity - totalGoods(state);
  if (room <= 0 || state.cash < price) return 0;
  return Math.min(room, Math.floor(state.cash / price));
}

export function buy(state: GameState, gid: GoodId, qty: number): GameEvent[] {
  const g = GOODS_BY_ID[gid];
  if (!g) return [];
  const price = state.prices[gid] || 0;
  if (price <= 0) {
    return [event("no_market", "system", `哦？仿佛没有人在这里做${g.name}生意。`, { speaker: "me" })];
  }
  const actual = Math.min(Math.trunc(qty), maxBuy(state, gid));
  if (actual <= 0) return [];
  state.cash -= actual * price;
  state.inventory[gid] += actual;
  state.total_goods = totalGoods(state);
  return [];
}

export function sell(state: GameState, gid: GoodId, qty: number): GameEvent[] {
  const g = GOODS_BY_ID[gid];
  if (!g) return [];
  const price = state.prices[gid] || 0;
  const have = state.inventory[gid] || 0;
  if (have <= 0) return [];
  if (price <= 0) {
    return [event("no_buyer", "system", `哦？仿佛没有人在这里做${g.name}生意。`, { speaker: "me" })];
  }
  const actual = Math.min(Math.trunc(qty), have);
  if (actual <= 0) return [];
  state.inventory[gid] -= actual;
  state.cash += actual * price;
  state.total_goods = totalGoods(state);
  const hit = g.fame_hit;
  const messages: GameEvent[] = [];
  if (hit) {
    const flag = gid === "BABY" ? "bad_fame_baby" : "bad_fame_alcohol";
    const harm = gid === "BABY" ? "污染社会,俺的名声变坏了啊!" : "危害社会，俺的名声下降了.";
    if (!state[flag]) {
      state[flag] = true;
      messages.push(event(flag, "system", `买卖${g.name}，${harm}`, { speaker: "me" }));
    }
    state.fame -= hit;
    clampFame(state);
  }
  return messages;
}

export function deposit(state: GameState, amount: number): number {
  amount = Math.max(0, Math.min(Math.trunc(amount), state.cash));
  state.cash -= amount;
  state.bank += amount;
  return amount;
}

export function withdraw(state: GameState, amount: number): number {
  amount = Math.max(0, Math.min(Math.trunc(amount), state.bank));
  state.bank -= amount;
  state.cash += amount;
  return amount;
}

export function repayDebt(state: GameState, amount: number): GameEvent[] {
  amount = Math.max(0, Math.min(Math.trunc(amount), state.debt, state.cash));
  if (amount <= 0) {
    return [
      event("cant_repay", "system", "村长老婆狂吞“雪中丐”补钙片，冷笑道：“你还得起吗?”", {
        speaker: "wife",
      }),
    ];
  }
  state.cash -= amount;
  state.debt -= amount;
  return [];
}

export function heal(state: GameState, points: number): GameEvent[] {
  if (state.health >= 100) {
    return [
      event("hospital_ok", "system", "小护士笑咪咪地望着俺：“大哥！神经科这边挂号。”", {
        speaker: "nurse",
        sfx: "opendoor.wav",
      }),
    ];
  }
  points = Math.max(0, Math.min(Math.trunc(points), 100 - state.health));
  const cost = points * HOSPITAL_COST_PER_POINT;
  if (cost > state.cash) {
    return [event("hospital_broke", "system", "医生说，“钱不够哎! 拒绝治疗。”", { speaker: "doctor" })];
  }
  state.health += points;
  state.cash -= cost;
  clampHealth(state);
  return [];
}

export function visitWangba(state: GameState, rng: Rng): GameEvent[] {
  if (state.wangba_visits >= WANGBA_MAX_VISITS) {
    return [
      event("wangba_ban", "system", "村长放出话来：你别总是在网吧里鬼混，快去做正经买卖!", {
        speaker: "chief",
      }),
    ];
  }
  if (state.cash < WANGBA_MIN_CASH) {
    return [
      event("wangba_broke", "system", "进网吧至少身上要带15元，呵呵，取钱再来。", { speaker: "netbar" }),
    ];
  }
  state.wangba_visits += 1;
  const gain = 1 + rng.randrange(10);
  state.cash += gain;
  return [
    event("wangba_ad", "system", `感谢电信改革，可以免费上网! 还挣了美国网络广告费${gain}元，嘿嘿!`, {
      speaker: "me",
      sfx: "opendoor.wav",
    }),
  ];
}

export function rentHouse(state: GameState): GameEvent[] {
  if (state.capacity >= MAX_CAPACITY) {
    return [event("house_max", "system", "中介说，您的房子比局长的还大!还租房?", { speaker: "agent" })];
  }
  if (state.cash < HOUSE_MIN_CASH) {
    return [
      event("house_broke", "system", "中介说，您没有三万现金就想租房? 一边凉快去!", { speaker: "agent" }),
    ];
  }
  if (state.cash <= HOUSE_MIN_CASH) state.cash -= 25000;
  else state.cash = Math.floor(state.cash / 2) - 2000;
  state.capacity += HOUSE_STEP;
  return [
    event("house_ok", "system", `我的房子可以放${state.capacity}个物品了!可是，好象中介公司骗了我一些钱...`, {
      speaker: "me",
    }),
  ];
}

export function postNoDebtLine(state: GameState): string {
  const wealth = state.cash + state.bank;
  if (wealth < 1000) return "村长嘿嘿笑道：“你没钱,有神经病!”";
  if (wealth < 100000) return "村长朝俺点头：“兄弟,您想支援家乡1000元吗？”";
  if (wealth < 10000000) return "村长在电话中朝俺鞠躬:“富豪!我想把我女儿嫁给您.”...";
  return "村长在电话中朝俺下跪，说：“您简直是我亲爹！”";
}

function addGoods(state: GameState, gid: GoodId, qty: number): number {
  const room = state.capacity - totalGoods(state);
  const addcount = Math.min(qty, room);
  if (addcount <= 0) return 0;
  state.inventory[gid] += addcount;
  state.total_goods = totalGoods(state);
  return addcount;
}

function eventAllowed(state: GameState, spec: EventSpec): boolean {
  if (spec.once && state.seen_flags.includes(spec.id)) return false;
  if ((state.cooldowns[spec.id] || 0) > 0) return false;
  const cond = spec.conditions || {};
  const day = TOTAL_DAYS - state.days_left;
  if (day < (Number(cond.min_day) || 0)) return false;
  if (cond.max_day != null && day > Number(cond.max_day)) return false;
  const locs = (cond.locations as string[] | undefined) || [];
  if (locs.length && !locs.includes(state.location)) return false;
  if (state.fame < (Number(cond.min_fame) || -9999)) return false;
  if ("max_fame" in cond && state.fame > Number(cond.max_fame)) return false;
  if ("max_health" in cond && state.health > Number(cond.max_health)) return false;
  if ("min_debt" in cond && state.debt < Number(cond.min_debt)) return false;
  for (const flag of (cond.flags_all as string[] | undefined) || []) {
    if (!state.seen_flags.includes(flag)) return false;
  }
  return true;
}

function applyCommercial(state: GameState, spec: EventSpec, _rng: Rng): GameEvent[] {
  const gid = spec.goods;
  if (gid && (state.prices[gid] || 0) === 0) return [];
  const text = spec.text;
  if (spec.id === "chief_phone") state.debt += PHONE_EVENT_DEBT;
  const effects = spec.effects || {};
  if (effects.multiply && gid) state.prices[gid] *= effects.multiply;
  if (effects.divide && gid) state.prices[gid] = Math.trunc(state.prices[gid] / effects.divide);
  const add = Math.trunc(effects.add || 0);
  if (add && gid) {
    const added = addGoods(state, gid, add);
    if (added === 0) {
      return [
        event(spec.id, spec.type, text, { speaker: spec.speaker || "news", sfx: spec.sfx, goods: gid }),
        event("house_full", "system", `可惜!俺租的房子太小，只能放${state.capacity}个物品。`, {
          speaker: "me",
        }),
      ];
    }
  }
  return [
    event(spec.id, spec.type, text, {
      speaker: spec.speaker || "news",
      sfx: spec.sfx,
      goods: gid,
      sprite: spec.sprite,
      bg: spec.bg,
    }),
  ];
}

function applyHealth(state: GameState, spec: EventSpec): GameEvent[] {
  const hunt = Math.trunc(spec.effects?.health || 0);
  state.health += hunt;
  let text = spec.text;
  if (hunt < 0) text = `${text}俺的健康减少了${-hunt}点。`;
  return [event(spec.id, "health", text, { speaker: spec.speaker || "me", sfx: spec.sfx })];
}

function applyCashOrBank(state: GameState, spec: EventSpec): GameEvent[] {
  const ratio = Math.trunc(spec.effects?.ratio || 0);
  const target = spec.type;
  let text = spec.text;
  if (target === "cash") {
    text += `俺的银子减少了${ratio}%。`;
    state.cash = Math.trunc((state.cash / 100) * (100 - ratio));
    if (state.cash < 0) state.cash = 0;
  } else if (target === "bank") {
    if (state.bank <= 0) return [];
    text += `俺的存款减少了${ratio}%。，哎呀!`;
    state.bank = Math.trunc((state.bank / 100) * (100 - ratio));
  }
  return [event(spec.id, target, text, { speaker: spec.speaker || "me", sfx: spec.sfx })];
}

function tickCooldowns(state: GameState) {
  for (const k of Object.keys(state.cooldowns)) {
    const nv = state.cooldowns[k] - 1;
    if (nv <= 0) delete state.cooldowns[k];
    else state.cooldowns[k] = nv;
  }
}

function markSeen(state: GameState, spec: EventSpec) {
  if (spec.once && !state.seen_flags.includes(spec.id)) state.seen_flags.push(spec.id);
  if (spec.cooldown) state.cooldowns[spec.id] = spec.cooldown;
}

function runCatalog(
  state: GameState,
  catalog: EventSpec[],
  rng: Rng,
  kinds: string[],
  modulus: number,
  stopOnFirst: boolean,
): GameEvent[] {
  const messages: GameEvent[] = [];
  for (const spec of catalog) {
    if (!kinds.includes(spec.type)) continue;
    if (!eventAllowed(state, spec)) continue;
    const freq = spec.weight || spec.freq || 0;
    if (!roll(rng, modulus, freq)) continue;
    let chunk: GameEvent[] = [];
    if (spec.type === "price" || spec.type === "goods") chunk = applyCommercial(state, spec, rng);
    else if (spec.type === "health") chunk = applyHealth(state, spec);
    else if (spec.type === "cash" || spec.type === "bank") chunk = applyCashOrBank(state, spec);
    else if (spec.type === "story") {
      chunk = [
        event(spec.id, "story", spec.text, {
          speaker: spec.speaker || "chief",
          sfx: spec.sfx,
          sprite: spec.sprite,
          bg: spec.bg,
        }),
      ];
    }
    if (chunk.length) {
      markSeen(state, spec);
      messages.push(...chunk);
      if (stopOnFirst) break;
      if (chunk.some((m) => m.id === "house_full")) break;
    }
  }
  return messages;
}

function maybeHospital(state: GameState, rng: Rng): GameEvent[] {
  if (state.health >= 85 || state.days_left <= 3) return [];
  const delay = 1 + rng.randrange(2);
  const loc = LOC_BY_ID[state.location]?.name || "北京";
  const spot = HOSPITAL_SPOTS[rng.randrange(HOSPITAL_SPOTS.length)];
  const load = delay * (1000 + rng.randrange(8500));
  state.debt += load;
  state.health += 10;
  clampHealth(state);
  state.days_left -= delay;
  if (state.days_left < 0) state.days_left = 0;
  return [
    event("forced_hospital", "system", `好心的市民把我抬到医院，医生让我治疗${delay}天。`, {
      speaker: "doctor",
    }),
    event("forced_hospital_2", "system", `由于不注意身体,我被人发现昏迷在${loc}附近的${spot}。`, {
      speaker: "me",
    }),
    event("forced_hospital_3", "system", `村长让人为我垫付了住院费用${load}元。`, { speaker: "chief" }),
  ];
}

function maybeHacker(state: GameState, rng: Rng): GameEvent[] {
  if (!state.hacker) return [];
  if (rng.randrange(1000) % 25 !== 0) return [];
  if (state.bank < 1000) return [];
  let num: number;
  let text: string;
  if (state.bank > 100000) {
    num = Math.trunc(state.bank / (2 + rng.randrange(20)));
    if (rng.randrange(20) % 3 !== 0) {
      state.bank -= num;
      text = `黑客入侵银行网络，疯狂修改数据库，我的存款减少了${num}`;
    } else {
      state.bank += num;
      text = `黑客入侵银行网络，疯狂修改数据库，我的存款增加了${num}`;
    }
  } else {
    num = Math.trunc(state.bank / (1 + rng.randrange(15)));
    state.bank += num;
    text = `黑客入侵银行网络，疯狂修改数据库，我的存款增加了${num}`;
  }
  return [event("hacker", "bank", text, { speaker: "news" })];
}

function forceSellAll(state: GameState): [string[], number] {
  let gained = 0;
  const names: string[] = [];
  for (const gid of GOODS_ORDER) {
    const qty = state.inventory[gid];
    if (qty <= 0) continue;
    gained += qty * (state.prices[gid] || 0);
    names.push(GOODS_BY_ID[gid].name);
    state.inventory[gid] = 0;
  }
  state.cash += gained;
  state.total_goods = 0;
  return [names, gained];
}

function storyBeats(state: GameState, catalog: EventSpec[]): GameEvent[] {
  const messages: GameEvent[] = [];
  const day = TOTAL_DAYS - state.days_left;
  for (const spec of catalog) {
    if (spec.type !== "story") continue;
    const cond = spec.conditions || {};
    if (cond.exact_day == null) continue;
    if (day !== Number(cond.exact_day)) continue;
    if (!eventAllowed(state, spec)) continue;
    const extra = spec.variants || [];
    let text = spec.text;
    let speaker = spec.speaker || "chief";
    if (extra.length) {
      if (state.debt >= 20000) {
        text = extra[0].text || text;
        speaker = extra[0].speaker || speaker;
      } else if (state.debt === 0 && extra.length > 1) {
        text = extra[1].text || text;
        speaker = extra[1].speaker || speaker;
      }
    }
    messages.push(event(spec.id, "story", text, { speaker, sprite: spec.sprite }));
    markSeen(state, spec);
  }
  return messages;
}

export function moveTo(
  state: GameState,
  locationId: LocId,
  rng: Rng,
  catalog: EventSpec[],
): GameEvent[] {
  const messages: GameEvent[] = [];
  if (!LOC_BY_ID[locationId]) return messages;
  if (locationId === state.location && state.day_index > 0) return messages;
  state.location = locationId;
  refreshPrices(state, rng);
  applyInterest(state);
  const flavor = LOCATION_FLAVOR[locationId];
  if (flavor) messages.push(event("flavor", "flavor", flavor, { speaker: "me" }));
  messages.push(...storyBeats(state, catalog));
  messages.push(...runCatalog(state, catalog, rng, ["price", "goods"], 950, false));
  messages.push(...runCatalog(state, catalog, rng, ["health"], 1000, true));
  const hospital = maybeHospital(state, rng);
  if (hospital.length) messages.push(...hospital);
  else {
    if (state.health > 0 && state.health < 20) {
      messages.push(event("health_warn", "system", "俺的健康..健康危机..快去医..", { speaker: "me" }));
    }
    if (state.health < 0) {
      state.dead = true;
      messages.push(
        event("death", "ending", "俺倒在街头,身边日记本上写着：“北京，我将再来!”", {
          speaker: "me",
          sfx: "death.wav",
        }),
      );
      return messages;
    }
  }
  messages.push(...runCatalog(state, catalog, rng, ["cash", "bank"], 1000, true));
  messages.push(...maybeHacker(state, rng));
  if (state.debt > DEBT_PUNISH_THRESHOLD) {
    state.health -= DEBT_PUNISH_HEALTH;
    messages.push(
      event("debt_thugs", "health", "俺欠钱太多，村长叫一群老乡揍了俺一顿!", {
        speaker: "chief",
        sfx: "kill.wav",
      }),
    );
    if (state.health < 0) {
      state.dead = true;
      messages.push(
        event("death", "ending", "俺倒在街头,身边日记本上写着：“北京，我将再来!”", {
          speaker: "me",
          sfx: "death.wav",
        }),
      );
      return messages;
    }
  }
  tickCooldowns(state);
  state.days_left -= 1;
  state.day_index = TOTAL_DAYS - state.days_left;
  if (state.cash < 0) state.cash = 0;
  if (state.days_left === 1) {
    messages.push(event("tomorrow_home", "story", "俺明天回家乡，快把全部货物卖掉。", { speaker: "me" }));
  }
  if (state.days_left <= 0) {
    const [names, gained] = forceSellAll(state);
    messages.push(event("day40", "story", "俺已经在北京40天了，该回去结婚去了。", { speaker: "me" }));
    if (names.length) {
      messages.push(
        event("autosell", "system", `系统替我卖了剩余货物: ${names.join("、")}。换得${gained}元。`, {
          speaker: "news",
        }),
      );
    }
    state.game_over = true;
  }
  state.last_events = messages.map((m) => m.id);
  state.total_goods = totalGoods(state);
  return messages;
}

export function reset(rng: Rng): GameState {
  const state = newState();
  refreshPrices(state, rng);
  return state;
}

export function endingRank(state: GameState): [string, string, number] {
  const s = score(state);
  if (state.dead) return ["death", "倒在北京街头", s];
  if (s < 0) return ["broke", "两手空空回乡", s];
  if (s < 50000) return ["ok", "还清债务，勉强回家结婚", s];
  if (s < 500000) return ["rich", "荣登北京小富人榜", s];
  return ["tycoon", "北京富人排行榜前列", s];
}

export function locBg(state: GameState): string {
  return `bg ${LOC_BY_ID[state.location]?.bg || "market_station"}.png`;
}
