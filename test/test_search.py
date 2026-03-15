#!/usr/bin/env python3
"""Test script for search_products function"""

from tools.search_tool import  search_products

if __name__ == "__main__":
    result = search_products.invoke({'query': 'switch2 jp version'})
    print(result)
