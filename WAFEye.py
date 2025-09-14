#!/usr/bin/env python3
import requests
import argparse
from WAFEye_Plugin import load_plugins
import re
import time
import sys
import random
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def hacker_title():
    title = """
    ██╗    ██╗ █████╗ ███████╗███████╗██╗   ██╗███████╗
    ██║    ██║██╔══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
    ██║ █╗ ██║███████║█████╗  █████╗   ╚████╔╝ █████╗  
    ██║███╗██║██╔══██║██╔══╝  ██╔══╝    ╚██╔╝  ██╔══╝  
    ╚███╔███╔╝██║  ██║██║     ███████╗   ██║   ███████╗
     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝
    
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ▓ > Web Application Firewall Detection Tool ▓
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    """
    print(Fore.RED + Style.BRIGHT + title)

def matrix_effect(duration=1.5):
    chars = "0123456789abcdef!@#$%^&*()abcdefghijklmnopqrstuvwxyz"
    end_time = time.time() + duration
    while time.time() < end_time:
        line = "".join(random.choice(chars) for _ in range(60))
        print(Fore.GREEN + line)
        time.sleep(0.02)

class SimpleResp:
    def __init__(self, resp):
        self.headers = {k: v for k, v in resp.headers.items()} if resp else {}
        self.text = resp.text if resp else ""
        self.status_code = getattr(resp, "status_code", None)
        self.reason = getattr(resp, "reason", "")
        try:
            cj = getattr(resp, "cookies", {})
            if hasattr(cj, "keys"):
                self.cookies = {k: cj.get(k) for k in cj.keys()}
            else:
                self.cookies = {}
        except Exception:
            self.cookies = {}

class WafEngine:
    def __init__(self, normal_resp: SimpleResp, attack_resp: SimpleResp = None, path="/"):
        self.rq = normal_resp
        self.attackres = attack_resp
        self.headers = dict(normal_resp.headers) if normal_resp else {}
        self.path = path
        self.requestnumber = 1
        self.knowledge = {'generic': {'found': False, 'reason': ''}, 'wafname': []}

    def _choose_resp(self, attack=True):
        return self.attackres if attack else self.rq

    def matchHeader(self, headermatch, attack=False):
        r = self._choose_resp(attack=attack)
        if not r:
            return False
        header, pattern = headermatch
        for hk, hv in r.headers.items():
            if hk.lower() == header.lower():
                try:
                    if re.search(pattern, hv, re.I):
                        return True
                except re.error:
                    if pattern.lower() in hv.lower():
                        return True
        return False
    
    def matchContent(self, pattern, attack=False):
        """Response içeriğini kontrol eder"""
        r = self._choose_resp(attack=attack)
        if not r or not r.text:
            return False
        try:
            return bool(re.search(pattern, r.text, re.I))
        except re.error:
            return pattern.lower() in r.text.lower()
    
    def matchCookie(self, cookiematch, attack=False):
        """Cookie'leri kontrol eder"""
        r = self._choose_resp(attack=attack)
        if not r or not r.cookies:
            return False
        cookie_name, pattern = cookiematch
        for name, value in r.cookies.items():
            if name.lower() == cookie_name.lower():
                try:
                    return bool(re.search(pattern, str(value), re.I))
                except re.error:
                    return pattern.lower() in str(value).lower()
        return False
    
    def matchStatus(self, status_code, attack=False):
        """HTTP status kodunu kontrol eder"""
        r = self._choose_resp(attack=attack)
        if not r:
            return False
        return r.status_code == status_code
    
    def matchReason(self, reason_text, attack=False):
        """HTTP reason phrase'ini kontrol eder"""
        r = self._choose_resp(attack=attack)
        if not r:
            return False
        try:
            return bool(re.search(reason_text, r.reason, re.I))
        except (re.error, AttributeError):
            return reason_text.lower() in str(r.reason).lower()
    
    def matchBoth(self, pattern_dict, attack=False):
        """Hem normal hem attack response'unu kontrol eder"""
        if attack and self.attackres:
            return self.matchContent(pattern_dict.get('content', ''), attack=True)
        return self.matchContent(pattern_dict.get('content', ''), attack=False)

class Detector:
    def __init__(self, url, plugins):
        self.url = url
        self.plugins = plugins
        self.response = None
        self.detected = []

    def normal_request(self):
        msg = f"[~] Sending normal request to {self.url}"
        for c in msg:
            sys.stdout.write(Fore.YELLOW + c)
            sys.stdout.flush()
            time.sleep(0.02)
        print()
        try:
            self.response = requests.get(self.url, timeout=7)
            print(Fore.CYAN + "[+] Normal request completed.\n")
            return self.response
        except requests.RequestException as e:
            print(Fore.RED + f"[!] Could not reach target: {e}")
            return None

    def detect_plugins(self, find_all=False):
        if not self.response:
            self.normal_request()
        if not self.response:
            print(Fore.RED + "[!] Normal request failed, plugin detection skipped.")
            return []

        normal_wrapped = SimpleResp(self.response)
        engine = WafEngine(normal_resp=normal_wrapped, attack_resp=None, path="/")

        for name, plugin in self.plugins.items():
            try:
                is_waf_fn = getattr(plugin, "is_waf", None)
                if callable(is_waf_fn):
                    ok = False
                    try:
                        ok = is_waf_fn(engine)
                    except TypeError:
                        ok = is_waf_fn(engine)
                    if ok:
                        self.detected.append(name)
                        print(Fore.GREEN + Style.BRIGHT + f"[+] WAF detected: {name}")
                        if not find_all:
                            break
            except Exception as e:
                print(Fore.YELLOW + f"[!] Plugin {name} raised an error: {e}")
                continue

        if not self.detected:
            print(Fore.MAGENTA + "[-] No WAF detected")
        return self.detected

    def active_attack_simulation(self, scope="50", aggressive=0.5):
        payloads_50 = ["<script>alert(1)</script>", "' OR '1'='1"]
        payloads_full = payloads_50 + ["<img src=x onerror=alert(1)>"]
        payloads = payloads_50 if scope == "50" else payloads_full

        print(Fore.CYAN + f"[~] Starting active test with scope {scope}...")
        matrix_effect(1)  # matrix efekti başlat

        total = len(payloads)
        for i, payload in enumerate(payloads, 1):
            try:
                r = requests.get(self.url, params={"test": payload}, timeout=7)
                progress = f"\r[{'█'*i}{'.'*(total-i)}] {i}/{total}"
                sys.stdout.write(Fore.YELLOW + progress)
                sys.stdout.flush()
                if r.status_code in [403, 406, 429] or "blocked" in (r.text or "").lower():
                    print(Fore.RED + f"\n[+] WAF likely blocked payload: {payload}")
                    return payload, r
            except requests.RequestException:
                continue
            time.sleep(aggressive)
        print(Fore.CYAN + "\n[~] Active test completed, no blocking detected.")
        return None, None

def main():
    hacker_title()
    parser = argparse.ArgumentParser(
        description="Plugin-based WAF Detection Tool (WAFEye plugins)"
    )
    parser.add_argument("--url", required=True, help="Target URL (e.g., https://site.com)")
    parser.add_argument("--findall", action="store_true", help="Detect all WAFs")
    parser.add_argument("--active", action="store_true", help="Enable active testing")
    parser.add_argument("--scope", choices=["50", "full"], default="50", help="Active test scope")
    parser.add_argument("--aggressive", type=float, default=0.5, help="Delay between payloads")

    args = parser.parse_args()

    plugins = load_plugins()
    print(Fore.CYAN + f"[~] Loaded {len(plugins)} WAFEye plugins.\n")

    detector = Detector(args.url, plugins)
    detector.normal_request()
    detector.detect_plugins(find_all=args.findall)

    if args.active:
        payload, attack_resp = detector.active_attack_simulation(scope=args.scope, aggressive=args.aggressive)
        if payload and attack_resp:
            print(Fore.GREEN + "[~] Active test completed.")

if __name__ == "__main__":
    main()
