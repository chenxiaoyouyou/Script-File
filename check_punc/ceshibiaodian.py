# coding=utf-8
import json
from check_punc_0313 import check_punc
from check_quanbanjiao import check_quanbanjiao

with open("../bookContent/WordReviewByPara_三作家传（标点符号测试）.txt", encoding="utf-8", errors="ignore") as file:
    source_text = json.load(file)
    # print(source_text)
with open("../Answer2/A_WordReview_三作家传（标点符号测试）_punctuation.json", encoding="utf-8", errors="ignore") as file:
    answer_text = json.load(file)

print(source_text)
result_list = check_punc(source_text)
result_list1 = check_quanbanjiao(source_text)
result_list += result_list1
# {'pageIndex': 0, 'paragraphIndex': 43, 'offset': 5, 'content': '》', 'lookup': '需补充《', 'errortype': 1, 'rule': 'pun
print(result_list)
# print(len(result_list))
wubao = []
loubao = []

index_set = {}
new_answer_list = []
i = 0
# {'pageIndex': 1, 'paragraphIndex': 1, 'offset': 2, 'content': '】', 'lookup': '需补充【', 'errortype': 1, 'rule': 'punctuation'}
for item in answer_text:
    para_index = item["paragraphIndex"]
    sen = item["sentence"]
    right_answer = item["content"]
    offset = item['offset']
    for item2 in result_list:
        if item2['paragraphIndex'] == para_index and right_answer == item2["content"] and offset == item2["offset"]:
            break
    else:
        loubao.append(item)


for item1 in result_list:
    for item2 in answer_text:
        para_index = item2["paragraphIndex"]
        sen = item2["sentence"]
        right_answer = item2["content"]
        offset = item2['offset']
        if item1['paragraphIndex'] == para_index and right_answer == item1["content"] and offset == item1["offset"]:
            break
    else:
        for item3 in source_text:
            if item3["ParagraphIndex"] == item1["paragraphIndex"]:
                item1.update(sentence=item3["Text"])
                wubao.append(item1)

with open("wubao.json", "w", encoding="utf-8") as f:
    json.dump(wubao, f, ensure_ascii=False, indent=True)


# for item1 in result_list:
#     para_index = item1["paragraphIndex"]
#     for item2 in new_answer_list:
#         if para_index == item2["paragraphIndex"]:
#             pass


# index_set = set()
# for i in result_list:
#     index_set.add(i["paragraphIndex"])
#
# for item in new_answer_list:
#     if item["paragraphIndex"] not in index_set:
#         loubao.append(item)

with open("loubao.json", "w", encoding="utf-8") as f:
    json.dump(loubao, f, ensure_ascii=False, indent=True)

# print(new_answer_list)