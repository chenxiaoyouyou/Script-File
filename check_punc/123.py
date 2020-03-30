# coding=utf-8
import json

with open("..\Result\\20200228\Compare\punctuation\WordReview_三作家传（标点符号测试）_N_diff.json", encoding="utf-8") as f:
    neg = json.load(f)

with open("../Books2/WordReviewByPara_三作家传（标点符号测试）.txt", encoding="utf-8") as f:
    source = json.load(f)

print(len(neg))
print(len(source))
print(neg[0])
print(source[0])
res = []
for item1 in neg:
    index = item1["paragraphIndex"]
    for item2 in source:
        if index == item2["ParagraphIndex"]:
            item1["source"] = item2["Text"]
            res.append(item1)
print(len(res))

with open("wubao1.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=True)



