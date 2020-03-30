# coding=utf-8


def split_cube(nesting_list, left_punc, right_punc):
    # 把嵌套符号分组如 《<><》》《》  分成 《<><》》和《》
    split_list = []
    left = 0
    max_left = 0
    temp_list = []
    for item in nesting_list:
        if item['c'] in left_punc:
            if left == 0 and len(temp_list) != 0:
                temp_list.append(max_left)
                split_list.append(temp_list)
                max_left = 0
                temp_list = []
                temp_list.append(item)
                left += 1
            else:
                temp_list.append(item)
                left += 1
            if max_left < left:
                max_left = left
        else:
            temp_list.append(item)
            left -= 1
    if len(temp_list) != 0:
        temp_list.append(max_left)
        print(temp_list)
        split_list.append(temp_list)
    return split_list

yinhao_left = ["'", "\"", "‘", "“"]  # ‘’    “”
yinhao_right = ["”", "’", "'", '"']
kuohao_left = ["[", "{", "【", '(', '（', '〔', "［", "《", '｛']
kuohao_right = ["]", "}", "】", ")", '）', '〕', '］', '》', '｝']
# math_kuohao_left = ["{", "[", "("]
# math_kuohao_right = ["}", "]", ")"]
# character_end = all_biaodian + yinhao_right + yinhao_left + kuohao_right + kuohao_left
traditional_yinhao = ["「", "」", "『", "』"]
yinhao_left = set(yinhao_left)
yinhao_right = set(yinhao_right)
kuohao_left = set(kuohao_left)
kuohao_right = set(kuohao_right)
left_punc = yinhao_left.union(kuohao_left)
right = {}
nest_list = [{"c":'('}, {"c":')'},{"c":'['},{"c":'{'},{'c':'}'},{'c':']'}, {"c":'“'}, {"c":'“'},{"c":'“'}, {"c":'”'}, {"c":'”'},{"c":'“'}, {"c":'”'},{"c":'”'}]

print(split_cube(nest_list, left_punc, right))