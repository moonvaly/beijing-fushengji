import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  buy,
  endingRank,
  heal,
  maxBuy,
  moveTo,
  newState,
  rentHouse,
  reset,
  SeededRng,
  sell,
  visitWangba,
  type EventSpec,
  type GoodId,
} from "../src/sim/sim";

const catalog: EventSpec[] = JSON.parse(
  readFileSync(
    join(dirname(fileURLToPath(import.meta.url)), "../../beijing_fushengji/game/engine/events.json"),
    "utf8",
  ),
);

describe("sim", () => {
  it("buy sell and capacity", () => {
    const rng = new SeededRng(1);
    const st = reset(rng);
    const gid = (Object.keys(st.prices) as GoodId[]).find(
      (g) => st.prices[g] > 0 && st.prices[g] <= st.cash,
    );
    expect(gid).toBeTruthy();
    const before = st.cash;
    const price = st.prices[gid!];
    buy(st, gid!, 1);
    expect(st.inventory[gid!]).toBe(1);
    expect(st.cash).toBe(before - price);
    sell(st, gid!, 1);
    expect(st.inventory[gid!]).toBe(0);
    expect(st.cash).toBe(before);
  });

  it("cannot buy missing or unaffordable", () => {
    const st = newState();
    st.prices.CAR = 0;
    const msgs = buy(st, "CAR", 1);
    expect(st.inventory.CAR).toBe(0);
    expect(msgs[0]?.id).toBe("no_market");
    st.prices.CAR = 20000;
    st.cash = 100;
    buy(st, "CAR", 1);
    expect(st.inventory.CAR).toBe(0);
    expect(maxBuy(st, "CAR")).toBe(0);
  });

  it("fame on contraband", () => {
    const st = newState();
    st.prices.BABY = 100;
    st.inventory.BABY = 2;
    st.cash = 0;
    const msgs = sell(st, "BABY", 2);
    expect(st.fame).toBe(93);
    expect(msgs.some((m) => m.id === "bad_fame_baby")).toBe(true);
    st.prices.ALCOHOL = 100;
    st.inventory.ALCOHOL = 1;
    sell(st, "ALCOHOL", 1);
    expect(st.fame).toBe(83);
  });

  it("interest and move decrements day", () => {
    const rng = new SeededRng(2);
    const st = reset(rng);
    st.debt = 5000;
    st.bank = 1000;
    st.cash = 10000;
    moveTo(st, "xizhimen", rng, catalog);
    expect(st.location).toBe("xizhimen");
    expect(st.days_left).toBe(39);
    expect(st.debt).toBe(5500);
    expect(st.bank).toBe(1010);
  });

  it("forced sell on day 40", () => {
    const rng = new SeededRng(3);
    const st = reset(rng);
    st.days_left = 1;
    st.inventory.CD = 10;
    st.prices.CD = 20;
    st.cash = 0;
    const msgs = moveTo(st, "dongzhimen", rng, catalog);
    expect(st.game_over).toBe(true);
    expect(st.inventory.CD).toBe(0);
    expect(msgs.some((m) => m.id === "day40")).toBe(true);
    expect(st.total_goods).toBe(0);
  });

  it("hospital and death paths", () => {
    const st = newState();
    expect(heal(st, 1).some((m) => m.id === "hospital_ok")).toBe(true);
    st.health = 90;
    st.cash = 0;
    expect(heal(st, 1).some((m) => m.id === "hospital_broke")).toBe(true);
    st.cash = 35000;
    heal(st, 10);
    expect(st.health).toBe(100);
    st.health = -1;
    st.days_left = 2;
    const msgs = moveTo(st, "fangzhuang", new SeededRng(0), catalog);
    expect(st.dead || msgs.some((m) => m.id === "death") || st.health >= 0).toBe(true);
  });

  it("house and wangba", () => {
    const st = newState();
    st.cash = 1000;
    expect(rentHouse(st).some((m) => m.id === "house_broke")).toBe(true);
    st.cash = 40000;
    rentHouse(st);
    expect(st.capacity).toBe(110);
    const rng = new SeededRng(4);
    st.cash = 20;
    visitWangba(st, rng);
    visitWangba(st, rng);
    visitWangba(st, rng);
    expect(visitWangba(st, rng).some((m) => m.id === "wangba_ban")).toBe(true);
  });

  it("story beats fire once", () => {
    const rng = new SeededRng(5);
    const st = reset(rng);
    st.days_left = 30;
    const msgs = moveTo(st, "gongzhufen", rng, catalog);
    expect(msgs.some((m) => m.id === "beat_day10")).toBe(true);
    st.days_left = 30;
    st.location = "beijingzhan";
    const msgs2 = moveTo(st, "gongzhufen", rng, catalog);
    expect(msgs2.some((m) => m.id === "beat_day10")).toBe(false);
  });

  it("ending rank", () => {
    const dead = newState();
    dead.dead = true;
    expect(endingRank(dead)[0]).toBe("death");
    const broke = newState();
    broke.cash = 100;
    broke.bank = 0;
    broke.debt = 5000;
    expect(endingRank(broke)[0]).toBe("broke");
  });
});
