import { audioFile, imageFile, SPEAKER_NAME } from "./assets";
import {
  GOODS,
  GOOD_IMAGE,
  LOC_BY_ID,
  MAP_GROUPS,
  type GameState,
  type GoodId,
  type LocId,
} from "./sim/sim";

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

export const els = {
  bg: $<HTMLImageElement>("bg"),
  hero: $<HTMLImageElement>("hero"),
  npc: $<HTMLImageElement>("npc"),
  prop: $<HTMLImageElement>("prop"),
  hud: $("hud"),
  overlay: $("overlay"),
  choices: $("choices"),
  dialogue: $<HTMLButtonElement>("dialogue"),
  speaker: $("speaker"),
  line: $("line"),
  title: $("title"),
};

export function setBg(file: string | null) {
  if (!file) {
    els.bg.hidden = true;
    els.bg.removeAttribute("src");
    return;
  }
  els.bg.hidden = false;
  els.bg.src = imageFile(file);
}

export function setHero(on: boolean) {
  els.hero.hidden = !on;
  if (on) els.hero.src = imageFile("hero normal.png");
}

export function setNpc(file: string | null) {
  if (!file) {
    els.npc.hidden = true;
    els.npc.removeAttribute("src");
    return;
  }
  els.npc.hidden = false;
  els.npc.src = imageFile(file);
}

export function setProp(file: string | null) {
  if (!file) {
    els.prop.hidden = true;
    els.prop.removeAttribute("src");
    return;
  }
  els.prop.hidden = false;
  els.prop.src = imageFile(file);
}

export function playSfx(name: string | undefined) {
  if (!name) return;
  const a = new Audio(audioFile(name));
  a.play().catch(() => {});
}

export function showHud(state: GameState | null) {
  if (!state) {
    els.hud.hidden = true;
    return;
  }
  els.hud.hidden = false;
  const day = state.day_index + 1;
  const loc = LOC_BY_ID[state.location].name;
  els.hud.innerHTML = `<span>第 ${day} 天 / 40</span><span class="loc">${loc}</span><span>现金 ${state.cash}</span><span class="debt">债 ${state.debt}</span><span class="hp">健康 ${state.health}</span><span>名声 ${state.fame}</span>`;
}

export function showDialogue(speaker: string, text: string, onNext: () => void) {
  els.choices.hidden = true;
  els.overlay.hidden = true;
  els.dialogue.hidden = false;
  els.speaker.textContent = SPEAKER_NAME[speaker] || speaker;
  els.line.textContent = text;
  els.dialogue.onclick = onNext;
  els.dialogue.focus();
}

export function hideDialogue() {
  els.dialogue.hidden = true;
}

export type Choice = { label: string; disabled?: boolean; run: () => void };

export function showChoices(caption: string, items: Choice[]) {
  hideDialogue();
  els.overlay.hidden = true;
  els.choices.hidden = false;
  els.choices.innerHTML = "";
  if (caption) {
    const cap = document.createElement("div");
    cap.className = "caption";
    cap.textContent = caption;
    els.choices.append(cap);
  }
  for (const item of items) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = item.label;
    b.disabled = !!item.disabled;
    b.onclick = item.run;
    els.choices.append(b);
  }
}

export function hideChoices() {
  els.choices.hidden = true;
}

export function hideOverlay() {
  els.overlay.hidden = true;
  els.overlay.innerHTML = "";
}

export function showStall(state: GameState, onPick: (gid: GoodId) => void, onLeave: () => void) {
  els.choices.hidden = true;
  els.overlay.hidden = false;
  const cards = document.createElement("div");
  cards.className = "cards";
  for (const g of GOODS) {
    const price = state.prices[g.id];
    const have = state.inventory[g.id];
    if (price <= 0 && have <= 0) continue;
    const b = document.createElement("button");
    b.className = "card";
    b.innerHTML = `<img alt="" src="${imageFile(GOOD_IMAGE[g.id])}"><div>${g.name}</div><div>${price > 0 ? price + " 元" : "今日无市"}</div>${have ? `<div>口袋 ${have}</div>` : ""}`;
    b.onclick = () => onPick(g.id);
    cards.append(b);
  }
  const leave = document.createElement("button");
  leave.className = "chip";
  leave.textContent = "离开货摊";
  leave.onclick = onLeave;
  els.overlay.innerHTML = "";
  const panel = document.createElement("div");
  panel.className = "panel";
  panel.innerHTML = "<h2>摊上今天有这些。点一件，跟摊主谈。</h2>";
  panel.append(cards, leave);
  els.overlay.append(panel);
}

export function showMap(state: GameState, onPick: (id: LocId) => void, onCancel: () => void) {
  els.choices.hidden = true;
  els.overlay.hidden = false;
  const panel = document.createElement("div");
  panel.className = "panel";
  panel.innerHTML = "<h2>下一站去哪儿？出城就算过一天。</h2>";
  for (const [title, ids] of MAP_GROUPS) {
    const row = document.createElement("div");
    row.className = "map-row";
    const lab = document.createElement("span");
    lab.className = "lab";
    lab.textContent = title;
    row.append(lab);
    for (const id of ids) {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = LOC_BY_ID[id].name;
      b.disabled = id === state.location;
      b.onclick = () => onPick(id);
      row.append(b);
    }
    panel.append(row);
  }
  const cancel = document.createElement("button");
  cancel.className = "chip";
  cancel.textContent = "还是留下";
  cancel.onclick = onCancel;
  panel.append(cancel);
  els.overlay.innerHTML = "";
  els.overlay.append(panel);
}

export function showQty(prompt: string, maxn: number, onDone: (n: number) => void) {
  let n = maxn;
  els.choices.hidden = true;
  els.overlay.hidden = false;
  const panel = document.createElement("div");
  panel.className = "panel";
  const title = document.createElement("h2");
  title.textContent = prompt;
  const row = document.createElement("div");
  row.className = "qty-row";
  const val = document.createElement("span");
  const paint = () => {
    val.textContent = `${n} / ${maxn}`;
  };
  const mk = (label: string, fn: () => void) => {
    const b = document.createElement("button");
    b.className = "qty-btn";
    b.textContent = label;
    b.onclick = () => {
      fn();
      paint();
    };
    return b;
  };
  row.append(
    mk("−", () => {
      n = Math.max(0, n - 1);
    }),
    val,
    mk("+", () => {
      n = Math.min(maxn, n + 1);
    }),
    mk("全部", () => {
      n = maxn;
    }),
  );
  paint();
  const ok = document.createElement("button");
  ok.className = "chip";
  ok.textContent = "就这些";
  ok.onclick = () => onDone(n);
  const cancel = document.createElement("button");
  cancel.className = "chip";
  cancel.textContent = "算了";
  cancel.onclick = () => onDone(0);
  panel.append(title, row, ok, cancel);
  els.overlay.innerHTML = "";
  els.overlay.append(panel);
}

export function showDiary(state: GameState, onClose: () => void) {
  els.choices.hidden = true;
  els.overlay.hidden = false;
  const loc = LOC_BY_ID[state.location].name;
  const held = GOODS.filter((g) => state.inventory[g.id] > 0);
  const panel = document.createElement("div");
  panel.className = "panel";
  panel.innerHTML = `<h2>铁牛的日记</h2>
    <p>人在 ${loc}。还剩 ${state.days_left} 天。</p>
    <p>现金 ${state.cash}　存款 ${state.bank}　负债 ${state.debt}</p>
    <p>健康 ${state.health}　名声 ${state.fame}　屋子 ${state.total_goods}/${state.capacity}</p>
    <h2>口袋里的货</h2>`;
  if (!held.length) {
    const p = document.createElement("p");
    p.textContent = "空空如也。";
    panel.append(p);
  }
  for (const g of held) {
    const row = document.createElement("div");
    row.className = "map-row";
    row.innerHTML = `<img alt="" src="${imageFile(GOOD_IMAGE[g.id])}" style="width:48px;height:48px;object-fit:cover"> <span>${g.name} ×${state.inventory[g.id]}</span>`;
    panel.append(row);
  }
  const close = document.createElement("button");
  close.className = "chip";
  close.textContent = "合上日记";
  close.onclick = onClose;
  panel.append(close);
  els.overlay.innerHTML = "";
  els.overlay.append(panel);
}
