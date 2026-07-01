import urllib.request
import json

print("=== 测试产品接口 ===")
resp = urllib.request.urlopen('http://localhost:5000/api/v1/products')
data = json.loads(resp.read().decode())
print('产品总数:', data['data']['total'])
print('产品列表:')
for p in data['data']['items']:
    print('  -', p['name'], '($' + str(p['price_usd']) + ')')

print()
print("=== 测试分类接口 ===")
resp2 = urllib.request.urlopen('http://localhost:5000/api/v1/categories')
cats = json.loads(resp2.read().decode())
print('分类数量:', len(cats['data']))

print()
print("=== 测试轮播图接口 ===")
resp3 = urllib.request.urlopen('http://localhost:5000/api/v1/banners')
banners = json.loads(resp3.read().decode())
print('轮播图数量:', len(banners['data']))

print()
print("=== 测试网站配置接口 ===")
resp4 = urllib.request.urlopen('http://localhost:5000/api/v1/site-config')
config = json.loads(resp4.read().decode())
print('网站配置:', config['data'])

print()
print("=== 测试热销产品接口 ===")
resp5 = urllib.request.urlopen('http://localhost:5000/api/v1/products/hot')
hot = json.loads(resp5.read().decode())
print('热销产品数量:', len(hot['data']))

print()
print("=== 测试新闻接口 ===")
resp6 = urllib.request.urlopen('http://localhost:5000/api/v1/news')
news = json.loads(resp6.read().decode())
print('新闻数量:', news['data']['total'])

print()
print("所有接口测试完成！")
