# block-builder-share

Counts who built the last N Ethereum blocks. Since the merge most blocks come from a few specialized
builders through MEV-Boost relays, and builders usually put their name in the block's `extraData`.
It only needs `eth_getBlockByNumber`.

```bash
python builders.py
python builders.py --blocks 1000
python builders.py --rpc https://mainnet.base.org --blocks 300     # L2s have a single sequencer
```

For each block it decodes `extraData` as text (dropping non-printable bytes) and records the `miner`
field (the fee recipient). The output has the number of blocks and the share per builder label, the
most common fee recipient for each label, and the average gas used per block. Blocks with empty or
binary `extraData` are grouped by fee recipient instead.

Blocks are fetched 8 at a time. `--blocks 1000` takes a minute or two on a public RPC.

`extraData` is whatever the builder chooses to write, so it can't be fully trusted. The fee recipient
is more reliable, which is why both are shown.

## Tests

```bash
python -m unittest -v
```
