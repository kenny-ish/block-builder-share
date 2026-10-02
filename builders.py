"""Ethereum block builder share from extraData."""
import argparse
import json
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor


def rpc(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "User-Agent": "block-builder-share"})
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.load(r)
    if "error" in resp:
        raise RuntimeError(resp["error"].get("message"))
    return resp["result"]


def label(extra_data_hex, miner):
    raw = bytes.fromhex(extra_data_hex[2:]) if extra_data_hex else b""
    text = "".join(chr(b) for b in raw if 32 <= b < 127).strip()
    return text if len(text) >= 3 else miner.lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--blocks", type=int, default=300)
    ap.add_argument("--rpc", default="https://ethereum-rpc.publicnode.com")
    a = ap.parse_args()

    head = int(rpc(a.rpc, "eth_blockNumber", []), 16)
    numbers = range(head - a.blocks + 1, head + 1)
    with ThreadPoolExecutor(max_workers=8) as pool:
        blocks = list(pool.map(lambda n: rpc(a.rpc, "eth_getBlockByNumber", [hex(n), False]), numbers))

    counts = Counter()
    recipients = defaultdict(Counter)
    gas = defaultdict(int)
    for b in blocks:
        lab = label(b.get("extraData"), b["miner"])
        counts[lab] += 1
        recipients[lab][b["miner"].lower()] += 1
        gas[lab] += int(b["gasUsed"], 16)

    print(f"blocks {numbers[0]}-{numbers[-1]} ({len(blocks)})\n")
    print(f"{'builder (extraData)':<34}{'blocks':>7}{'share':>8}{'avg gas':>12}  top fee recipient")
    for lab, n in counts.most_common():
        top, _ = recipients[lab].most_common(1)[0]
        print(f"{lab[:33]:<34}{n:>7}{n / len(blocks):>8.1%}{gas[lab] / n / 1e6:>10.1f}M  {top}")


if __name__ == "__main__":
    main()
