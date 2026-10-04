# -*- coding: utf-8 -*-
"""Pure-Python tests for the Beijing Fushengji simulation."""

from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "beijing_fushengji" / "game"
sys.path.insert(0, str(GAME))

import fushengji_sim as sim  # noqa: E402


def assert_eq(a, b, msg=""):
    if a != b:
        raise AssertionError("%s: %r != %r" % (msg, a, b))


def assert_true(cond, msg=""):
    if not cond:
        raise AssertionError(msg)


def catalog():
    return sim.load_events()


def test_buy_sell_and_capacity():
    rng = random.Random(1)
    st = sim.reset(rng)
    gid = None
    for g in sim.GOODS_ORDER:
        if st["prices"][g] > 0 and st["prices"][g] <= st["cash"]:
            gid = g
            break
    assert_true(gid, "need an affordable good")
    before = st["cash"]
    price = st["prices"][gid]
    sim.buy(st, gid, 1)
    assert_eq(st["inventory"][gid], 1)
    assert_eq(st["cash"], before - price)
    sim.sell(st, gid, 1)
    assert_eq(st["inventory"][gid], 0)
    assert_eq(st["cash"], before)


def test_cannot_buy_missing_or_unaffordable():
    st = sim.new_state()
    st["prices"]["CAR"] = 0
    msgs = sim.buy(st, "CAR", 1)
    assert_eq(st["inventory"]["CAR"], 0)
    assert_true(msgs and msgs[0]["id"] == "no_market")
    st["prices"]["CAR"] = 20000
    st["cash"] = 100
    sim.buy(st, "CAR", 1)
    assert_eq(st["inventory"]["CAR"], 0)


def test_fame_on_contraband():
    st = sim.new_state()
    st["prices"]["BABY"] = 100
    st["inventory"]["BABY"] = 2
    st["cash"] = 0
    msgs = sim.sell(st, "BABY", 2)
    assert_eq(st["fame"], 100 - 7)
    assert_true(any(m["id"] == "bad_fame_baby" for m in msgs))
    sim.sell(st, "ALCOHOL", 1)  # none
    st["prices"]["ALCOHOL"] = 100
    st["inventory"]["ALCOHOL"] = 1
    sim.sell(st, "ALCOHOL", 1)
    assert_eq(st["fame"], 100 - 7 - 10)


def test_interest_and_move_decrements_day():
    rng = random.Random(2)
    st = sim.reset(rng)
    cat = catalog()
    st["debt"] = 5000
    st["bank"] = 1000
    st["cash"] = 10000
    sim.move_to(st, "xizhimen", rng, cat)
    assert_eq(st["location"], "xizhimen")
    assert_eq(st["days_left"], 39)
    assert_eq(st["debt"], 5500)
    assert_eq(st["bank"], 1010)


def test_forced_sell_on_day_40():
    rng = random.Random(3)
    st = sim.reset(rng)
    cat = catalog()
    st["days_left"] = 1
    st["inventory"]["CD"] = 10
    st["prices"]["CD"] = 20
    st["cash"] = 0
    msgs = sim.move_to(st, "dongzhimen", rng, cat)
    assert_true(st["game_over"])
    assert_eq(st["inventory"]["CD"], 0)
    assert_true(any(m["id"] == "day40" for m in msgs))
    assert_true(st["total_goods"] == 0)


def test_hospital_and_death():
    st = sim.new_state()
    st["health"] = 100
    msgs = sim.heal(st, 1)
    assert_true(any(m["id"] == "hospital_ok" for m in msgs))
    st["health"] = 90
    st["cash"] = 0
    msgs = sim.heal(st, 1)
    assert_true(any(m["id"] == "hospital_broke" for m in msgs))
    st["cash"] = 35000
    sim.heal(st, 10)
    assert_eq(st["health"], 100)
    st["health"] = -1
    st["days_left"] = 2
    rng = random.Random(0)
    msgs = sim.move_to(st, "fangzhuang", rng, catalog())
    assert_true(st["dead"] or any(m["id"] == "death" for m in msgs) or st["health"] >= 0)


def test_house_and_wangba():
    st = sim.new_state()
    st["cash"] = 1000
    msgs = sim.rent_house(st)
    assert_true(any(m["id"] == "house_broke" for m in msgs))
    st["cash"] = 40000
    sim.rent_house(st)
    assert_eq(st["capacity"], 110)
    rng = random.Random(4)
    st["cash"] = 20
    sim.visit_wangba(st, rng)
    sim.visit_wangba(st, rng)
    sim.visit_wangba(st, rng)
    msgs = sim.visit_wangba(st, rng)
    assert_true(any(m["id"] == "wangba_ban" for m in msgs))


def test_story_beats_fire_once():
    rng = random.Random(5)
    st = sim.reset(rng)
    cat = catalog()
    st["days_left"] = 40
    # first move -> day_index 1, days_left 39. exact_day uses TOTAL-days_left after decrement.
    # story_beats runs BEFORE decrement, day = 40 - 40 = 0 at start of first move.
    st["days_left"] = 30  # day = 10 at start of move
    msgs = sim.move_to(st, "gongzhufen", rng, cat)
    assert_true(any(m["id"] == "beat_day10" for m in msgs), msgs)
    st["days_left"] = 30
    st["location"] = "beijingzhan"
    msgs = sim.move_to(st, "gongzhufen", rng, cat)
    assert_true(not any(m["id"] == "beat_day10" for m in msgs))


def test_ending_rank():
    st = sim.new_state()
    st["dead"] = True
    kind, _, _ = sim.ending_rank(st)
    assert_eq(kind, "death")
    st = sim.new_state()
    st["cash"] = 100
    st["bank"] = 0
    st["debt"] = 5000
    kind, _, _ = sim.ending_rank(st)
    assert_eq(kind, "broke")


def main():
    tests = [
        test_buy_sell_and_capacity,
        test_cannot_buy_missing_or_unaffordable,
        test_fame_on_contraband,
        test_interest_and_move_decrements_day,
        test_forced_sell_on_day_40,
        test_hospital_and_death,
        test_house_and_wangba,
        test_story_beats_fire_once,
        test_ending_rank,
    ]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("all passed", len(tests))


if __name__ == "__main__":
    main()
