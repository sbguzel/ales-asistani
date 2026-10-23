# -*- coding: utf-8 -*-
"""
2021-ALES/2 SÖZEL TESTİ (Q1 - Q50) OTOMATİK OLUŞTURUCU
"""

import re
import json

SOZEL_KEY = {
    1: 'D', 2: 'B', 3: 'A', 4: 'A', 5: 'D', 6: 'B', 7: 'B', 8: 'B', 9: 'D', 10: 'C',
    11: 'B', 12: 'B', 13: 'C', 14: 'A', 15: 'C', 16: 'B', 17: 'C', 18: 'A', 19: 'B', 20: 'C',
    21: 'E', 22: 'E', 23: 'A', 24: 'B', 25: 'B', 26: 'B', 27: 'E', 28: 'A', 29: 'A', 30: 'D',
    31: 'C', 32: 'D', 33: 'A', 34: 'E', 35: 'E', 36: 'C', 37: 'E', 38: 'D', 39: 'A', 40: 'C',
    41: 'C', 42: 'C', 43: 'D', 44: 'D', 45: 'E', 46: 'C', 47: 'E', 48: 'C', 49: 'A', 50: 'D'
}

with open('scripts/seeds/sozel_by_columns.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Remove page markers
cleaned = re.sub(r'=== PAGE \d+ ===\n', '', raw_text)

# We will manually clean and split questions carefully
# Let's inspect each question's text
print('Building Sözel 2021-ALES/2 generator...')
