#!/usr/bin/env node
// Create the Foreguild falsification market on Seer (Base, chain 8453).
// Usage:
//   PRIVATE_KEY=0x... node create-market.cjs          # simulate + send
//   node create-market.cjs --dry-run                  # build + simulate only
//   node create-market.cjs --address                  # show derived address, exit
const {
  createPublicClient,
  createWalletClient,
  http,
  parseEther,
} = require("viem");
const { base } = require("viem/chains");
const { privateKeyToAccount } = require("viem/accounts");
const {
  getCreateMarketExecution,
  getNewMarketFromLogs,
  MarketTypes,
} = require("@seer-pm/sdk");

const QUESTION =
  "Will any futarchy market on Seer record nonzero trading volume before 1 March 2027?";
const OUTCOMES = ["Yes", "No"];
const MIN_BOND = parseEther("1"); // 1 sUSDS (~$1) — deters spam answers, cheap to dispute

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const addrOnly = args.includes("--address");

const pk = process.env.PRIVATE_KEY;
if (!pk) {
  console.error("PRIVATE_KEY env var required.");
  process.exit(1);
}
if (!/^0x[0-9a-fA-F]{64}$/.test(pk)) {
  console.error("PRIVATE_KEY must be 0x + 64 hex chars");
  process.exit(1);
}

const account = privateKeyToAccount(pk);
if (addrOnly) {
  console.log(account.address);
  process.exit(0);
}

const publicClient = createPublicClient({ chain: base, transport: http() });
const walletClient = createWalletClient({
  chain: base,
  transport: http(),
  account,
});

const chainId = base.id;
const openingTime = Math.floor(Date.now() / 1000);

const params = {
  marketType: MarketTypes.CATEGORICAL,
  marketName: QUESTION,
  outcomes: OUTCOMES,
  openingTime,
  minBond: MIN_BOND,
  chainId,
  category: "crypto",
};

const execution = getCreateMarketExecution(params);
console.log("creator:        ", account.address);
console.log("factory:        ", execution.to);
console.log("question:       ", QUESTION);
console.log("openingTime:    ", new Date(openingTime * 1000).toISOString());
console.log("minBond:        ", MIN_BOND.toString(), "(1 sUSDS)");

async function main() {
const gasEstimate = await publicClient.estimateGas({
  to: execution.to,
  data: execution.data,
  value: execution.value ?? 0n,
  account: account.address,
});
console.log("est. gas:       ", gasEstimate.toString());

const fee = await publicClient.estimateFeesPerGas();
const costWei = gasEstimate * (fee.maxFeePerGas ?? fee.gasPrice ?? 0n);
console.log("est. max cost:  ", (Number(costWei) / 1e18).toFixed(6), "ETH");

const bal = await publicClient.getBalance({ address: account.address });
console.log("balance:        ", (Number(bal) / 1e18).toFixed(6), "ETH");
if (bal < costWei) {
  console.error("Insufficient balance for gas.");
  process.exit(1);
}
if (dryRun) {
  console.log("dry run — not sending.");
  process.exit(0);
}

const hash = await walletClient.sendTransaction({
  to: execution.to,
  data: execution.data,
  value: execution.value ?? 0n,
});
console.log("tx:             ", hash);
const receipt = await publicClient.waitForTransactionReceipt({ hash });
console.log("status:         ", receipt.status);

const marketAddress = getNewMarketFromLogs(receipt.logs);
console.log("market:         ", marketAddress ?? "(NewMarket event not found — check logs)");
if (marketAddress) {
  console.log(`https://seerscan.org/base/markets/${marketAddress}`);
  console.log(`https://basescan.org/address/${marketAddress}`);
}
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
