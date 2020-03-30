# coding=utf-8
import json
answer_book = open("../Answer2/A_WordReview_三作家传（标点符号测试）_punctuation.json", encoding="utf-8", errors="ignore")
answer_list = json.load(answer_book)
answer_book.close()
# print(answer_list)
wrong_predict = open("../Result/20200218/Compare/punctuation/WordReview_三作家传（标点符号测试）_N_diff.json", encoding="utf-8", errors="ignore")
wrong_predict_list = json.load(wrong_predict)
wrong_predict.close()
compare = []
index_set = {}
new_answer_list = []
i = 0
for item in answer_list:
    para_index = item["paragraphIndex"]
    sen = item["sentence"]
    right_answer = item["content"]
    if para_index not in index_set:
        new_item = {}
        new_item["sentence"] = sen
        new_item["answer"] = [right_answer]
        new_item["paragraphIndex"] = para_index
        new_answer_list.append(new_item)
        index_set[para_index] = i
        i += 1
    else:
        index = index_set[para_index]
        new_answer_list[index]["answer"].append(right_answer)


for item in new_answer_list:
    para_index = item["paragraphIndex"]
    sen = item["sentence"]
    right_answer = item["answer"]
    for temp in wrong_predict_list:
        if temp["paragraphIndex"] == para_index:
            content = temp["content"]
            lookup = temp["lookup"]
            break
    else:
        continue
    new_item = {}
    new_item["answer"] = "\t".join(right_answer)
    new_item["predict"] = content
    new_item["sentence"] = sen
    new_item["lookup"] = lookup
    compare.append(new_item)

with open("wrong_predict.json", "w", encoding="utf-8") as file:
    json.dump(compare, file, ensure_ascii=False, indent=True)





