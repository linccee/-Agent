#!/usr/bin/env python3
"""Test script for compare_prices function"""

from tools.price_tool import prices

if __name__ == "__main__":
    result = prices.invoke({"platform": "Amazon", "product_sku": "B0FH5DPB28"})
    # result = prices.invoke({"platform": "eBay", "product_sku": "257232260675"})
    print(result)