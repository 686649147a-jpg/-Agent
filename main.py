from agents.parser_agent import ParserAgent
from agents.classifier_agent import ClassifierAgent
from agents.stats_agent import StatsAgent
from utils.matcher import fuzzy_match
import json

parser = ParserAgent()
classifier = ClassifierAgent("data/cities.json")
stats = StatsAgent()

with open("data/cities.json", "r", encoding="utf-8") as f:
    city_data = json.load(f)
all_cities = city_data["province_capitals"] + city_data["prefecture_cities"]

with open("data/sample_addresses.txt", "r", encoding="utf-8") as f:
    addresses = f.readlines()

print("开始处理...\n")

for addr in addresses:
    city = parser.extract_city(addr)

    if city:
        city = fuzzy_match(city, all_cities)
        category = classifier.classify(city)
    else:
        category = "未知"

    stats.update(category)

    print(f"地址: {addr.strip()} | 城市: {city} | 分类: {category}")

ratio = stats.result()
print("\n====================")
print(f"总样本数: {stats.total}")
print(f"省会+地级市占比: {ratio:.2%}")
