from tools.review_tool import analyze_reviews

if __name__ == '__main__':
    query = '{"product_sku": "389173520354", "platform": "eBay"}'
    result = analyze_reviews.invoke(query)
    print(result)