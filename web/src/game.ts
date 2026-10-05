import { NPC_SPRITE } from "./assets";
import {
  buy,
  deposit,
  endingRank,
  GOODS_BY_ID,
  heal,
  locBg,
  LOC_BY_ID,
  maxBuy,
  moveTo,
  nativeRng,
  postNoDebtLine,
  repayDebt,
  rentHouse,
  reset,
  sell,
  visitWangba,
  withdraw,
  type EventSpec,
  type GameEvent,
  type GameState,
  type GoodId,
  type LocId,
} from "./sim/sim";
import * as ui from "./ui";

const SAVE_KEY = "beijing-fushengji-save-v1";

type Line = { speaker: string; text: string; npc?: string | null; sfx?: string; then?: () => void };

export class Game {
  state!: GameState;
  catalog: EventSpec[] = [];
  queue: Line[] = [];
  stallGid: GoodId | null = null;

  async start() {
    const base = import.meta.env.BASE_URL;
    const res = await fetch(base + "events.json");
    this.catalog = await res.json();
    this.bindTitle();
    ui.setBg("bg market_station.png");
    ui.els.title.style.backgroundImage = `linear-gradient(#0000, #120e0acc 55%), url("${base}main_menu.png")`;
    ui.els.title.style.backgroundSize = "cover";
    ui.els.title.hidden = false;
    const cont = document.getElementById("btn-continue") as HTMLButtonElement;
    cont.hidden = !localStorage.getItem(SAVE_KEY);
  }

  bindTitle() {
    document.getElementById("btn-start")!.onclick = () => {
      this.state = reset(nativeRng());
      this.save();
      this.beginIntro();
    };
    document.getElementById("btn-continue")!.onclick = () => {
      const raw = localStorage.getItem(SAVE_KEY);
      if (!raw) return;
      this.state = JSON.parse(raw);
      ui.els.title.hidden = true;
      this.locationMenu();
    };
    document.getElementById("btn-about")!.onclick = () => {
      ui.showDialogue(
        "news",
        "《北京浮生记》。原作郭祥昊（2000–2001，GPL-2.0）。本页为 Ren'Py 移植的网页版。",
        () => {
          ui.hideDialogue();
          ui.els.title.hidden = false;
        },
      );
      ui.els.title.hidden = true;
    };
  }

  save() {
    localStorage.setItem(SAVE_KEY, JSON.stringify(this.state));
  }

  beginIntro() {
    ui.els.title.hidden = true;
    ui.setBg("bg market_station.png");
    ui.setHero(true);
    ui.setNpc(null);
    ui.showHud(this.state);
    this.playLines(
      [
        { speaker: "me", text: "一九九八年。俺从村里来北京，口袋里两千块，肩上压着村长的五千块债。" },
        { speaker: "me", text: "利息一天一分。四十天内还不完，老乡就会来北京找俺。" },
        {
          speaker: "chief",
          text: "铁牛，听清楚。五千块，四十天。别在城里花天酒地。",
          npc: NPC_SPRITE.chief,
        },
        { speaker: "me", text: "房子只能塞一百件货。倒什么、去哪儿，都写在这一页北京里。" },
      ],
      () => this.locationMenu(),
    );
  }

  playLines(lines: Line[], done: () => void) {
    this.queue = [...lines];
    const next = () => {
      const line = this.queue.shift();
      if (!line) {
        ui.hideDialogue();
        done();
        return;
      }
      if (line.npc) ui.setNpc(line.npc);
      else if (line.speaker === "me" || line.speaker === "news") ui.setNpc(null);
      else if (NPC_SPRITE[line.speaker]) ui.setNpc(NPC_SPRITE[line.speaker]);
      ui.playSfx(line.sfx);
      ui.showDialogue(line.speaker, line.text, next);
    };
    next();
  }

  playEvents(evs: GameEvent[], done: () => void) {
    this.playLines(
      evs.map((ev) => ({
        speaker: ev.speaker,
        text: ev.text,
        sfx: ev.sfx,
        npc: NPC_SPRITE[ev.speaker],
      })),
      done,
    );
  }

  scenePlace() {
    ui.setBg(locBg(this.state));
    ui.setHero(true);
    ui.setNpc(null);
    ui.setProp(null);
    ui.showHud(this.state);
    ui.hideOverlay();
    ui.hideChoices();
  }

  locationMenu() {
    if (this.state.dead || this.state.game_over) {
      this.ending();
      return;
    }
    this.save();
    this.scenePlace();
    const name = LOC_BY_ID[this.state.location].name;
    ui.showChoices(`人在${name}，风沙还没停。俺要——`, [
      { label: "去货摊看看今天卖什么。", run: () => this.stall() },
      { label: "换个黑市，过一天。", run: () => this.travel() },
      { label: "去银行。", run: () => this.bank() },
      { label: "去医院。", run: () => this.hospital() },
      { label: "去邮局给村长汇钱。", run: () => this.post() },
      { label: "钻进网吧。", run: () => this.wangba() },
      { label: "找租房中介。", run: () => this.house() },
      { label: "翻翻口袋和日记。", run: () => this.diary() },
    ]);
  }

  stall() {
    this.scenePlace();
    this.playLines([{ speaker: "me", text: "摊主把报纸盖在货上，只露出一个角。价码一天一个样。" }], () => {
      ui.showStall(
        this.state,
        (gid) => this.stallTalk(gid),
        () => this.locationMenu(),
      );
    });
  }

  stallTalk(gid: GoodId) {
    this.stallGid = gid;
    const gname = GOODS_BY_ID[gid].name;
    const price = this.state.prices[gid];
    const have = this.state.inventory[gid];
    ui.hideOverlay();
    ui.setProp(GOODS_BY_ID[gid] ? `${gid}` : null);
    ui.setProp(
      (
        {
          CIGARETTE: "good cigarette.png",
          CAR: "good car.png",
          CD: "good cd.png",
          ALCOHOL: "good alcohol.png",
          BABY: "good baby.png",
          TOY: "good toy.png",
          PHONES: "good phones.png",
          COSMETIC: "good cosmetic.png",
        } as Record<GoodId, string>
      )[gid],
    );
    const canBuy = maxBuy(this.state, gid) > 0;
    if (price > 0 && have > 0) {
      this.playLines(
        [{ speaker: "stallkeep", text: `${gname}，今天 ${price} 元一件。你口袋里还有 ${have} 件。` }],
        () => {
          ui.showChoices("", [
            { label: "买一点。", disabled: !canBuy, run: () => this.stallBuy() },
            { label: "出手。", run: () => this.stallSell() },
            { label: "再看看。", run: () => this.stall() },
          ]);
        },
      );
    } else if (price > 0) {
      this.playLines([{ speaker: "stallkeep", text: `${gname}，${price} 元。要不要？` }], () => {
        ui.showChoices("", [
          { label: "还价，买。", disabled: !canBuy, run: () => this.stallBuy() },
          { label: "兜里空，走了。", run: () => this.stall() },
        ]);
      });
    } else {
      const lines: Line[] = [{ speaker: "stallkeep", text: `这地方今儿没人收 ${gname}。` }];
      if (have > 0) lines.push({ speaker: "me", text: `口袋里还压着 ${have} 件，只能等到有市再抛。` });
      this.playLines(lines, () => this.stall());
    }
  }

  stallBuy() {
    const gid = this.stallGid!;
    const mx = maxBuy(this.state, gid);
    if (mx <= 0) {
      this.playLines([{ speaker: "me", text: "钱不够，或者屋子满了。" }], () => this.stall());
      return;
    }
    const gname = GOODS_BY_ID[gid].name;
    const price = this.state.prices[gid];
    ui.showQty(`买多少件${gname}？每件 ${price} 元。`, mx, (n) => {
      ui.hideOverlay();
      if (!n) {
        this.stall();
        return;
      }
      const evs = buy(this.state, gid, n);
      ui.playSfx("buy.wav");
      this.playLines([{ speaker: "stallkeep", text: "成交。拿走吧。" }, ...evs.map(toLine)], () => {
        this.save();
        this.stall();
      });
    });
  }

  stallSell() {
    const gid = this.stallGid!;
    const have = this.state.inventory[gid];
    const price = this.state.prices[gid];
    if (have <= 0 || price <= 0) {
      this.stall();
      return;
    }
    ui.showQty(`抛出多少件${GOODS_BY_ID[gid].name}？`, have, (n) => {
      ui.hideOverlay();
      if (!n) {
        this.stall();
        return;
      }
      const evs = sell(this.state, gid, n);
      ui.playSfx("money.wav");
      this.playLines([{ speaker: "stallkeep", text: "货我收下了。" }, ...evs.map(toLine)], () => {
        this.save();
        this.stall();
      });
    });
  }

  travel() {
    ui.setBg("bg map_beijing.png");
    ui.setHero(true);
    ui.setNpc(null);
    ui.setProp(null);
    this.playLines([{ speaker: "me", text: "北京城那么大。下一站去哪儿？" }], () => {
      ui.showMap(
        this.state,
        (id) => this.go(id),
        () => this.locationMenu(),
      );
    });
  }

  go(dest: LocId) {
    ui.hideOverlay();
    const destName = LOC_BY_ID[dest].name;
    ui.playSfx("shutdoor.wav");
    ui.setBg(null);
    this.playLines([{ speaker: "me", text: `俺挤上地铁，去${destName}。一天又过去了。` }], () => {
      const evs = moveTo(this.state, dest, nativeRng(), this.catalog);
      this.save();
      ui.setBg(locBg(this.state));
      ui.setHero(true);
      this.playEvents(evs, () => this.locationMenu());
    });
  }

  bank() {
    ui.setBg("bg bank.png");
    ui.setHero(true);
    ui.setNpc(NPC_SPRITE.teller);
    ui.playSfx("opendoor.wav");
    const cash = this.state.cash;
    const bank = this.state.bank;
    this.playLines(
      [{ speaker: "teller", text: `客户您好。现金 ${cash} 元，存款 ${bank} 元。请问您要……` }],
      () => {
        ui.showChoices("", [
          {
            label: "把钱存进去。",
            disabled: this.state.cash <= 0,
            run: () => {
              ui.showQty("存多少？", this.state.cash, (n) => {
                ui.hideOverlay();
                if (n) {
                  deposit(this.state, n);
                  this.save();
                  this.playLines([{ speaker: "teller", text: "已经入账。您慢走。" }], () =>
                    this.locationMenu(),
                  );
                } else this.locationMenu();
              });
            },
          },
          {
            label: "把钱取出来。",
            disabled: this.state.bank <= 0,
            run: () => {
              ui.showQty("取多少？", this.state.bank, (n) => {
                ui.hideOverlay();
                if (n) {
                  withdraw(this.state, n);
                  this.save();
                  this.playLines([{ speaker: "teller", text: "给您。点清楚。" }], () => this.locationMenu());
                } else this.locationMenu();
              });
            },
          },
          {
            label: "走错了。",
            run: () =>
              this.playLines([{ speaker: "teller", text: "下一个。" }], () => this.locationMenu()),
          },
        ]);
      },
    );
  }

  hospital() {
    ui.setBg("bg hospital.png");
    ui.setHero(true);
    ui.playSfx("opendoor.wav");
    const need = 100 - this.state.health;
    const hp = this.state.health;
    if (need <= 0) {
      ui.setNpc(NPC_SPRITE.nurse);
      this.playEvents(heal(this.state, 0), () => this.locationMenu());
      return;
    }
    ui.setNpc(NPC_SPRITE.doctor);
    this.playLines(
      [{ speaker: "doctor", text: `您的健康是 ${hp} 点，还差 ${need} 点。一点三千五。` }],
      () => {
        ui.showChoices("", [
          {
            label: "治。",
            disabled: this.state.cash < 3500,
            run: () => {
              ui.showQty("治几点？每点三千五。", need, (pts) => {
                ui.hideOverlay();
                if (pts) this.playEvents(heal(this.state, pts), () => { this.save(); this.locationMenu(); });
                else this.locationMenu();
              });
            },
          },
          {
            label: "没钱，走。",
            run: () =>
              this.playLines([{ speaker: "doctor", text: "下次早点来。" }], () => this.locationMenu()),
          },
        ]);
      },
    );
  }

  post() {
    ui.setBg("bg post.png");
    ui.setHero(true);
    ui.setNpc(NPC_SPRITE.chief);
    ui.playSfx("opendoor.wav");
    if (this.state.debt <= 0) {
      this.playLines([{ speaker: "chief", text: postNoDebtLine(this.state) }], () => this.locationMenu());
      return;
    }
    const d = this.state.debt;
    this.playLines([{ speaker: "chief", text: `铁牛，你欠俺 ${d} 元，快还！` }], () => {
      ui.showChoices("", [
        {
          label: "汇出去。",
          disabled: this.state.cash <= 0,
          run: () => {
            ui.showQty("汇多少给村长？", Math.min(this.state.cash, this.state.debt), (amt) => {
              ui.hideOverlay();
              if (amt) {
                const evs = repayDebt(this.state, amt);
                this.save();
                this.playEvents(evs.length ? evs : [{ id: "ok", type: "system", text: "汇出去了。", speaker: "me" }], () =>
                  this.locationMenu(),
                );
              } else this.locationMenu();
            });
          },
        },
        {
          label: "挂了。",
          run: () =>
            this.playLines([{ speaker: "chief", text: "利息可没睡着。" }], () => this.locationMenu()),
        },
      ]);
    });
  }

  wangba() {
    ui.setBg("bg wangba.png");
    ui.setHero(true);
    ui.setNpc(NPC_SPRITE.netbar);
    ui.playSfx("opendoor.wav");
    this.playEvents(visitWangba(this.state, nativeRng()), () => {
      this.save();
      this.locationMenu();
    });
  }

  house() {
    ui.setBg("bg house.png");
    ui.setHero(true);
    ui.setNpc(NPC_SPRITE.agent);
    ui.playSfx("opendoor.wav");
    this.playEvents(rentHouse(this.state), () => {
      this.save();
      this.locationMenu();
    });
  }

  diary() {
    ui.showDiary(this.state, () => this.locationMenu());
  }

  ending() {
    ui.showHud(null);
    ui.hideChoices();
    ui.hideOverlay();
    const [kind, title, sc] = endingRank(this.state);
    if (kind === "death") {
      ui.setBg("bg ending_death.png");
      ui.setHero(false);
      ui.setNpc(null);
      ui.playSfx("death.wav");
      this.playLines(
        [
          { speaker: "me", text: "俺倒在街头。日记本最后一页写着：北京，我将再来。" },
          { speaker: "news", text: "《北京浮生记》。原作郭祥昊，GPL-2.0。" },
        ],
        () => this.backToTitle(),
      );
    } else {
      ui.setBg("bg ending_home.png");
      ui.setHero(true);
      ui.setNpc(null);
      this.playLines(
        [
          { speaker: "me", text: `四十天到了。现金加存款减去负债，还剩 ${sc} 元。` },
          { speaker: "me", text: `这就是俺在北京的分数。${title}` },
          { speaker: "me", text: `健康 ${this.state.health}，名声 ${this.state.fame}。该回家了。` },
          { speaker: "news", text: "《北京浮生记》。原作郭祥昊，GPL-2.0。" },
        ],
        () => this.backToTitle(),
      );
    }
    localStorage.removeItem(SAVE_KEY);
  }

  backToTitle() {
    ui.hideDialogue();
    ui.setHero(false);
    ui.setNpc(null);
    ui.showHud(null);
    ui.els.title.hidden = false;
    (document.getElementById("btn-continue") as HTMLButtonElement).hidden = !localStorage.getItem(SAVE_KEY);
  }
}

function toLine(ev: GameEvent): Line {
  return { speaker: ev.speaker, text: ev.text, sfx: ev.sfx, npc: NPC_SPRITE[ev.speaker] };
}
