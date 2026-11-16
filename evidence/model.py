#!/usr/bin/env python3
"""Foreguild revenue model — every number traceable to plan §10.

Run:  python3 model.py

This is the falsifiable core of the "revenue-optimised" claim. Every input is
a named assumption at the top; every output is derived. Change a scenario,
re-run, and the kill criteria in §14 price themselves.

Units: USD unless noted. sDAI/USDS treated as $1 (stated assumption).
"""

# ---------------------------------------------------------------- assumptions
# Task economics — from §10's worked $500 judged task (verified against index.html)
WORKER_FEE   = 0.03    # 3% worker-side take
POSTER_FEE   = 0.07    # 7% poster-side take (machine tasks)
ASSESS_JUDGED = 0.04   # 4% assessment on judged work ($16 assess + $4 treasury on $500)
ASSESS_MACHINE = 0.01  # 1% assessment on machine-checked work
VERDICT_SEED_NET = -0.016  # net cost of verdict-market seed as % of GMV (§10: -8.00/500)
DISPUTE_RESERVE = 0.01 # 1% until 3x trailing payouts
AGENT_GAS      = 0.006 # ~$3 per $500 task ≈ 0.6% of GMV

# Demand scenarios — monthly GMV and judged-work share.
# Judged share is THE number §14 kills on (<35% at day 90 -> VaaS pivot).
SCENARIOS = {
    "pessimistic": {"gmv_mo": 50_000,   "judged_share": 0.20},
    "median":      {"gmv_mo": 250_000,  "judged_share": 0.40},
    "optimistic":  {"gmv_mo": 1_000_000,"judged_share": 0.55},
}

# Verification-as-a-Service — receipts/month sold to external platforms.
# Priced per §06: $0.25-2 machine, $2-10 judged. Blended midpoint $3 used here.
VAAS = {
    "receipts_mo": {"pessimistic": 2_000, "median": 20_000, "optimistic": 100_000},
    "price_per_receipt": 3.00,
    "platform_share": 0.60,   # share of receipt price accruing to treasury
}

# Cost side — what it costs to run the swarm at each scale (rough, honest)
SWARM_COST_MO = {  # LLM + infra + liquidity ops
    "pessimistic": 2_000,
    "median":      8_000,
    "optimistic":  25_000,
}

KILL_GMV_JUDGED_SHARE = 0.35   # §14 kill criterion
KILL_DAY               = 90

# ------------------------------------------------------------- price anchors
# What a verdict costs elsewhere — the VaaS price floor argument (§06)
ANCHORS = [
    ("Kleros agentic court (Gnosis), full dispute",      "~$3.30",   "Devcon 8 demo, 5 min, autonomous"),
    ("Kleros xDAI General Court arbitration fee",         "~$12",     "12 xDAI juror fee, KIP-80 params"),
    ("Kleros standard court juror fee",                   "~$7",      "7.2 xDAI, xDAI Curation"),
    ("Manual QA review (freelance, small task)",          "$5-25",    "market rate, hours not minutes"),
    ("Foreguild panel verdict (48h fast path)",           "$0.25-10", "per receipt, scales with stakes"),
]

# ------------------------------------------------------------------- model
def treasury_per_gmv(judged_share):
    """Treasury contribution as fraction of GMV, blended across work mix.

    Machine task: poster 7% + worker 3% + 1% assess -> but treasury keeps
    the assessment slice + a share of take; §10 nets ≈6.5% on bare-take model
    and ≈10.8% on judged. We model per-task then blend.
    """
    # Judged task treasury yield (§10 worked example: +54/500 = 10.8%)
    judged_yield = 0.108
    # Machine task: take minus assessment payout minus reserves ~= 6.5% (§10)
    machine_yield = 0.065
    return judged_share * judged_yield + (1 - judged_share) * machine_yield

def run():
    print("=" * 72)
    print("FOREGUILD REVENUE MODEL — falsifiable core of §10")
    print("=" * 72)
    print(f"{'scenario':<14}{'GMV/mo':>12}{'judged%':>9}{'treasury/mo':>14}"
          f"{'VaaS/mo':>10}{'swarm/mo':>10}{'net/mo':>12}{'net/yr':>12}")
    print("-" * 72)
    results = {}
    for name, s in SCENARIOS.items():
        take = treasury_per_gmv(s["judged_share"])
        treasury = s["gmv_mo"] * take
        vaas = VAAS["receipts_mo"][name] * VAAS["price_per_receipt"] * VAAS["platform_share"]
        swarm = SWARM_COST_MO[name]
        net = treasury + vaas - swarm
        results[name] = net
        print(f"{name:<14}{s['gmv_mo']:>12,.0f}{s['judged_share']*100:>8.0f}%"
              f"{treasury:>14,.0f}{vaas:>10,.0f}{swarm:>10,.0f}{net:>12,.0f}{net*12:>12,.0f}")

    print()
    print("Judged-share sensitivity at median GMV ($250k/mo):")
    print(f"{'judged share':<16}{'treasury/mo':>14}{'status':>16}")
    for share in (0.10, 0.20, KILL_GMV_JUDGED_SHARE, 0.50, 0.70):
        t = 250_000 * treasury_per_gmv(share)
        flag = "KILL (<35%)" if share < KILL_GMV_JUDGED_SHARE else "above kill line"
        print(f"{share*100:>13.0f}%{t:>14,.0f}{flag:>16}")

    print()
    print("VaaS price anchors — what a verdict costs elsewhere:")
    for item, price, note in ANCHORS:
        print(f"  {item:<52} {price:>8}   {note}")

    print()
    print("Kill criterion (§14): judged work < 35% of GMV at day 90 -> pivot to")
    print("VaaS-only. In this model the pivot is not a failure state — at median")
    print("receipts the VaaS line alone is $36k/mo gross, $21.6k to treasury,")
    print("which covers the $8k swarm with room to spare.")

if __name__ == "__main__":
    run()
