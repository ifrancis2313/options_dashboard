import math

import pytest

import analysis
from bs_pricer import bs_call, bs_put
from implied_vol import implied_vol


REFERENCE_CASE = (42, 40, 0.5, 0.10, 0.20)


def test_black_scholes_matches_hull_reference_case():
    call = bs_call(*REFERENCE_CASE)
    put = bs_put(*REFERENCE_CASE)

    assert call == pytest.approx(4.76, abs=0.01)
    assert put == pytest.approx(0.81, abs=0.01)


def test_put_call_parity():
    S, K, T, r, sigma = REFERENCE_CASE

    assert bs_call(S, K, T, r, sigma) - bs_put(S, K, T, r, sigma) == pytest.approx(
        S - K * math.exp(-r * T)
    )


def test_implied_volatility_round_trip():
    S, K, T, r, sigma = REFERENCE_CASE
    market_price = bs_call(S, K, T, r, sigma)

    assert implied_vol(S, K, T, r, market_price) == pytest.approx(sigma)


def test_pnl_heatmap_nets_entry_premium_and_flips_sign_for_short(monkeypatch):
    monkeypatch.setattr(analysis.plt, "show", lambda: None)
    monkeypatch.setattr(analysis.plt, "savefig", lambda *args, **kwargs: None)
    S, K, T, r, sigma = REFERENCE_CASE
    entry_premium = bs_call(S, K, T, r, sigma)

    long = analysis.pnl_heatmap(
        K, r, sigma, stock_prices=[S, 50], days=[182.5], entry_spot=S
    )
    short = analysis.pnl_heatmap(
        K,
        r,
        sigma,
        stock_prices=[S, 50],
        days=[182.5],
        entry_premium=entry_premium,
        position="short",
    )

    assert long.loc[S, "182.5d"] == 0
    assert long.loc[50, "182.5d"] > 0
    assert short.loc[S, "182.5d"] == 0
    assert short.loc[50, "182.5d"] < 0
    analysis.plt.close("all")
