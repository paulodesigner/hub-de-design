#!/usr/bin/env python3
"""WCAG contrast checker for code->figma validation.

Usage:
  python3 wcag-contrast.py '#1a1a1a' '#ffffff'            # single pair
  python3 wcag-contrast.py '#1a1a1a' '#ffffff' large      # large text / icon / border / focus (min 3.0)
  python3 wcag-contrast.py                                 # runs the self-test demo

Thresholds (WCAG 2.1/2.2 AA):
  - normal text:            4.5:1   (default)
  - large text (>=24px, or >=18.66px bold), icons/graphics, UI borders, focus ring: 3.0:1
  - AAA normal: 7.0:1
Note: disabled/inactive components are EXEMPT (WCAG 1.4.3).
"""
import sys

def _lin(c):
    c /= 255.0
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4

def luminance(hexstr):
    h = hexstr.lstrip('#')
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return 0.2126*_lin(r) + 0.7152*_lin(g) + 0.0722*_lin(b)

def ratio(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a,b), min(a,b)
    return (hi + 0.05) / (lo + 0.05)

def check(fg, bg, kind="normal"):
    need = 3.0 if kind in ("large","icon","border","focus","nontext") else 4.5
    r = ratio(fg, bg)
    return r, need, ("PASS" if r >= need else "FAIL")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2:
        fg, bg = args[0], args[1]
        kind = args[2] if len(args) > 2 else "normal"
        r, need, status = check(fg, bg, kind)
        print(f"{status}  {r:.2f}:1  (min {need})  {fg} on {bg}  [{kind}]")
    else:
        demo = [
            ("title",  "#1a1a1a", "#ffffff", "normal"),
            ("desc",   "#666666", "#ffffff", "normal"),
            ("icon",   "#6b55d8", "#ffffff", "icon"),
            ("focus",  "#5644ad", "#ffffff", "focus"),
        ]
        for label, fg, bg, kind in demo:
            r, need, status = check(fg, bg, kind)
            print(f"{status}  {r:5.2f}:1 (min {need}) — {label}: {fg} on {bg}")
