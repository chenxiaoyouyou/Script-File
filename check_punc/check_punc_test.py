# coding=utf-8
# -*- coding: utf-8 -*-
import time
import re
import copy
import pickle

"""
2020/2/11
修改：
提供嵌套错误的提示

"""


def check(text, number, page):
    error_list = []

    traditional_errors = []  # 判断繁体引号
    traditional_pairs = []
    traditional_nesting = []

    yinhao_pairs = []         # 判断中英文引号错误
    chinese_yinhao_nesting = []
    chinese_yinhao_nesting_array = []

    english_yinhao_nesting = []

    kuohao_pairs = []        # 判断括号的缺失与搭配不当
    kuohao_nesting = []      # 判断括号的嵌套
    kuohao_nesting_array = []     # 用于存放一组组的符号
    # level_kuohao_nesting = []      # 判定{[(
    shuminghao_nesting = []  # 书名号
    shuminghao_nesting_array = []
    shuminghao_pairs = []
    # li_left_Chinese_shuangyinhao = []  # “
    li_left_allbiaodian = []
    li_left_dianhao = []

    left_must_be_banjiao_yinhao = ['s', 'm', 't']
    left_must_be_banjiao_yinhao_2 = ['re', 'll']
    right_must_be_banjiao_yinhao = ['s']
    all_biaodian = ['.', '。', '!', '！', '?', '？', '…', ':', '：', ';', '、', '；', '—', ',', '，', '·']
    dianhao = ['.', '。', '!', '！', '?', '？', ':', '：', ';', '、', '；', ',', '，']
    yinhao_left = ["'", "\"", "‘", "“"]  # ‘’    “”
    yinhao_right = ["”", "’", "'", '"']
    kuohao_left = ["[", "{", "【", '(', '（', '〔', "［", "《", '｛']
    kuohao_right = ["]", "}", "】", ")", '）', '〕', '］', '》', '｝']
    # math_kuohao_left = ["{", "[", "("]
    # math_kuohao_right = ["}", "]", ")"]
    character_end = all_biaodian + yinhao_right + yinhao_left + kuohao_right + kuohao_left
    traditional_yinhao = ["「", "」", "『", "』"]
    yinhao_left = set(yinhao_left)
    yinhao_right = set(yinhao_right)
    kuohao_left = set(kuohao_left)
    kuohao_right = set(kuohao_right)
    left_punc = yinhao_left.union(kuohao_left)
    # all_pair_punc = yinhao_left + yinhao_right + kuohao_left + kuohao_right + traditional_yinhao
    #
    # kuohao = []
    # yinhao = []
    flag = 0
    # flag1 = 0

    # 用于配对符号
    yingshe = {'[': ']', ']': '[', '{': '}', '}': '{', '【': '】', '】': '【', '(': ')', ')': '(', '（': '）', '）': '（',
               '〔': '〕', '〕': '〔', '［': '］', '］': '［', '《': '》', '》': '《', "'": "'", '"': '"', "‘": "’", "’": "‘",
               "“": "”", "”": "“", "｛":"｝", '｝':'｛'}
    # 排除句首的）
    pattern_kuohao_1 = "[ 0-9.ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+?[\)）]"
    pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    pattern_kuohao_2 = "[a-zA-Z][\)）]"
    pattern_kuohao_2 = re.compile(pattern_kuohao_2)

    # 括号的首位置检查每句话只进行一次
    flag_start = True

    def add_right_kuohao(punc, is_order=False):
        if is_order:
            return 0
        pair = yingshe[punc]
        if len(kuohao_pairs) > 0:
            if kuohao_pairs[-1]["c"] == pair:
                item["flag"] = i
                item["pair"] = True
                item_last = copy.deepcopy(kuohao_pairs[-1])
                item_last["flag"] = i
                item_last["pair"] = True
                kuohao_nesting.append(item)
                kuohao_nesting.append(item_last)
                kuohao_nesting_array.append({"flag": i, "items": [item, item_last], "pair":True})
                kuohao_pairs.pop()
            elif kuohao_pairs[-1]["c"] in kuohao_right:
                if is_order:
                    return 0
                error_list.append([page, number, i, "", char, "需补充{}".format(pair), 1])
            else:
                if is_order:
                    return 0
                item["flag"] = i
                item["pair"] = False
                item_last = copy.deepcopy(kuohao_pairs[-1])
                item_last["flag"] = i
                item_last["pair"] = False
                kuohao_nesting.append(item)
                kuohao_nesting.append(item_last)
                kuohao_nesting_array.append({"flag": i, "items": [item, item_last], "pair":False})
                kuohao_pairs.pop()
        else:
            if is_order:
                return 0
            error_list.append([page, number, i, "", char, "需补充{}".format(pair), 1])
        return 0

    for i, char in enumerate(text):
        if char in [' ', '\t', '\n']:
            continue
        # 判断段首标点符号
        # 需求取消
        # if char in ['.','。','!','！','?','？','……',',','，','：','；',';',':','、'] and flag1 ==0:
        #   error_list.append((page,number,i+1,text[i],'','段首不能出现符号',1))
        # else:
        #   flag1 = 1

        item = {"i": i, "c": char}
        if char in all_biaodian:
            li_left_allbiaodian.append(i)

        if char == "「":
            traditional_pairs.append(item)
            continue
        if char == "」":
            # traditional_pairs.append(item)
            if len(traditional_pairs) > 0:
                if traditional_pairs[-1]["c"] in {"『", "「"}:
                    traditional_nesting.append(traditional_pairs[-1])
                    traditional_nesting.append(item)
                    traditional_pairs.pop()
                else:
                    traditional_errors.append([page, number, i, "", char, "需补充「", 1])
            else:
                traditional_errors.append([page, number, i, "", char, "需补充「", 1])
            continue
        if char == "『":
            traditional_pairs.append(item)
            continue

        if char == "』":
            # traditional_pairs.append(item)
            if len(traditional_pairs) > 0:
                if traditional_pairs[-1]["c"] in {"「", "『"}:
                    traditional_nesting.append(traditional_pairs[-1])
                    traditional_nesting.append(item)
                    traditional_pairs.pop()
                else:
                    traditional_errors.append([page, number, i, "", char, "需补充『", 1])
            else:
                traditional_errors.append([page, number, i, "", char, "需补充『", 1])
            continue

        # 判断引号
        if char == '“':
            yinhao_pairs.append(item)
            continue
        if char == '”':
            if len(yinhao_pairs) > 0:
                if yinhao_pairs[-1]["c"] in {'"', "'"}:
                    error_list.append([page, number, i, "", char, "成对标点符号格式须一致", 1])
                    error_list.append(
                        [page, number, yinhao_pairs[-1]["i"], "", yinhao_pairs[-1]["c"], "成对标点符号格式必须一致", 1])
                    yinhao_pairs.pop()
                elif yinhao_pairs[-1]["c"] in {"“", "‘"}:
                    chinese_yinhao_nesting.append(yinhao_pairs[-1])
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop()
                else:
                    error_list.append([page, number, i, "", char, "需补充“", 1])
            else:
                error_list.append([page, number, i, "", char, "需补充“", 1])
            continue

        if char == '‘':
            yinhao_pairs.append(item)
            continue
        if char == '’':
            # 判断I's等几个特殊情况
            # 需明确此时的content和lookup
            if text[i + 1:i + 2] in left_must_be_banjiao_yinhao:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append([page, number, i, text[i], "’", "修改为'", 1])
                continue
            if text[i + 1:i + 3] in left_must_be_banjiao_yinhao_2:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append([page, number, i, text[i], "’", "修改为'", 1])
                continue
            if text[i - 1:i] in right_must_be_banjiao_yinhao:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append([page, number, i, text[i], "’", "修改为'", 1])
                continue

            if len(yinhao_pairs) > 0:
                if yinhao_pairs[-1]["c"] in {'"', "'"}:
                    error_list.append([page, number, i, "", char, "成对标点符号格式须一致", 1])
                    error_list.append(
                        [page, number, yinhao_pairs[-1]["i"], "", yinhao_pairs[-1]["c"], "成对标点符号格式必须一致", 1])
                    yinhao_pairs.pop()
                elif yinhao_pairs[-1]["c"] in {"‘", "“"}:
                    chinese_yinhao_nesting.append(yinhao_pairs[-1])
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop()
                else:
                    error_list.append([page, number, i, "", char, "需补充‘", 1])
            else:
                error_list.append([page, number, i, "", char, "需补充‘", 1])
            continue

        if char == "'":
            # 排除"（fd’dsf）"的情况
            pattern_right = "[a-zA-Z0-9 ]+?）"
            pattern_right = re.compile(pattern_right)
            string_right = text[i + 1:]
            flag_right = pattern_right.match(string_right)
            pattern_left = "[a-zA-Z0-9 ]+?（"
            pattern_left = re.compile(pattern_left)
            string_left = text[:i][::-1]
            flag_left = pattern_left.match(string_left)
            if flag_left is not None and flag_right is not None:
                continue
            # 排除‘ll等情况
            if text[i + 1:i + 2] in left_must_be_banjiao_yinhao:
                continue
            if text[i + 1:i + 3] in left_must_be_banjiao_yinhao_2:
                continue
            if text[i - 1:i] in right_must_be_banjiao_yinhao:
                continue
            # 法语不进行判断
            if not_english(i, text):
                continue
            if len(yinhao_pairs) == 0:
                yinhao_pairs.append(item)
            else:
                if yinhao_pairs[-1]["c"] == "'":
                    english_yinhao_nesting.append(item)
                    english_yinhao_nesting.append(yinhao_pairs[-1])
                    yinhao_pairs.pop()
                else:
                    yinhao_pairs.append(item)
            continue

        if char == '"':
            if len(yinhao_pairs) == 0:
                yinhao_pairs.append(item)
            else:
                if yinhao_pairs[-1]["c"] == '"':
                    english_yinhao_nesting.append(item)
                    english_yinhao_nesting.append(yinhao_pairs[-1])
                    yinhao_pairs.pop()
                else:
                    yinhao_pairs.append(item)
            continue

        # 判断小括号
        # 检查左半边

        if char == '（':
            kuohao_pairs.append(item)
            continue
        if char == '）':
            # 句首的直接排除
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue
            is_order = is_order_number(i, text)
            add_right_kuohao("）", is_order=is_order)
            continue

        if char == '(':
            kuohao_pairs.append(item)
            continue
        if char == ')':
            # 句首的直接排除
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue
            is_order = is_order_number(i, text)
            add_right_kuohao(")", is_order=is_order)
            continue

        if char == "〔":
            kuohao_pairs.append(item)
            continue

        if char == "〕":
            add_right_kuohao("〕", is_order=False)
            continue

        if char == "[":
            kuohao_pairs.append(item)
            continue

        if char == "]":
            add_right_kuohao("]", is_order=False)
            continue

        if char == "［":
            kuohao_pairs.append(item)
            continue

        if char == "］":
            add_right_kuohao("］", is_order=False)
            continue

        if char == "【":
            kuohao_pairs.append(item)
            continue

        if char == "】":
            add_right_kuohao("】", is_order=False)
            continue

        if char == "{":
            kuohao_pairs.append(item)
            continue

        if char == "}":
            add_right_kuohao("}", is_order=False)
            continue

        if char == "｛":
            kuohao_pairs.append(item)
            continue

        if char == "｝":
            add_right_kuohao('｝', is_order=False)
            continue

        if char == "《":
            kuohao_pairs.append(item)
            shuminghao_pairs.append(item)
            # continue

        if char == "》":
            if len(kuohao_pairs) > 0:
                if kuohao_pairs[-1]["c"] == "《":
                    item["flag"] = i
                    item["pair"] = True
                    item_last = copy.deepcopy(kuohao_pairs[-1])
                    item_last["flag"] = i
                    item_last["pair"] = True
                    shuminghao_nesting.append(item)
                    shuminghao_nesting.append(item_last)
                    kuohao_pairs.pop()
                elif kuohao_pairs[-1]["c"] in kuohao_right:
                    error_list.append([page, number, i, "", char, "需补充《", 1])
                else:
                    error_list.append([page, number, i, "", char, "成对标点符号格式须一致", 1])
                    error_list.append(
                        [page, number, kuohao_pairs[-1]["i"], "", kuohao_pairs[-1]["c"], "成对标点符号格式须一致", 1])
                    kuohao_pairs.pop()
            else:
                if len(shuminghao_pairs) == 0:
                    error_list.append([page, number, i, "", char, "需补充《", 1])
                else:
                    if shuminghao_pairs[-1]['c'] in {"<", "《"}:
                        item["flag"] = i
                        item["pair"] = True
                        item_last = copy.deepcopy(shuminghao_pairs[-1])
                        item_last["flag"] = i
                        item_last["pair"] = True
                        shuminghao_nesting.append(item)
                        shuminghao_nesting.append(item_last)
                        shuminghao_pairs.pop()
                    else:
                        error_list.append([page, number, i, "", char, "需补充《", 1])

            if len(shuminghao_pairs) > 0:
                if shuminghao_pairs[-1]['c'] == "<":
                    item["flag"] = i
                    item["pair"] = False
                    item_last = copy.deepcopy(shuminghao_pairs[-1])
                    item_last["flag"] = i
                    item_last["pair"] = False
                    shuminghao_nesting.append(item)
                    shuminghao_nesting.append(item_last)
                    shuminghao_nesting_array.append({"flag": i, "items": [item, item_last], "pair": False})
                    shuminghao_pairs.pop()
                if len(shuminghao_pairs) > 0:
                    if shuminghao_pairs[-1]['c'] == "《":
                        shuminghao_pairs.pop()

        if char == "<":
            shuminghao_pairs.append(item)
            continue
        if char == ">":
            if len(kuohao_pairs) > 0:
                if kuohao_pairs[-1]['c'] == "《":
                    kuohao_pairs.pop()
            if len(shuminghao_pairs) > 0:
                if shuminghao_pairs[-1]["c"] == "<":
                    item["flag"] = i
                    item["pair"] = True
                    item_last = copy.deepcopy(shuminghao_pairs[-1])
                    item_last["flag"] = i
                    item_last["pair"] = True
                    shuminghao_nesting.append(item)
                    shuminghao_nesting.append(item_last)
                    shuminghao_nesting_array.append({"flag": i, "items": [item, item_last], "pair": True})
                    shuminghao_pairs.pop()
                elif shuminghao_pairs[-1]["c"] == "《":
                    item["flag"] = i
                    item["pair"] = False
                    item_last = copy.deepcopy(shuminghao_pairs[-1])
                    item_last["flag"] = i
                    item_last["pair"] = False
                    shuminghao_nesting.append(item)
                    shuminghao_nesting.append(item_last)
                    shuminghao_nesting_array.append({"flag": i, "items": [item, item_last], "pair": False})
                    shuminghao_pairs.pop()
            continue

        if char == '·':
            li_left_dianhao.append(i)
            continue
        if char == '》':
            flag = 1
            temp = i
            continue
        if char == '《' and i >= 2 and flag == 1:
            flag = 0
            if text[i - 2] == '》' and text[i - 1] == '、':
                error_list.append([page, number, i - 1, text[i - 1], '、', '删除、', 1])

    # 判断括号的遗漏问题
    for item in kuohao_pairs:
        error_list.append([page, number, item["i"], "", item["c"], "需补充{}".format(yingshe[item["c"]]), 1])

    # 判断繁体引号
    for item in traditional_pairs:
        if item["c"] == "「":
            traditional_errors.append([page, number, item["i"], "", item["c"], "需补充」", 1])
        else:
            traditional_errors.append([page, number, item["i"], "", item["c"], "需补充』", 1])

    error_list.extend(traditional_errors)
    if len(traditional_nesting) >= 2:
        traditional_nesting_errors = c_yinhao_nesting_check(traditional_nesting, label="「")
        for temp1 in traditional_nesting_errors:
            if "成对" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 1])
            else:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 2])

    # 判断中英文引号的匹配问题
    if len(yinhao_pairs) > 0:
        flag=False
        flag1 = True
        for i in range(len(yinhao_pairs)-1):
            if flag:
                flag=False
                continue
            item_current = yinhao_pairs[i]
            item_next = yinhao_pairs[i+1]
            if item_current["c"] in {"“", '‘'} and item_next["c"] in {'"', "'"}:
                error_list.append([page, number, item_current["i"], "", item_current["c"], "成对标点符号格式须一致", 1])
                error_list.append([page, number, item_next["i"], "", item_next["c"], "成对标点符号格式须一致", 1])
                flag=True
                if i + 2 == len(yinhao_pairs):
                    # 走到这一步，说明最后一个item已经判断
                    flag1 = False
                continue
            else:
                error_list.append([page, number, item_current["i"], "", item_current["c"], "需补充{}".format(yingshe[item_current["c"]]), 1])
        if flag1:
            error_list.append(
                [page, number, yinhao_pairs[-1]["i"], "", yinhao_pairs[-1]["c"], "需补充{}".format(yingshe[yinhao_pairs[-1]["c"]]), 1])

    # 判断英文引号的嵌套
    if len(english_yinhao_nesting) >= 2:
            english_yinhao_nesting_errors = e_yinhao_nesting_check(english_yinhao_nesting)

            for temp1 in english_yinhao_nesting_errors:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["msg"], 2])

    # 判断中文引号的嵌套
    if len(chinese_yinhao_nesting) >= 2:

        chinese_yinhao_nesting = sorted(chinese_yinhao_nesting, key=lambda x: x[i])
        chinese_yinhao_nesting = split_cube(chinese_yinhao_nesting, left_punc)
        chinese_yinhao_nesting_errors = c_yinhao_nesting_check(chinese_yinhao_nesting, label="“")
        for temp1 in chinese_yinhao_nesting_errors:
            if "成对" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 1])
            else:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 2])

    # 判断书名号的嵌套
    if len(shuminghao_nesting) >= 2:
        shuminghao_nesting_errors = shuminghao_check(shuminghao_nesting, shuminghao_nesting_array, text)
        for temp1 in shuminghao_nesting_errors:
            if "成对" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 1])
            else:
                error_list.append([page, number, temp1["i"], "", temp1["c"], temp1["errmsg"], 2])

    # 括号错误
    if len(kuohao_nesting) >= 2:
        kuohao_nesting_errors = kuohao_nesting_check(kuohao_nesting, kuohao_nesting_array, kuohao_left, kuohao_right)

        for item in kuohao_nesting_errors:
            if "成对" in item["errmsg"]:
                error_list.append([page, number, item["i"], "", item["c"], item["errmsg"], 1])
            else:
                error_list.append([page, number, item["i"], "", item["c"], item["errmsg"], 2])

    error_list_dict = []
    for err in error_list:
        dict_err = {}
        dict_err['pageIndex'] = err[0]
        dict_err['paragraphIndex'] = err[1]
        dict_err['offset'] = err[2]
        dict_err['content'] = err[4]
        dict_err['lookup'] = err[5]
        dict_err['errortype'] = err[6]
        dict_err["rule"] = "punctuation"
        error_list_dict.append(dict_err)

    # 判断标点是否连续使用
    lian_xv_cuo_wu = []
    if len(li_left_allbiaodian) > 0:
        aaa = -1
        for p in li_left_allbiaodian:
            aaa += 1
            # 判断叠用
            # 符号不能叠用（两个一样的符号紧连使用），符号之后不允许紧跟了同样的符号，需要排除以下情况
            # 省略号允许很多个叠用，不提示错误；
            # 问号允许最多三个连用（只允许全角），并提示错误类型为“可疑错误”；
            # 感叹号允许最多三个连用（只允许全角），并提示错误类型为“可疑错误”；
            # 如果连续重复使用了符号，则提示连续重复的所有符号的位置，并建议修改为“空”；
            # 如果使用了半角符号，提示绝对错误；
            # 179704 一字线可以两个叠用，两个以上提示错误，编码为4E00或2014；

            # 定位当前位置的前三个字符
            # p_1为前一个字符，p_2为前两个字符
            if p - 1 < 0:
                # p = 0
                p_3_start = 0
                p_3_end = 0
                p_2_start = 0
                p_2_end = 0
                p_1_start = 0
                p_1_end = 0
            elif p - 2 < 0:
                # p = 1
                p_3_start = 0
                p_3_end = 0
                p_2_start = 0
                p_2_end = 0
                p_1_start = p - 1
                p_1_end = p

            elif p - 3 < 0:
                p_3_start = 0
                p_3_end = 0
                p_2_start = p - 2
                p_2_end = p - 1
                p_1_start = p - 1
                p_1_end = p
            else:
                p_3_start = p - 3
                p_3_end = p - 2
                p_2_start = p - 2
                p_2_end = p - 1
                p_1_start = p - 1
                p_1_end = p

            # before_3好像没用
            # before_3 = text[p_3_start:p_3_end]
            # before_2 = text[p_2_start:p_2_end]
            before_1 = text[p_1_start:p_1_end]
            before_0 = text[p]  # 当前
            after_1 = text[p + 1:p + 2]
            # after_2 = text[p + 2:p + 3]
            # after_3 = text[p + 3:p + 4]
            # after_4 = text[p + 4:p + 5]

            # 判断叠用
            # if before_0 not in ['—', '…', '？', '！']:
            # 其他符号不允许叠用
            if before_0 == after_1:
                dict_err = {}
                dict_err['pageIndex'] = page
                dict_err['paragraphIndex'] = number
                dict_err['offset'] = p
                dict_err['content'] = before_0
                dict_err['lookup'] = "标点符号叠用"
                dict_err['errortype'] = 1
                dict_err["rule"] = "punctuation"
                lian_xv_cuo_wu.append(dict_err)

            if before_0 == before_1 and after_1 not in all_biaodian:
                dict_err = {}
                dict_err['pageIndex'] = page
                dict_err['paragraphIndex'] = number
                dict_err['offset'] = p
                dict_err['content'] = before_0
                dict_err['lookup'] = "标点符号叠用"
                dict_err['errortype'] = 1
                dict_err["rule"] = "punctuation"
                lian_xv_cuo_wu.append(dict_err)

            # 判断符号连用
            # 符号不能连用（两个不一样的符号紧连使用），但是排除以下情况
            # ？！连用（全角符号），符号有顺序，提示错误类型为“可疑错误”；
            # 省略号（……）与逗号(，)、句号（。）、问号（？）、感叹号（！）连用（包括全角和半角符号），包括前后，提示错误类型为“可疑错误”；
            # 双引号可与任何符号连用（全角符号），不提示错误；
            # 波折号（——）同“点号连用”，包括前后，提示错误类型为“可疑错误”；

            if before_0 != after_1 and after_1 in all_biaodian:
                dict_err = {}
                dict_err['pageIndex'] = page
                dict_err['paragraphIndex'] = number
                dict_err['offset'] = p
                dict_err['content'] = before_0
                dict_err['lookup'] = "标点符号连用"
                dict_err['errortype'] = 1
                dict_err["rule"] = "punctuation"
                lian_xv_cuo_wu.append(dict_err)

            if before_0 != before_1 and after_1 not in all_biaodian and before_1 in all_biaodian:
                dict_err = {}
                dict_err['pageIndex'] = page
                dict_err['paragraphIndex'] = number
                dict_err['offset'] = p
                dict_err['content'] = before_0
                dict_err['lookup'] = "标点符号连用"
                dict_err['errortype'] = 1
                dict_err["rule"] = "punctuation"
                lian_xv_cuo_wu.append(dict_err)
    lian_xv_cuo_wu = remove_chongfu_for_all(lian_xv_cuo_wu)

    idx_to_remove = []
    # 去除可以连用的应用
    for idx, item in enumerate(lian_xv_cuo_wu):
        con = item["content"]
        length = len(con)
        if con == "？！":
            item["errortype"] = 2
        elif length == 3 and con[0] == "…" and con[1] == "…" and con[2] in [",", ".", "?", "!", "，", "。", "！", "？"]:
            item["errortype"] = 2
        elif length == 3 and con[0] == con[1] == "—" and con[2] in dianhao:
            item["errortype"] = 2
        elif length == 3 and con[0] in [",", ".", "?", "!", "，", "。", "！", "？"] and con[1] == con[2] == "…":
            item["errortype"] = 2
        elif length == 3 and con[0] in dianhao and con[1] == con[2] == "—":
            item["errortype"] = 2
        elif length == 2 and con[0] in [",", ".", "?", "!", "，", "。", "！", "？"] and con[1] == "…":
            item["errortype"] = 2
        elif length == 2 and con[0] == "…" and con[1] in [",", ".", "?", "!", "，", "。", "！", "？"]:
            item["errortype"] = 2

        if con == "？" * length or con == "！" * length:
            if length >= 4:
                item["errortype"] = 1
            else:
                item["errortype"] = 2
        elif con == "—" * length:
            if 3 <= length <= 11:
                item["errortype"] = 1
            else:
                idx_to_remove.append(idx)
        elif con == "…" * length:
            idx_to_remove.append(idx)
        elif con == "." * length and length >= 12:
            idx_to_remove.append(idx)
        start = con[0]
        for char in con:
            if start != char:
                item["lookup"] = "标点符号连用"
            start = char

    idx_to_remove.sort(reverse=True)
    for i in idx_to_remove:
        lian_xv_cuo_wu.pop(i)

    error_list_dict.extend(lian_xv_cuo_wu)
    error_list_dict.sort(key=lambda x: x["offset"])
    return error_list_dict


def split_cube(nesting_list, left_punc):
    # 把嵌套符号分组如 《<><》》《》  分成 《<><》》和《》
    split_list = []
    left = 0
    temp_list = []
    max_left = 0
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
        split_list.append(temp_list)
    return split_list


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def e_yinhao_nesting_check(yinhao_list):
    # 判断英文引号的嵌套错误
    error_list = []
    pair_list = []
    flag = 0
    yinhao_list = sorted(yinhao_list, key=lambda x: x["i"])
    temp = []
    for item in yinhao_list:
        if item['c'] != '"':
            temp.append(item)
        else:
            # 遇见第一个2
            if flag == 0:
                if len(temp) != 0:
                    pair_list.append(temp)
                temp = []
                temp.append(item)
                flag = 1
            else:
                # 遇见第二个
                temp.append(item)
                pair_list.append(temp)
                temp = []
                flag = 0
    if len(temp) != 0:
        pair_list.append(temp)
    for pair in pair_list:
        if pair[0]['c'] != '"':
            for item in pair:
                item.update(msg="""''应写在""之内""")
                error_list.append(item)
    return error_list


def shuminghao_check(shuminghao_list, shuminghao_array, text):
    shuminghao_list = sorted(shuminghao_list, key=lambda x: x["i"])
    new_shuming_list = []
    idx = set()
    for i, item in enumerate(shuminghao_list):
        if item["i"] not in idx:
            new_shuming_list.append(item)
            idx.add(item["i"])

    shuminghao_list = new_shuming_list
    left1 = "《"
    right1 = "》"
    left2 = "<"
    right2 = ">"

    length = len(shuminghao_list)
    error_list = []
    # flag = False
    errmsg = "{}应写在之内".format(left2 + right2, left1 + right1)
    errmsg1 = "成对标点符号格式须一致"
    for i, item_current in enumerate(shuminghao_list):
        if i == 0:
            item_last1 = {"i": -1, "c": ""}
            item_last2 = {"i": -1, "c": ""}
        elif i == 1:
            item_last1 = shuminghao_list[i - 1]
            item_last2 = {"i": -1, "c": ""}
        else:
            item_last1 = shuminghao_list[i - 1]
            item_last2 = shuminghao_list[i - 2]

        if i == length - 1:
            item_next = {"i": -1, "c": ""}
        else:
            item_next = shuminghao_list[i + 1]

        # 《 》
        if item_last2["c"] == left1 and item_next['c'] == right1:
            # 《 《》 》
            if item_last1['c'] == left1 and item_current['c'] == right1:
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                # item_last2["errmsg"] = errmsg
                # item_next["errmsg"] = errmsg
                error_list.extend([item_last1, item_current])
            # 《《 > 》
            elif item_last1['c'] == left1 and item_current['c'] == right2:

                # item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                error_list.extend([item_current])
            # “ ‘ ” ” 《 < 》》
            elif item_last1['c'] == left2 and item_current['c'] == right1:
                item_last1["errmsg"] = errmsg
                # item_current["errmsg"] = errmsg
                error_list.extend([item_last1])
        # ‘ ’
        elif item_last2["c"] == left2 and item_next['c'] == right2:
            # ‘ “ ” ’ <《》>
            if item_last1["c"] == left1 and item_current['c'] == right1:
                try:
                    item_last3 = shuminghao_list[i - 3]
                    item_next2 = shuminghao_list[i + 2]
                except:
                    item_last3 = {"i": -1, "c": ""}
                    item_next2 = {"i": -1, "c": ""}
                #  “ ‘ “ ” ’ ”
                if item_last3['c'] == left1 and item_next2['c'] == right1:
                    continue
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_last1, item_current, item_next])
            # ‘ ‘ ” ’
            elif item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_last1, item_current, item_next])
            #  ‘ “ ’ ’
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_last1, item_current, item_next])
            #  ‘ ‘ ’ ’ <<>>
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                try:
                    item_last3 = shuminghao_list[i - 3]
                    item_next2 = shuminghao_list[i + 2]
                except:
                    item_last3 = {"i": -1, "c": ""}
                    item_next2 = {"i": -1, "c": ""}
                # 《<<>>》 里面错
                #   <<>>   外面错
                if item_last3['c'] == left1 and item_next2['c'] == right1:
                    item_last1["errmsg"] = errmsg
                    item_current['errmsg'] = errmsg
                    error_list.extend([item_last1, item_current])
                else:
                    item_last2["errmsg"] = errmsg
                    # item_last1["errmsg"] = errmsg
                    # item_current["errmsg"] = errmsg
                    item_next["errmsg"] = errmsg
                    error_list.extend([item_last2, item_next])

        # “ ’
        elif item_last2["c"] == left1 and item_next['c'] == right2:
            # “ ‘ ” ’
            if item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # “ “ ” ’
            elif item_last1['c'] == left1 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # “ “ ’ ’
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
                #  # “ ‘ ’ ’
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])

        # ‘ ”
        elif item_last2["c"] == left2 and item_next['c'] == right1:
            # ‘ ‘ ” ”
            if item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # ‘ “ ” ”
            elif item_last1['c'] == left1 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # ‘ “ ’ ”
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            # ‘ ‘ ’ ”
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
        elif item_last1['c'] == left1 and item_current['c'] == right2:
            item_current["errmsg"] = errmsg1
            item_last1["errmsg"] = errmsg1
            error_list.extend([item_last1, item_current])
        elif item_current['c'] == right1 and item_last1['c'] == left2:
            item_last1["errmsg"] = errmsg1
            item_current["errmsg"] = errmsg1
            error_list.extend([item_last1, item_current])
        if item_last2["c"] in {right1, ""} or item_next['c'] in {left1, ""}:
            if item_last1['c'] == left2 and item_current['c'] == right2:

                text1 = text[item_last1["i"]:item_current["i"]]
                if is_Chinese_v2(text1):
                    item_last1["errmsg"] = errmsg
                    item_current["errmsg"] = errmsg
                    error_list.append(item_last1)
                    error_list.append(item_current)

    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list


def c_yinhao_nesting_check(yinhao_list, left_lunc, label="“"):
    """中文引号嵌套检查"""
    if label == "“":
        left1 = "“"
        right1 = "”"
        left2 = "‘"
        right2 = "’"
    else:
        left1 = "「"
        right1 = "」"
        left2 = "『"
        right2 = "』"
    error_list = []
    # flag = False
    errmsg = "{}应写{}在之内".format(left2+right2, left1+right1)
    errmsg1 = "成对标点符号格式须一致"
    for item_list in yinhao_list:
        levels =



        item_first = item_list[0]
        item_last = item_list[-1]
        # “ ... ”
        if item_first['c'] == left1 and item_last['c'] == right1:
            if len(item_list) == 2:
                continue
            elif len(item_list) == 4:
                if item_list[1]['c']



        # ‘ ... ”
        elif item_first['c'] == left2 and item_last['c'] == right1:
            if len(item_list) == 2:
                for item in item_list:
                    item["errmsg"] = errmsg1
                    error_list.append(item)
            else:
                for item in item_list:
                    item['errmsg'] = errmsg
                    error_list.append(item)
        # “ ... ’
        elif item_first['c'] == left1 and item_last['c'] == right2:
            if len(item_list) == 2:
                for item in item_list:
                    item["errmsg"] = errmsg1
                    error_list.append(item)
            else:
                for item in item_list:
                    item['errmsg'] = errmsg
                    error_list.append(item)
        # ‘ ... ’
        else:



def func(item_past, item_current, error_list):
    item_left1 = item_past[0]
    item_right1 = item_past[1]
    item_left2 = item_past[2]
    item_right2 = item_past[3]
    if len(item_current) == 2:
        return












    for i, item_current in enumerate(yinhao_list):
        if i == 0:
            item_last1 = {"i": -1, "c": ""}
            item_last2 = {"i": -1, "c": ""}
        elif i == 1:
            item_last1 = yinhao_list[i - 1]
            item_last2 = {"i": -1, "c": ""}
        else:
            item_last1 = yinhao_list[i - 1]
            item_last2 = yinhao_list[i - 2]

        if i == length - 1:
            item_next = {"i": -1, "c": ""}
        else:
            item_next = yinhao_list[i + 1]

        # “ ”
        if item_last2["c"] == left1 and item_next['c'] == right1:
            # “ “ ” ”
            if item_last1['c'] == left1 and item_current['c'] == right1:
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                error_list.extend([item_last1, item_current])
            # “ “ ’ ”
            elif item_last1['c'] == left1 and item_current['c'] == right2:

                item_last1["errmsg"] = errmsg
                # item_current["errmsg"] = errmsg
                error_list.extend([item_last1])
            # “ ‘ ” ”
            elif item_last1['c'] == left2 and item_current['c'] == right1:
                # item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                error_list.extend([item_current])
        # ‘ ’
        elif item_last2["c"] == left2 and item_next['c'] == right2:
            # ‘ “ ” ’
            if item_last1['c'] == left1 and item_current['c'] == right1:
                try:
                    item_last3 = yinhao_list[i - 3]
                    item_next2 = yinhao_list[i + 2]
                except:
                    item_last3 = {"i": -1, "c": ""}
                    item_next2 = {"i": -1, "c": ""}
                #  “ ‘ “ ” ’ ”
                if item_last3['c'] == left1 and item_next2['c'] == right1:
                    continue
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg

                error_list.extend([item_last2, item_last1, item_current, item_next])
            # ‘ ‘ ” ’
            elif item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_last1, item_current, item_next])
            #  ‘ “ ’ ’
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_last1, item_current, item_next])
            #  ‘ ‘ ’ ’
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                # item_last1["errmsg"] = errmsg
                # item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next])

        # “ ’
        elif item_last2["c"] == left1 and item_next['c'] == right2:
            # “ ‘ ” ’
            if item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # “ “ ” ’
            elif item_last1['c'] == left1 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # “ “ ’ ’
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
                #  # “ ‘ ’ ’
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])

        # ‘ ”
        elif item_last2["c"] == left2 and item_next['c'] == right1:
            # ‘ ‘ ” ”
            if item_last1['c'] == left2 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # ‘ “ ” ”
            elif item_last1['c'] == left1 and item_current['c'] == right1:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            #  # ‘ “ ’ ”
            elif item_last1['c'] == left1 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            # ‘ ‘ ’ ”
            elif item_last1['c'] == left2 and item_current['c'] == right2:
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
        elif item_last1['c'] == left1 and item_current['c'] == right2:

            item_current["errmsg"] = errmsg1
            item_last1["errmsg"] = errmsg1
            error_list.extend([item_last1, item_current])
        elif item_last1['c'] == left2 and item_current['c'] == right1:

            item_last1["errmsg"] = errmsg1
            item_current["errmsg"] = errmsg1
            error_list.extend([item_last1, item_current])
        if item_last2["c"] in {right1, ""} or item_next['c'] in {left1, ""}:
            if item_last1['c'] == left2 and item_current['c'] == right2:
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                error_list.append(item_last1)
                error_list.append(item_current)

    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list


def yinhao_nesting_check(yinhao_list, label="“"):
    # 判断引号使用中的嵌套错误
    error_list = []
    yinhao_list = sorted(yinhao_list, key=lambda x: x["i"])
    if label == "“":
        left1 = "“"
        left2 = "‘"
        right1 = "”"
        right2 = "’"
    elif label == '"':
        left1 = right1 = '"'
        left2 = right2 = "'"
    elif label == "《":
        left1 = "《"
        left2 = "<"
        right1 = "》"
        right2 = ">"
    else:
        left1 = "「"
        left2 = "『"
        right1 = "」"
        right2 = "』"
    length = len(yinhao_list)
    item_last = {"c": ""}     # 上一个状态

    for i in range(length-1):
        item_current = yinhao_list[i]
        if i != 0:
            item_last = yinhao_list[i-1]
        item_next = yinhao_list[i+1]
        if item_current["c"] == item_next["c"]:
            item_current.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            error_list.append(item_current)
            item_next.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            error_list.append(item_next)

        flag = item_last["c"] == right1 or item_last["c"] == ""
     # “ ‘ “ ‘’，‘’ ” ’ ”
        if flag:
            # 判定在没有使用“的时候使用‘的错误
            if item_current["c"] == left2 and item_next["c"] == left1:
                #
                item_current.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
                item_next.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
                error_list.append(item_current)
                error_list.append(item_next)
            elif item_last["c"] == left2:
                item_current.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
                error_list.append(item_current)

    temp = copy.deepcopy(yinhao_list)
    temp.reverse()
    item_last = {"c": ""}
    for i in range(length-1):
        item_current = temp[i]
        item_next = temp[i+1]
        if i != 0:
            item_last = temp[i - 1]
        flag = item_last["c"] == left1 or item_last["c"] == ""
        if flag:
            if item_current["c"] == right2 and item_next["c"] == right1:
                item_current.update(errmsg="{}应写在{}之内".format(left2 + right2, left1 + right1))
                item_next.update(errmsg="{}应写在{}之内".format(left2 + right2, left1 + right1))
                error_list.append(item_current)
                error_list.append(item_next)
            elif item_current["c"] == right2:
                item_current.update(errmsg="{}应写在{}之内".format(left2 + right2, left1 + right1))
                error_list.append(item_current)

    error_list = sorted(error_list, key=lambda x: x["i"])
    return_list = []
    # 去重
    for item in error_list:
        for temp in return_list:
            if item["i"] == temp["i"]:
                break
        else:
            return_list.append(item)

    return return_list


def kuohao_nesting_check(kuohao_nesting, kuohao_nesting_array, kuo_left, kuo_right):
    kuohao_nesting = sorted(kuohao_nesting, key=lambda x: x['i'])
    error_list = []
    length = len(kuohao_nesting)
    # 中文圆括号（）：又叫小括号，编码FF08和FF09
    # 西文圆括号()：又叫小括号，编码0028和0029
    # 中文方括号［］：又叫中括号，编码FF3B和FF3D
    # 西文方括号[]：又叫中括号，编码005B和005D
    # 六角括号〔〕：编码3014和3015
    # 方头括号【】：编码3010和3011
    # 大括号｛｝：编码FF5B和FF5D
    small_left = {"(", "（"}
    small_right = {")", "）"}
    middle_left = {"[", "［"}
    middle_right = {"]", "］"}
    big_left = {"{"}
    big_right = {"}"}
    # item_last = {"i":0, "c":""}

    for i in range(length-1):
        item_current = kuohao_nesting[i]
        item_next = kuohao_nesting[i+1]
        # if i != 0:
        #     item_last = kuohao_nesting[i-1]
        # 同种括号连续
        if item_current["c"] == item_next["c"] and item_current["c"] in kuo_left:
            new_item = copy.deepcopy(item_next)
            new_item.update(errmsg="套用错误")
            error_list.append(new_item)
        if item_current['c'] == item_next['c'] and item_current['c'] in kuo_right:
            new_item = copy.deepcopy(item_current)
            new_item.update(errmsg="套用错误")
            error_list.append(new_item)

        # 不连续的时候只有{[()]}是对的
        if item_current["c"] in kuo_left and item_next["c"] in kuo_left:
            if item_current["c"] in big_left and item_next["c"] in middle_left:
                continue
            elif item_current["c"] in middle_left and item_next["c"] in small_left:
                continue
            else:
                if item_current["c"] != item_next["c"]:
                    item_current.update(errmsg="套用错误")
                    item_next.update(errmsg="套用错误")
                    error_list.append(item_current)
                    error_list.append(item_next)
        elif item_current["c"] in kuo_right and item_next["c"] in kuo_right:
            if item_current["c"] in small_right and item_next["c"] in middle_right:
                continue
            elif item_current["c"] in middle_right and item_next["c"] in big_right:
                continue
            else:
                if item_current['c'] != item_next['c']:
                    item_current.update(errmsg="套用错误")
                    item_next.update(errmsg="套用错误")
                    error_list.append(item_current)
                    error_list.append(item_next)

    error_list = sorted(error_list, key=lambda x: x["i"])
    for item_for_pair in kuohao_nesting_array:
        item_left, item_right = item_for_pair["items"]
        if item_for_pair["pair"] is True:
            item_left["errmsg"] = "套用错误"
            item_right["errmsg"] = "套用错误"
            if item_left in error_list:
                error_list.append(item_right)
            elif item_right in error_list:
                error_list.append(item_left)
        else:
            item_left["errmsg"] = "套用错误"
            item_right["errmsg"] = "套用错误"
            if item_left in error_list:
                error_list.append(item_right)
            elif item_right in error_list:
                error_list.append(item_left)
            else:
                item_left["errmsg"] = "成对标点符号格式须一致"
                item_right["errmsg"] = "成对标点符号格式须一致"
                error_list.append(item_left)
                error_list.append(item_right)
    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list

def remove_qiantao_kuohao(error_list, text):

    new_error_list = copy.deepcopy(error_list)
    xiaokuohao_qiantao_E = []
    xiaokuohao_qiantao_C = []
    dakuohao_qiantao = []
    zhongkuohao_qiantao = []

    fangkuohao_qiantao = []
    danyinhao_qiantao_E = []
    shuangyinhao_qiantao_E = []
    danyinhao_qiantao_C = []
    shuangyinhao_qiantao_C = []


    def is_a_cube(strings):
        # 判断一个字符串是不是为一句话， 判断嵌套是否生效
        # 不能有句号
        if len(strings) > 500:
            return False
        else:
            return True

    for error_item in new_error_list:
        if error_item["info"] == "[":
            zhongkuohao_qiantao.append(error_item)
        elif error_item["info"] == "{":
            dakuohao_qiantao.append(error_item)
        elif error_item["info"] == "(":
            xiaokuohao_qiantao_E.append(error_item)
        elif error_item["info"] == "（":
            xiaokuohao_qiantao_C.append(error_item)
        elif error_item["info"] == "“":
            shuangyinhao_qiantao_C.append(error_item)


        elif error_item["info"] == "]" and zhongkuohao_qiantao != []:
            strings = text[zhongkuohao_qiantao[-1]["i"]:error_item["i"]]
            res = is_a_cube(strings)
            if res:
                error_list.remove(error_item)
                error_list.remove(zhongkuohao_qiantao[-1])
                zhongkuohao_qiantao.pop(-1)
        elif error_item["info"] == ")" and xiaokuohao_qiantao_E != []:
            strings = text[xiaokuohao_qiantao_E[-1]["i"]:error_item["i"]]
            if is_a_cube(strings):
                error_list.remove(error_item)
                error_list.remove(xiaokuohao_qiantao_E[-1])
                xiaokuohao_qiantao_E.pop()
        elif error_item["info"] == "）" and xiaokuohao_qiantao_C != []:
            strings = text[xiaokuohao_qiantao_C[-1]["i"]:error_item["i"]]
            if is_a_cube(strings):
                error_list.remove(error_item)
                error_list.remove(xiaokuohao_qiantao_C[-1])
                xiaokuohao_qiantao_C.pop()
        elif error_item["info"] == "}" and dakuohao_qiantao != []:
            strings = text[dakuohao_qiantao[-1]["i"]:error_item["i"]]
            if is_a_cube(strings):
                error_list.remove(error_item)
                error_list.remove(dakuohao_qiantao[-1])
                dakuohao_qiantao.pop()
    return error_list


def is_order_number(index, text):
    # 判断是不是序号，是的话返回True，反之False
    # 去除 1） 第一条  此类误报, 移除在段落中的误报
    pattern_kuohao_1 = "[\)）][ 0-9ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+"
    pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    pattern_kuohao_2 = "[\)）][a-zA-Z ]+"
    pattern_kuohao_2 = re.compile(pattern_kuohao_2)
    pattern_kuohao_3 = "[\)）][ 0-9\.]+"
    pattern_kuohao_3 = re.compile(pattern_kuohao_3)
    newtext = text[:index + 1][::-1]
    if pattern_kuohao_2.match(newtext):
        # 防止将 goodboy)类排除
        if len(pattern_kuohao_2.match(newtext).group().strip().strip(")").strip()) <= 2:
            return True
    elif pattern_kuohao_3.match(newtext):
        res = pattern_kuohao_3.match(newtext)
        text1 = res.group().strip().strip(")").strip()
        try:
            next_char = newtext[res.span()[1]]
        except:
            next_char = ""

        if next_char in {"+", "-", "*", "/", "÷", "×", "·", "=","﹤","﹥","≦","≧"
                         ,"≡","≮","≯","＋","－","＝","＜","＞","≤","≥","≈","≒",
                         "≠","﹢","﹣","∶","∵","∴","㏒","㏑","∑","∏","∅"}:
            return False
        if "." in text1:
            if len(text1) <= 7:
                return True
        else:
            if len(text1) <= 2:
                return True
    elif pattern_kuohao_1.match(newtext):
        if len(pattern_kuohao_1.match(newtext).group().strip().strip(")").strip()) <= 2:
            return True

    return False


def remove_danyinhao_wubao(i, text, character_end):
    # I’ 用全角单引号的时候会报错，但是如果是法语，是允许的，排除这种误报
    english_pattern = "^[a-zA-Z ]+$"
    english_pattern = re.compile(english_pattern)
    left_text = text[:i][::-1]
    right_text = text[i + 1:]
    left = ""
    right = ""
    for i in left_text:
        if i in character_end:
            break
        if '\u4e00' <= i <= '\u9fff':
            break
        left += i

    for i in right_text:
        if i in character_end:
            break
        if '\u4e00' <= i <= '\u9fff':
            break
        right += i
    # # 没写出正则，只能这样了
    flag_left = english_pattern.match(left)
    flag_right = english_pattern.match(left)
    # 只要有一侧匹配不到英文，直接返回false，不报错
    if (flag_right is None or flag_left is None):
        return False
    left = left[::-1]
    left_words = left.lower().split()
    right_words = right.lower().split()
    flag = False
    try:
        with open("edict.pickle", 'rb') as f:
            engdict = pickle.load(open(f))
    except:
        engdict={}
    for i in left_words + right_words:
        if i not in engdict:
            flag = True
    if flag:
        return False
    return True


def not_english(i, text):
    pattern = "[a-zA-Z àâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ]"
    pattern = re.compile(pattern)
    left = text[:i][::-1]
    right = text[i + 1:]
    left_chars = pattern.match(left)
    right_chars = pattern.match(right)
    if left_chars:
        left_string = left_chars.group()
    else:
        left_string = ""
    if right_chars:
        right_string = right_chars.group()
    else:
        right_string = ""
    try:
        with open("edict.pickle", 'rb') as f:
            english_dict = pickle.load(f)
    except:
        english_dict = {}
    # print(english_dict)
    strings = right_string + " " + left_string
    for word in strings.split():
        if word not in english_dict:
            return True
    return False

# 增加全角标点符号
def is_Chinese_v2(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
        if ch in '“”《》「」【】——……，。！：‘’；？！，（）%〔〕':
            return True
    return False


def remove_chongfu(alist):
    # 在连续错误的情况下，保留第一个错误位置
    index_to_delete = []
    before_l = ""
    before_o = -10
    keep_index = 0

    alist = sorted(alist, key=lambda x: x["offset"])
    for i, temp in enumerate(alist):
        if before_l == temp["lookup"] and temp["offset"] - before_o == 1:
            index_to_delete.append(i)
            alist[keep_index]["content"] += temp["content"]
        else:
            keep_index = i
        before_l = temp["lookup"]
        before_o = temp["offset"]
    index_to_delete.sort(reverse=True)
    for i in index_to_delete:
        alist.pop(i)
    return alist


def remove_chongfu_for_all(alist):
    # 在连续错误的情况下，保留第一个错误位置,区别于上一个，不考虑错误类型
    index_to_delete = []
    before_l = ""
    before_o = -10000000
    keep_index = 0
    length = -100000

    alist = sorted(alist, key=lambda x: x["offset"])
    for i, temp in enumerate(alist):

        if temp["offset"] - before_o == length:
            index_to_delete.append(i)
            alist[keep_index]["content"] += temp["content"]
        else:
            keep_index = i
        before_o = temp["offset"]
        length = len(temp["content"])
    index_to_delete.sort(reverse=True)
    for i in index_to_delete:
        alist.pop(i)
    return alist


def check_punc(text):
    result_list = []
    for every_dict in text:
        Inputtext = every_dict['paragraphContent']
        Inputnumber = every_dict['paragraphNumber']
        Inputpage = every_dict['pageIndex']
        # Inputtext = every_dict['Text']
        # Inputnumber = every_dict['ParagraphIndex']
        # Inputpage = every_dict['PageIndex']
        # try:
        result = check(Inputtext, Inputnumber, Inputpage)
        # except:
        # continue
        result_list = result_list + result
    return result_list


if __name__ == '__main__':
    # check_punc(text)‘’
    text1 = """"""
    text2 = '“sfd f“fds ”发多少”'
    text = [{'paragraphContent': text1, 'paragraphNumber': 1, 'pageIndex': 1}]
    a = check_punc(text)
    for i in a:
        print(i)
        pass
# ‘’
# 自我描述的天才   38
# “'s”，“'m”，“'re”，“'ll”，“s'”,“'t”，单引号一定为英文半角形式， 如果为英文，不做成对检查；
# 中文's这种情况，要怎么处理？
