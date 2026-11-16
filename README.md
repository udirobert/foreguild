# Foreguild — Every Task a Receipt

A revenue-first operating plan for **Foreguild**, a proposed AI job board run as a
Futarchy Autonomous Organization — submitted to the Seer FAO Operating Plan Contest
([Poidh bounty #1531](https://poidh.xyz/base/bounty/1531)).

**Read the plan:** <https://udirobert.github.io/foreguild/> (mirror: <https://foreguild-lime.vercel.app/>)

## What's in this repo

| Path | What it is |
|---|---|
| `index.html` + `plan.css` + `tokens.css` + `fonts.css` + `fonts/` | The plan — single standalone HTML document, Electric Foundation kit, prints to PDF |
| `evidence/model.py` | Runnable revenue model — §10's unit economics as executable scenarios; re-run it |
| `evidence/create-market.cjs` | The script that created the live market below |
| `evidence/seer-depth.json` | Measured appendix: 398 futarchy markets → 0 liquidity / 0 volume / 0 odds |
| `evidence/futarchy_raw.json` | All 398 raw market rows behind that measurement |
| `evidence/receipt.json` + `evidence/receipt-anchor/` | A signed specimen VerificationReceipt, digest-anchored on Base — `verify()` returns true |

## The live artifact

This submission doesn't just describe futarchy — it prices its own central claim on Seer:

> **"Will any futarchy market on Seer record nonzero trading volume before 1 March 2027?"**

- Market: [`0x867eB2bd5239d2d810F5Cd77954780330dc8e013`](https://app.seer.pm/#/markets/8453/0x867eB2bd5239d2d810F5Cd77954780330dc8e013) (Base, sUSDS collateral)
- Creation tx: [`0x937aaf55…7bd4`](https://basescan.org/tx/0x937aaf55676413b30d84ae3774b2a6dc70082d00ebb074a502cc2afe09527bd4)
- Reproduce: `npm i viem @seer-pm/sdk && PRIVATE_KEY=0x… node evidence/create-market.cjs --dry-run`

And the receipt format is deployed too: `ReceiptAnchor` on Base
([`0x8fEBbbc356F4AFBB8FA9c43F46Bd2bEdA327e95A`](https://basescan.org/address/0x8fEBbbc356F4AFBB8FA9c43F46Bd2bEdA327e95A))
stores receipt digests; `verify(0x5ea1b331…9239fee8)` returns `true` for the specimen receipt
in `evidence/receipt.json` and `false` for anything else.

## Verify the numbers yourself

```bash
python3 evidence/model.py   # pessimistic / median / optimistic scenarios + kill line
```

Every figure in §10–§14 is either measured (with the raw pull shipped), linked to a
primary source (§18), or inside the runnable model.
