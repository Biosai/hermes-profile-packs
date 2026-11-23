# Explorers and endpoints

Public sources change; re-check an endpoint before relying on it and name the one used in the report.

## Chains to sweep
Ethereum, Arbitrum, Optimism, Base, Polygon, BNB Smart Chain, Avalanche C-Chain, Gnosis, Linea, Scroll, zkSync Era, Blast, Mantle, Celo, Fantom/Sonic, Moonbeam, Cronos, opBNB, Polygon zkEVM. Add the chains the owner names.

## Public RPC
- Many chains: `https://<chain>-rpc.publicnode.com` (for example `ethereum-rpc.publicnode.com`, `arbitrum-one-rpc.publicnode.com`, `bsc-rpc.publicnode.com`).
- zkSync Era: `https://mainnet.era.zksync.io`.
- Calls: `eth_getBalance(address, "latest")`, `eth_getTransactionCount(address, "latest")`, `eth_call` for `balanceOf(address)` (selector `0x70a08231`).
- Public endpoints usually refuse `eth_getLogs` without an address filter and over wide block ranges.

## Explorer APIs
- **Blockscout API v2**, no key: `https://<chain>.blockscout.com/api/v2/addresses/<address>/{transactions,token-transfers,token-balances,internal-transactions}`, and `/counters` for an address's transaction count. When a plain HTTP client gets a 403, load the same URL in the browser and read the JSON from the page body.
- **Etherscan-family explorers** (Etherscan, Arbiscan, Polygonscan, BscScan) often show a bot challenge to headless browsers. Prefer Blockscout or a portfolio viewer rather than retrying. Their multichain API needs a key, and its free tier may not cover every chain: check the chain list first.
- **BNB Smart Chain**: when BscScan is blocked, an alternative explorer that renders headless (for example one run by an RPC provider) lists all tokens and BEP-20 transfers; open its token list and token-transfer tab.

## Portfolio viewers
A public portfolio page (for example DeBank) renders with JavaScript: load it in the browser and wait several seconds. It gives a USD total per chain, protocol positions (supplied, borrowed, health factor) and exchange labels on counterparties. Confirm each position on chain before reporting it.

## Probes
Write each probe as a script file and save every response to a file before parsing. A probe that failed is reported as a failed source, not as an empty result.
