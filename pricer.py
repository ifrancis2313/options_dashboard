"""
pricer.py
---------
CLI entry point for the Black-Scholes Options Dashboard.

Usage examples:
    python pricer.py --S 100 --K 105 --T 30 --r 0.05 --sigma 0.2
    python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --greeks
    python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --straddle
    python pricer.py --S 100 --K 100 --T 365 --r 0.05 --sigma 0.2 --heatmap
"""

import argparse
from bs_pricer import bs_call, bs_put, put_call_parity_check
from greeks import all_greeks
from strategies import straddle, bull_call_spread
from analysis import plot_greeks, pnl_heatmap


def main():
    parser = argparse.ArgumentParser(description="Black-Scholes Options Pricer")
    parser.add_argument("--S",     type=float, required=True,  help="Stock price")
    parser.add_argument("--K",     type=float, required=True,  help="Strike price")
    parser.add_argument("--T",     type=float, required=True,  help="Days to expiry")
    parser.add_argument("--r",     type=float, required=True,  help="Risk-free rate")
    parser.add_argument("--sigma", type=float, required=True,  help="Volatility")
    parser.add_argument("--greeks",  action="store_true", help="Show Greeks")
    parser.add_argument("--straddle", action="store_true", help="Show straddle analysis")
    parser.add_argument("--heatmap",  action="store_true", help="Show P&L heatmap")
    parser.add_argument("--plot",     action="store_true", help="Plot Greeks chart")

    args = parser.parse_args()
    T = args.T / 365  # convert days to years

    # --- Core pricing ---
    call = bs_call(args.S, args.K, T, args.r, args.sigma)
    put  = bs_put(args.S,  args.K, T, args.r, args.sigma)
    parity = put_call_parity_check(args.S, args.K, T, args.r, args.sigma)

    print(f"\n{'='*45}")
    print(f"  Black-Scholes Options Pricer")
    print(f"{'='*45}")
    print(f"  S={args.S}  K={args.K}  T={args.T}d  r={args.r}  σ={args.sigma}")
    print(f"{'='*45}")
    print(f"  Call Price : ${call:.4f}")
    print(f"  Put Price  : ${put:.4f}")
    print(f"  Put-Call Parity: {'✓ holds' if parity else '✗ violated'}")

    # --- Greeks ---
    if args.greeks:
        g = all_greeks(args.S, args.K, T, args.r, args.sigma)
        print(f"\n  Greeks")
        print(f"  {'─'*30}")
        for name, val in g.items():
            print(f"  {name:<8}: {val:.6f}")

    # --- Straddle ---
    if args.straddle:
        s = straddle(args.S, args.K, T, args.r, args.sigma)
        print(f"\n  Straddle Analysis")
        print(f"  {'─'*30}")
        for k, v in s.items():
            print(f"  {k:<20}: {v}")

    # --- Heatmap ---
    if args.heatmap:
        pnl_heatmap(args.K, args.r, args.sigma)

    # --- Greeks plot ---
    if args.plot:
        plot_greeks(args.K, T, args.r, args.sigma)

    print(f"{'='*45}\n")


if __name__ == "__main__":
    main()
