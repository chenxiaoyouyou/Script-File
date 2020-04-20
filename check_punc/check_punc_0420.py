# coding=utf-8
import re
import copy


def split_cube_for_chinese_yinhao(alist, right_set):
    # 将“ ” “ ‘’ ”， 拆分成 “ ” ， “ ‘’ ”
    if len(alist) <= 2:
        return [alist]
    alist = sorted(alist, key=lambda x: x['i'])
    # left1 = "「"
    # right1 = "」"
    # left2 = "『"
    # right2 = "』"
    # print(alist)
    # left = {"“", "‘", "「", "『"}
    # right = {"”", "’", "」", "』"}
    cube_list = []
    # temp = [alist[0]]
    temp = []
    left = 0
    for i, item in enumerate(alist):
        if item['c'] in right_set:
            left -= 1
            temp.append(item)
        else:
            if left == 0 and temp != []:
                if i != 0:
                    cube_list.append(temp)
                    temp = [item]
                else:
                    temp.append(item)
            else:
                temp.append(item)
            left += 1
    if temp is not []:
        cube_list.append(temp)
    return cube_list


def recur_split(alist, right_set, left_hold, right_hold, final_list):
    # 递归将 “ ‘’ ‘’ ” 拆分成“ ‘’ ”， “ ‘’ ”
    if len(alist) <= 2:
        new_right = right_hold.copy()
        new_right.reverse()
        final_list.append(left_hold + alist + new_right)
    else:
        left_hold.append(alist.pop(0))
        right_hold.append(alist.pop(-1))
        new_alist = split_cube_for_chinese_yinhao(alist, right_set)
        for temp in new_alist:
            recur_split(temp, right_set, left_hold.copy(), right_hold.copy(), final_list)
    return final_list


def split_list(alist, right_set):
    final_list = []
    res = split_cube_for_chinese_yinhao(alist, right_set)
    for i in res:
        if len(i) > 2:
            res1 = recur_split(i, right_set, [], [], [])
            final_list.extend(res1)
        else:
            final_list.append(i)
    return final_list


def check(text, number, page):
    # 错误列表
    error_list = []
    # 繁体引号对
    traditional_pairs = []
    traditional_nesting = []

    # 中英文因为要匹配非对称错误，用一个列表保存
    yinhao_pairs = []         # 判断中英文引号错误
    chinese_yinhao_nesting = []
    english_yinhao_nesting = []

    kuohao_pairs = []        # 判断括号的缺失与搭配不当
    kuohao_nesting = []      # 判断括号的嵌套

    shuminghao_nesting = []  # 书名号
    shuminghao_pairs = []

    li_left_allbiaodian = []
    li_left_dianhao = []

    left_must_be_banjiao_yinhao = {'s', 'm', 't'}
    left_must_be_banjiao_yinhao_2 = {'re', 'll'}
    right_must_be_banjiao_yinhao = {'s'}
    all_biaodian = {'.', '。', '!', '！', '?', '？', '…', ':', '：', ';', '、', '；', '—', ',', '，', '·'}
    dianhao = {'.', '。', '!', '！', '?', '？', ':', '：', ';', '、', '；', ',', '，'}

    # yinhao_left = {"'", "\"", "‘", "“", "\u301D", "＇"}  # ‘’    “”
    # yinhao_right = {"”", "’", "'", '"', "\u301E", "＇"}
    kuohao_left = {"[", "{", "【", '(', '（', '〔', "［", "《", '｛'}
    kuohao_right = {"]", "}", "】", ")", '）', '〕', '］', '》', '｝'}

    # character_end = all_biaodian.union(yinhao_right, yinhao_left, kuohao_right , kuohao_left)
    flag = 0

    # 用于配对符号
    yingshe = {'[': ']', ']': '[', '{': '}', '}': '{', '【': '】', '】': '【', '(': ')', ')': '(', '（': '）', '）': '（',
               '〔': '〕', '〕': '〔', '［': '］', '］': '［', '《': '》', '》': '《', "'": "'", '"': '"', "‘": "’", "’": "‘",
               "“": "”", "”": "“", "｛": "｝", '｝': '｛', "〝": "〞", "〞": "〝", "＇": "＇"}

    # 用于判断是否为全半角错误
    # yingshe_for_quanbanjiao = {
    #     "\uFF09":"\u0028", "\u0029":"\uFF08",      # ()（）
    #     "\u005D":"\uFF3B", "\uFF3D":"\u005B",      # [
    #     "\uFF5D":"\u007B", "\u007D":"\uFF5B",      # {
    #     "\uFF1E": "\u003C",
    #     "\u003E":"\u3008", "\u3009":"\u003C",
    #     "\u301E":"\u201C", "\u201D":"\u301D",
    #     "\uFF63": "\u300C", "\u300D":"\uFF62",
    # }
    # # 排除句首的）
    # pattern_kuohao_1 = "[(（]?[ 0-9.ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+?[\)）]"
    # pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    # pattern_kuohao_2 = "[(（]？[a-zA-Z][\)）]"
    # pattern_kuohao_2 = re.compile(pattern_kuohao_2)

    def add_right_kuohao(punc, is_order=False):

        pair = yingshe.get(punc, None)
        if pair is None:
            return

        if len(kuohao_pairs) > 0:
            item_last1 = kuohao_pairs[-1]
            try:
                item_last2 = kuohao_pairs[-2]
            except:
                item_last2 = {"c": ""}
            if item_last1['c'] == pair:
                # 成对, 全半角成对，不匹配成对
                if is_order:
                    text_n = text[item_last1['i']:i]
                    if len(text_n) > 200:
                        return
                kuohao_nesting.append(item)
                kuohao_nesting.append(kuohao_pairs.pop())
            elif item_last2['c'] == pair:
                kuohao_nesting.append(item)
                kuohao_nesting.append(kuohao_pairs.pop(-2))
            elif item_last1['c'] in kuohao_left:
                if is_order:
                    return None
                kuohao_nesting.append(item)
                kuohao_nesting.append(kuohao_pairs.pop())
            else:
                # 没有左括号
                # 是序号的话不操作，不是的话遗漏
                if is_order:
                    return None
                error_list.append([page, number, i, char, "需补充{}".format(pair), 1])
        else:
            if is_order:
                return None
            error_list.append([page, number, i, char, "需补充{}".format(pair), 1])

    for i, char in enumerate(text):
        if char in [' ', '\t', '\n']:
            continue
        if is_chinese_or_english_char(char):
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

        if char == "\uFF62":
            traditional_pairs.append(item)
            continue
        if char == "\uFF63":
            if len(traditional_pairs) > 0:
                if traditional_pairs[-1]["c"] in {"『", "\uFF62", "「"}:
                    traditional_nesting.append(traditional_pairs[-1])
                    traditional_nesting.append(item)
                    traditional_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充\uFF62", 1])
            else:
                error_list.append([page, number, i, char, "需补充\uFF62", 1])
            continue

        if char == "「":
            traditional_pairs.append(item)
            continue
        if char == "」":
            if len(traditional_pairs) > 0:
                if traditional_pairs[-1]["c"] in {"『", "「", "\uFF62"}:
                    traditional_nesting.append(traditional_pairs[-1])
                    traditional_nesting.append(item)
                    traditional_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充「", 1])
            else:
                error_list.append([page, number, i, char, "需补充「", 1])
            continue
        if char == "『":
            traditional_pairs.append(item)
            continue
        if char == "』":
            # traditional_pairs.append(item)
            if len(traditional_pairs) > 0:
                if traditional_pairs[-1]["c"] in {"「", "『", "\uFF62"}:
                    traditional_nesting.append(traditional_pairs[-1])
                    traditional_nesting.append(item)
                    traditional_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充『", 1])
            else:
                error_list.append([page, number, i, char, "需补充『", 1])
            continue

        # 左〝  右〞
        # 判断引号
        # print(yinhao_pairs)
        if char == '“':
            yinhao_pairs.append(item)
            continue
        if char == '”':
            if len(yinhao_pairs) > 0:
                last_item = yinhao_pairs[-1]
                try:
                    last_item2 = yinhao_pairs[-2]
                except:
                    last_item2 = {"c": ""}
                if last_item['c'] in {"“", "‘", "\u301D"}:
                    chinese_yinhao_nesting.append(last_item)
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop()
                elif last_item2['c'] == "“":
                    chinese_yinhao_nesting.append(last_item2)
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop(-2)
                elif last_item['c'] in {'"', "'"}:
                    error_list.append([page, number, i, char, "成对标点符号格式须一致", 1])
                    error_list.append(
                        [page, number, last_item["i"], last_item["c"], "成对标点符号格式须一致", 1])
                    yinhao_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充“", 1])
            else:
                error_list.append([page, number, i, char, "需补充“", 1])
            continue

        if char == "〝":
            yinhao_pairs.append(item)
            continue
        if char == "〞":
            if len(yinhao_pairs) > 0:
                last_item = yinhao_pairs[-1]
                if last_item['c'] in {"“", "‘", "\u301D"}:
                    chinese_yinhao_nesting.append(last_item)
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充〝", 1])
            else:
                error_list.append([page, number, i, char, "需补充〝", 1])
            continue

        if char == '‘':
            yinhao_pairs.append(item)
            continue
        if char == '’':
            # 判断I's等几个特殊情况
            if len(yinhao_pairs) > 0:
                last_item = yinhao_pairs[-1]
                if last_item['c'] in {"‘", "“"}:
                    chinese_yinhao_nesting.append(last_item)
                    chinese_yinhao_nesting.append(item)
                    yinhao_pairs.pop()
                elif last_item["c"] in {'"', "'"}:
                    error_list.append([page, number, i, char, "成对标点符号格式须一致", 1])
                    error_list.append(
                        [page, number, last_item["i"], last_item["c"], "成对标点符号格式须一致", 1])
                    yinhao_pairs.pop()
                else:
                    if text[i + 1:i + 2] in left_must_be_banjiao_yinhao:
                        # 不是法语的话，将中文引号改为英文引号
                        if not is_french(i, text):
                            error_list.append([page, number, i, text[i], "修改为'", 1])
                        continue
                    if text[i + 1:i + 3] in left_must_be_banjiao_yinhao_2:
                        if not is_french(i, text):
                            error_list.append([page, number, i, text[i], "修改为'", 1])
                        continue
                    if text[i - 1:i] in right_must_be_banjiao_yinhao:
                        if not is_french(i, text):
                            error_list.append([page, number, i, text[i], "修改为'", 1])
                        continue
                    error_list.append([page, number, i, char, "需补充‘", 1])
            else:
                if text[i + 1:i + 2] in left_must_be_banjiao_yinhao:
                    if not is_french(i, text):
                        error_list.append([page, number, i, text[i], "修改为'", 1])
                    continue
                if text[i + 1:i + 3] in left_must_be_banjiao_yinhao_2:
                    if not is_french(i, text):
                        error_list.append([page, number, i, text[i], "修改为'", 1])
                    continue
                if text[i - 1:i] in right_must_be_banjiao_yinhao:
                    if not is_french(i, text):
                        error_list.append([page, number, i, text[i], "’", "修改为'", 1])
                    continue
                # 不是以上情况，则说明遗漏引号
                error_list.append([page, number, i, char, "需补充‘", 1])

        if char == "'" or char == "＇":
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
            if is_french(i, text):
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
            # 判定是否为序号，如果是序号的话，则忽略遗漏的错误
            is_order = is_order_number(i, text)
            add_right_kuohao("）", is_order=is_order)
            continue

        if char == '(':
            kuohao_pairs.append(item)
            continue
        if char == ')':
            is_order = is_order_number(i, text)
            add_right_kuohao(")", is_order=is_order)
            continue

        if char == "〔":
            kuohao_pairs.append(item)
            continue

        if char == "〕":
            is_order = is_order_number(i, text)
            add_right_kuohao("〕", is_order=is_order)
            continue

        if char == "[":
            kuohao_pairs.append(item)
            continue

        if char == "]":
            is_order = is_order_number(i, text)
            add_right_kuohao("]", is_order=is_order)
            continue

        if char == "［":
            kuohao_pairs.append(item)
            continue

        if char == "］":
            is_order = is_order_number(i, text)
            add_right_kuohao("］", is_order=is_order)
            continue

        if char == "【":
            kuohao_pairs.append(item)
            continue

        if char == "】":
            is_order = is_order_number(i, text)
            add_right_kuohao("】", is_order=is_order)
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
            shuminghao_pairs.append(item)
        if char == "》":
            if len(shuminghao_pairs) > 0:
                last_item = shuminghao_pairs[-1]
                if last_item['c'] in {"《", "<", "〈"}:
                    shuminghao_nesting.append(last_item)
                    shuminghao_nesting.append(item)
                    shuminghao_pairs.pop()
                else:
                    error_list.append([page, number, i, char, "需补充《", 1])
            else:
                error_list.append([page, number, i, char, "需补充《", 1])

        if char == "<":
            # if is_compare(i, text):
            #     continue
            shuminghao_pairs.append(item)
            continue
        if char == ">":
            # if is_compare(i, text):
            #     continue
            if len(shuminghao_pairs) > 0:
                last_item = shuminghao_pairs[-1]
                if last_item['c'] in {"《", "<", "〈"}:
                    shuminghao_nesting.append(last_item)
                    shuminghao_nesting.append(item)
                    shuminghao_pairs.pop()

        if char == "〈":
            shuminghao_pairs.append(item)
            continue
        if char == "〉":
            if len(shuminghao_pairs) > 0:
                last_item = shuminghao_pairs[-1]
                if last_item['c'] in {"《", "<", "〈"}:
                    shuminghao_nesting.append(last_item)
                    shuminghao_nesting.append(item)
                    shuminghao_pairs.pop()

        if char == '·':
            li_left_dianhao.append(i)
            continue
        if char == '》':
            flag = 1
            # temp = i
            continue
        if char == '《' and i >= 2 and flag == 1:
            flag = 0
            if text[i - 2] == '》' and text[i - 1] == '、':
                error_list.append([page, number, i - 1, '、', '删除、', 1])

    # 判断括号的遗漏问题
    for item in kuohao_pairs:
        error_list.append([page, number, item["i"], item["c"], "需补充{}".format(yingshe[item["c"]]), 1])

    for item in shuminghao_pairs:
        if item['c'] in {"《", "》"}:
            error_list.append([page, number, item["i"], item["c"], "需补充{}".format(yingshe[item["c"]]), 1])

    # 判断繁体引号
    for item in traditional_pairs:
        if item["c"] == "「":
            error_list.append([page, number, item["i"], item["c"], "需补充」", 1])
        elif item["c"] == "『":
            error_list.append([page, number, item["i"], item["c"], "需补充』", 1])
        else:
            error_list.append([page, number, item["i"], item["c"], "需补充\uFF63", 1])

    if len(traditional_nesting) >= 2:
        traditional_nesting_errors = c_yinhao_nesting_check(traditional_nesting, text, label="「", yingshe=yingshe)
        for temp1 in traditional_nesting_errors:
            if "成对" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], text[temp1['i']], temp1["errmsg"], 1])
            else:
                error_list.append([page, number, temp1["i"], text[temp1['i']], temp1["errmsg"], 2])

    # 判断中英文引号的匹配问题
    # print(yinhao_pairs)
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
                error_list.append([page, number, item_current["i"], item_current["c"], "成对标点符号格式须一致", 1])
                error_list.append([page, number, item_next["i"], item_next["c"], "成对标点符号格式须一致", 1])
                flag=True
                if i + 2 == len(yinhao_pairs):
                    # 走到这一步，说明最后一个item已经判断
                    flag1 = False
                continue
            else:
                error_list.append([page, number, item_current["i"], text[item_current['i']], "需补充{}".format(yingshe[text[item_current['i']]]), 1])
        if flag1:
            error_list.append(
                [page, number, yinhao_pairs[-1]["i"], text[yinhao_pairs[-1]["i"]], "需补充{}".format(yingshe[text[yinhao_pairs[-1]["i"]]]), 1])

    # 判断英文引号的嵌套
    if len(english_yinhao_nesting) >= 2:
            english_yinhao_nesting_errors = e_yinhao_nesting_check(english_yinhao_nesting)
            for temp1 in english_yinhao_nesting_errors:
                error_list.append([page, number, temp1["i"], temp1["c"], temp1["msg"], 2])

    # 判断中文引号的嵌套
    if len(chinese_yinhao_nesting) >= 2:
        chinese_yinhao_nesting_errors = c_yinhao_nesting_check(chinese_yinhao_nesting, text, label="“", yingshe=yingshe)
        for temp1 in chinese_yinhao_nesting_errors:
            if "之内" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], text[temp1["i"]], temp1["errmsg"], 2])
            else:
                error_list.append([page, number, temp1["i"], text[temp1["i"]], temp1["errmsg"], 1])

    # 判断书名号的嵌套
    if len(shuminghao_nesting) >= 2:
        shuminghao_nesting_errors = shuminghao_check(shuminghao_nesting, text)
        for temp1 in shuminghao_nesting_errors:
            if "之内" in temp1["errmsg"]:
                error_list.append([page, number, temp1["i"], text[temp1["i"]], temp1["errmsg"], 2])
            else:
                error_list.append([page, number, temp1["i"], text[temp1["i"]], temp1["errmsg"], 1])

    # 括号错误
    # 可以先统一为半角，然后在进行全半角计算
    if len(kuohao_nesting) >= 2:
        kuohao_nesting_errors = kuohao_nesting_check(kuohao_nesting, kuohao_left, kuohao_right, yingshe, text)

        for item in kuohao_nesting_errors:
            if "套用" in item["errmsg"]:
                error_list.append([page, number, item["i"], text[item["i"]], item["errmsg"], 2])
            else:
                error_list.append([page, number, item["i"], text[item["i"]], item["errmsg"], 1])

    error_list_dict = []
    for err in error_list:
        dict_err = {}
        dict_err['pageIndex'] = err[0]
        dict_err['paragraphIndex'] = err[1]
        dict_err['offset'] = err[2]
        dict_err['content'] = err[3]
        dict_err['lookup'] = err[4]
        dict_err['errortype'] = err[5]
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

        # 排除 James A.，类误报
        if con == ".," or con == ".." or con==".，" or con == ".。":
            if is_name(item, text):
                idx_to_remove.append(idx)

    idx_to_remove.sort(reverse=True)
    for i in idx_to_remove:
        lian_xv_cuo_wu.pop(i)



    error_list_dict.extend(lian_xv_cuo_wu)
    error_list_dict.sort(key=lambda x: x["offset"])
    return error_list_dict


def is_french(i, text):
    # 通过法语字符简单判断是否为法语
    pattern = "[a-zA-Z àâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ]+"
    pattern = re.compile(pattern)
    french_char_set = set([i for i in "àâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ"])
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
    strings = right_string + " " + left_string
    for char in strings:
        if char in french_char_set:
            return True
    return False


def is_order_number(index, text):
    # 判断是不是序号，是的话返回True，反之False
    # 去除 1） 第一条  此类误报, 移除在段落中的误报
    pattern_kuohao_1 = "[ 0-9ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+"
    pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    pattern_kuohao_2 = "[a-zA-Z ]+"
    pattern_kuohao_2 = re.compile(pattern_kuohao_2)
    pattern_kuohao_3 = "[ 0-9\.]+"
    pattern_kuohao_3 = re.compile(pattern_kuohao_3)

    # 括号之前的字符
    newtext = text[:index][::-1]
    if pattern_kuohao_2.match(newtext):
        # 防止将 goodboy)类排除'
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


def is_chinese_or_english_char(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    if "a" <= char <= "z":
        return True
    if "A" <= char <= "Z":
        return True
    return False


def is_compare(i, text):
    # 判断尖括号是不是大于小于号
    # 比较一般发生在数字和变量之前
    pattern_variable = "[A-Za-z 0-9\.+-_]+"
    pattern_digit = '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?[\)）]?'
    left = text[:i][::-1]
    right = text[i+1:]
    pattern_digit = re.compile(pattern_digit)
    pattern_variable = re.compile(pattern_variable)
    variable_left = pattern_variable.match(left)
    variable_right = pattern_variable.match(right)

    if variable_left:
        variable_left_string = variable_left.group().strip()
        # 只有一个单词，认为是变量
        variable_left_list = variable_left_string.strip()
        if len(variable_left_list) == 1:
            var_left = True
        else:
            var_left = False
    else:
        var_left = False

    if variable_right:
        variable_right_string = variable_right.group().strip()
        variable_right_list = variable_right_string
        if len(variable_right_list) == 1:
            var_right = True
        else:
            var_right = False
    else:
        var_right = False

    digit_left = pattern_digit.match(left)
    digit_right = pattern_digit.match(right)

    if var_left and digit_right:
        return True
    if var_left and var_right:
        return True
    if digit_left and digit_right:
        return True
    if digit_left and var_right:
        return True
    return False


def c_yinhao_nesting_check(yinhao_list,text, label="“", yingshe=None):
    """中文引号嵌套检查"""
    if label == "“":
        for i in yinhao_list:
            if i['c'] == "〝":
                i['c'] = "“"
            elif i['c'] == "〞":
                i['c'] = "”"
        left1 = "“"
        right1 = "”"
        left2 = "‘"
        right2 = "’"
        right_set = {"”", "’"}
    else:
        for i in yinhao_list:
            if i['c'] == "\uFF62":
                i['c'] = "「"
            elif i['c'] == "\uFF63":
                i['c'] = "」"

        left1 = "「"
        right1 = "」"
        left2 = "『"
        right2 = "』"
        right_set = {"」", "』"}

    # left = {"‘", "“", "「", "『"}
    # right = {"’", "”", "」", "』"}
    yinhao_list = sorted(yinhao_list, key=lambda x: x["i"])
    error_list = []
    errmsg = "{}应写在{}之内".format(left2+right2, left1+right1)
    errmsg1 = "成对标点符号格式须一致"
    yinhao_list = split_list(yinhao_list, right_set)

    for pair_list in yinhao_list:
        if len(pair_list) == 2:
            ll, rr = pair_list
            if ll['c'] == left2 and rr['c'] == right2:

                if is_one_sentence(text[ll['i']+1: rr['i']], flag=False):
                    ll['errmsg'] = errmsg
                    rr['errmsg'] = errmsg
                else:
                    ll["errmsg"] = "需补充{}".format(yingshe[ll['c']])
                    rr["errmsg"] = "需补充{}".format(yingshe[rr['c']])

                error_list.append(ll)
                error_list.append(rr)
            elif ll['c'] == left1 and rr['c'] == right2:
                new_text = text[ll['i']+1:rr['i']]
                # 中间有句子终止符，不判定是否在一句话中
                if is_one_sentence(new_text, flag=False):
                    ll['errmsg'] = errmsg1
                    rr['errmsg'] = errmsg1
                else:
                    ll['errmsg'] = "需补充{}".format(yingshe[ll['c']])
                    rr['errmsg'] = "需补充{}".format(yingshe[rr['c']])

                error_list.append(ll)
                error_list.append(rr)
            elif ll['c'] == left2 and rr['c'] == right1:
                if is_one_sentence(text[ll['i']+1:rr['i']], flag=False):

                    ll['errmsg'] = errmsg1
                    rr['errmsg'] = errmsg1
                else:
                    ll['errmsg'] = "需补充{}".format(yingshe[ll['c']])
                    rr['errmsg'] = "需补充{}".format(yingshe[rr['c']])
                error_list.append(ll)
                error_list.append(rr)
            else:
                if is_one_sentence(text[ll['i'] + 1:rr['i']], flag=True):
                    pass
                else:
                    ll['errmsg'] = "需补充{}".format(yingshe[ll['c']])
                    rr['errmsg'] = "需补充{}".format(yingshe[rr['c']])
                    error_list.append(ll)
                    error_list.append(rr)

        elif len(pair_list) == 4:
            item_last2, item_last1, item_current, item_next = pair_list
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
                    error_list.extend([item_last1])
                # “ ‘ ” ”
                elif item_last1['c'] == left2 and item_current['c'] == right1:
                    item_current["errmsg"] = errmsg
                    error_list.extend([item_current])
            # ‘ ’
            elif item_last2["c"] == left2 and item_next['c'] == right2:

                #  ‘ ‘ ’ ’
                if item_last1['c'] == left2 and item_current['c'] == right2:
                    item_last2["errmsg"] = errmsg
                    item_next["errmsg"] = errmsg
                    error_list.extend([item_last2, item_next])
                # ‘ “ ” ’
                else:
                    #  “ ‘ “ ” ’ ”
                    item_last2["errmsg"] = errmsg
                    item_last1["errmsg"] = errmsg
                    item_current["errmsg"] = errmsg
                    item_next["errmsg"] = errmsg
                    error_list.extend([item_last2, item_last1, item_current, item_next])
            # “ ’
            elif item_last2["c"] == left1 and item_next['c'] == right2:
                # “ ‘ ” ’
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            # ‘ ”
            elif item_last2["c"] == left2 and item_next['c'] == right1:
                # ‘ ‘ ” ”
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
        else:
            i = 0
            while len(pair_list) > 0:
                ss = pair_list[0]
                ee = pair_list[-1]
                if i % 2 == 0:
                    if ss['c'] == left1 and ee['c'] == right1:
                        pass
                    else:
                        for item in pair_list:
                            item["errmsg"] = errmsg
                            error_list.append(item)
                else:
                    if ss['c'] == left2 and ee['c'] == right2:
                        pass
                    else:
                        if len(pair_list) == 2:
                            a1, a2 = pair_list
                            if a1['c'] == left1 and a2['c'] == right2:
                                a1["errmsg"] = errmsg
                                error_list.append(a1)
                            elif a1['c'] == left2 and a2['c'] == right1:
                                a2["errmsg"] = errmsg
                                error_list.append(a2)
                        else:
                            for item in pair_list:
                                item["errmsg"] = errmsg
                                error_list.append(item)
                i += 1
                pair_list.pop(0)
                pair_list.pop(-1)

    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list


def is_one_sentence(text, flag=True):
    # flag=True代表双引号的正常使用，False不是
    if len(text) == 0:
        return True
    end_of_sen = {"。", "?", "？", "!", "！"}
    last_char = text[-1]
    if last_char in end_of_sen:
        return True
    else:
        if flag:
            return True
        else:
            for char in text:
                if char in end_of_sen:
                    return False
            return True


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


def shuminghao_check(shuminghao_list, text):

    for i in shuminghao_list:
        if i['c'] == "\u3008":
            i['c'] = "<"
        elif i['c'] == "\u3009":
            i['c'] = ">"

    right_set = {">", "》"}
    left1 = "《"
    right1 = "》"
    left2 = "<"
    right2 = ">"
    # left = {"‘", "“", "「", "『"}
    # right = {"’", "”", "」", "』"}
    yinhao_list = sorted(shuminghao_list, key=lambda x: x["i"])

    error_list = []
    errmsg = "{}应写在{}之内".format(left2+right2, left1+right1)
    errmsg1 = "成对标点符号格式须一致"
    yinhao_list = split_list(yinhao_list, right_set)

    for pair_list in yinhao_list:
        if len(pair_list) == 2:
            ll, rr = pair_list
            if ll['c'] == left2 and rr['c'] == right2:
                # continue
                # 有一个是大于小于号的话，跳过
                if is_compare(ll['i'], text) or is_compare(rr['i'], text):
                    continue
                ll['errmsg'] = errmsg
                rr['errmsg'] = errmsg
                error_list.append(ll)
                error_list.append(rr)
            elif ll['c'] == left1 and rr['c'] == right2:
                is_com = is_compare(rr['i'], text)
                if is_com:
                    ll["errmsg"] = "需补充》"
                    error_list.append(ll)
                else:
                    ll['errmsg'] = errmsg1
                    rr['errmsg'] = errmsg1
                    error_list.append(ll)
                    error_list.append(rr)
            elif ll['c'] == left2 and rr['c'] == right1:
                if is_compare(ll['i'], text):
                    rr['errmsg'] = "需补充《"
                else:
                    ll['errmsg'] = errmsg1
                    rr['errmsg'] = errmsg1
                    error_list.append(ll)
                    error_list.append(rr)
        elif len(pair_list) == 4:
            item_last2, item_last1, item_current, item_next = pair_list
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
                    error_list.extend([item_last1])
                # “ ‘ ” ”
                elif item_last1['c'] == left2 and item_current['c'] == right1:
                    item_current["errmsg"] = errmsg
                    error_list.extend([item_current])
            # ‘ ’
            elif item_last2["c"] == left2 and item_next['c'] == right2:

                #  ‘ ‘ ’ ’
                if item_last1['c'] == left2 and item_current['c'] == right2:
                    item_last2["errmsg"] = errmsg
                    item_next["errmsg"] = errmsg
                    error_list.extend([item_last2, item_next])
                # ‘ “ ” ’
                else:
                    #  “ ‘ “ ” ’ ”
                    item_last2["errmsg"] = errmsg
                    item_last1["errmsg"] = errmsg
                    item_current["errmsg"] = errmsg
                    item_next["errmsg"] = errmsg
                    error_list.extend([item_last2, item_last1, item_current, item_next])
            # “ ’
            elif item_last2["c"] == left1 and item_next['c'] == right2:
                # “ ‘ ” ’
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
            # ‘ ”
            elif item_last2["c"] == left2 and item_next['c'] == right1:
                # ‘ ‘ ” ”
                item_last2["errmsg"] = errmsg
                item_last1["errmsg"] = errmsg
                item_current["errmsg"] = errmsg
                item_next["errmsg"] = errmsg
                error_list.extend([item_last2, item_next, item_last1, item_current])
        else:
            i = 0
            while len(pair_list) > 0:
                ss = pair_list[0]
                ee = pair_list[-1]
                if i % 2 == 0:
                    if ss['c'] == left1 and ee['c'] == right1:
                        pass
                    else:
                        for item in pair_list:
                            item["errmsg"] = errmsg
                            error_list.append(item)
                else:
                    if ss['c'] == left2 and ee['c'] == right2:
                        pass
                    else:
                        if len(pair_list) == 2:
                            a1, a2 = pair_list
                            if a1['c'] == left1 and a2['c'] == right2:
                                a1["errmsg"] = errmsg
                                error_list.append(a1)
                            elif a1['c'] == left2 and a2['c'] == right1:
                                a2["errmsg"] = errmsg
                                error_list.append(a2)
                        else:
                            for item in pair_list:
                                item["errmsg"] = errmsg
                                error_list.append(item)
                i += 1
                pair_list.pop(0)
                pair_list.pop(-1)

    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list


def kuohao_nesting_check(kuohao_nesting, kuo_left, kuo_right, yingshe, text):
    kuohao_nesting = sorted(kuohao_nesting, key=lambda x: x['i'])
    error_list = []
    # length = len(kuohao_nesting)
    # print(kuohao_nesting)
    # 中文圆括号（）：又叫小括号，编码FF08和FF09
    # 西文圆括号()：又叫小括号，编码0028和0029
    # 中文方括号［］：又叫中括号，编码FF3B和FF3D
    # 西文方括号[]：又叫中括号，编码005B和005D
    # 六角括号〔〕：编码3014和3015
    # 方头括号【】：编码3010和3011
    # 大括号｛｝：编码FF5B和FF5D
    kuohao_list = split_list(kuohao_nesting, kuo_right)
    errmsg = "成对标点符号格式须一致"
    errmsg1 = "套用错误"
    # print(kuohao_list)
    # 把所有全角转化为半角括号，然后判断嵌套类错误
    quan_to_ban = {"\uFF08": "\u0028", "\uFF09": "\u0029",
                   "\uFF3B": "\u005B", "\uFF3D": "\u005D",
                   "\uFF5B": "\u007B", "\uFF5D": "\u007D",}

    # 将全角转化为半角
    for i in kuohao_nesting:
        if i['c'] in quan_to_ban:
            i['c'] = quan_to_ban[i['c']]

    # 匹配数学公式
    math_type = '^[a-zA-Z0-9\.∶\-≦≈÷=∑∏≮∴＝﹣﹢﹤≤·＜＋/≡＞*㏒－∵+≠﹥≧≒≯㏑×≥∅\(\)\[\]\{\}｛｝（）］［\s]+$'
    math_pattern = re.compile(math_type)
    chars_pattern = re.compile("^[a-zA-Z ]$")

    for pair_list in kuohao_list:
        if len(pair_list) == 2:
            i0, i1 = pair_list
            if yingshe[i0['c']] == i1['c']:
                # 正确
                continue
            # elif yingshe_for_quanbanjiao[i0['c']] == i1['c']:
                # 全半角错误
                # continue
            else:
                i0['errmsg'] = errmsg
                i1['errmsg'] = errmsg
                error_list.extend([i0, i1])
        else:
            middle_text = text[pair_list[0]['i']:pair_list[-1]['i']+1]
            # 判断中间是否是数学公式
            math_match = math_pattern.match(middle_text)
            chars_match = chars_pattern.match(middle_text)
            # print(math_match)
            if math_match and not chars_match:
                #
                if len(pair_list) <= 4:
                    astr = {"{[()]}", "{[]}", "[()]"}
                    kuohao_in_use = "".join([i['c'] for i in pair_list])
                    if kuohao_in_use not in astr:
                        for item in pair_list:
                            item["errmsg"] = errmsg1
                            error_list.append(item)
                else:
                    # length = len(pair_list)
                    # num = (len(pair_list) - 4) // 2
                    astr = {"[()]", "[]"}
                    while pair_list[0]['c'] == "{" and pair_list[-1]['c'] == "}":
                        pair_list.pop(0)
                        pair_list.pop(-1)
                    kuohao_in_use = "".join([i['c'] for i in pair_list])
                    if kuohao_in_use not in astr:
                        for item in pair_list:
                            item["errmsg"] = errmsg1
                            error_list.append(item)

            else:

                start = pair_list.pop(0)
                end = pair_list.pop(-1)

                if yingshe[start['c']] != end['c']:

                    temp_text = text[start['i']+1:end['i']]
                    if "。" in temp_text or '？' in temp_text or "！" in temp_text:
                        start["errmsg"] = "需补充{}".format(yingshe[start['c']])
                        end['errmsg'] = '需补充{}'.format(yingshe[end['c']])
                    else:
                        start['errmsg'] = errmsg
                        end['errmsg'] = errmsg
                    error_list.extend([start, end])

                while len(pair_list) > 0:
                    ss = pair_list.pop(0)
                    ee = pair_list.pop(-1)
                    if yingshe[ss['c']] != ee['c']:
                        ss["errmsg"] = errmsg
                        ee['errmsg'] = errmsg
                        error_list.extend([ss, ee])

                    if ss['c'] == start['c'] and ee['c'] == end['c']:
                        ss["errmsg"] = errmsg1
                        ee["errmsg"] = errmsg1
                        error_list.append(ss)
                        error_list.append(ee)
                    start = ss
                    end = ee
    error_list = sorted(error_list, key=lambda x: x["i"])
    new_list = []
    idx = set()
    for i, item in enumerate(error_list):
        if item["i"] not in idx:
            new_list.append(item)
            idx.add(item["i"])
    return new_list


def remove_chongfu_for_all(alist):
    # 在连续错误的情况下，保留第一个错误位置,区别于上一个，不考虑错误类型
    index_to_delete = []
    # before_l = ""
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


def is_name(item, text):
    new_text = text[:item['offset']]
    pattern = re.compile("[a-z]*?[A-Z] ")
    if pattern.match(new_text[::-1]):
        return True
    return False


def check_punc(text):
    result_list = []
    for every_dict in text:
        Inputtext = every_dict['paragraphContent']
        Inputnumber = every_dict['paragraphNumber']
        Inputpage = every_dict['pageIndex']
        # Inputtext = every_dict['Text']
        # Inputnumber = every_dict['ParagraphIndex']
        # Inputpage = every_dict['PageIndex']
        try:
            result = check(Inputtext, Inputnumber, Inputpage)
        except:
            result = []
        result_list = result_list + result
    return result_list


if __name__ == '__main__':
    # check_punc(text)‘’
    # '^[a-zA-Z ]*[0-9\.∶-≦≈÷=∑∏≮∴＝﹣﹢﹤≤·＜＋/≡＞*㏒－∵+≠﹥≧≒≯㏑×≥∅\(\)\[\]\{\}｛｝（）］［]+$
    text1 = """司汤达，,这个所有自我中心主义者中的自我中心主义者，有这种勇敢，令灵魂感到愉悦的是，看到他如何大胆地冲向他的时代，一个人面对众人，看到他用令人眼花缭乱的招数和粗暴的攻击穿越了半个世纪一路厮杀，除了他那闪电般的高傲别无什么盔甲可言，他受伤了，从许多隐蔽的伤口里流出血来。但他直到最后一刻巍然挺立，没有放弃一丝一毫的特性和主见。对立是他的禀性，独立是他的狂喜。可以查阅成百的事例，看到这个坚定的投石党人多么强悍多么放肆地去抗拒一种普遍的观点，多么勇敢地去向它提出挑战。在一个一切都为战役而心醉神迷的时代，如他所说的，在法国人们“把英雄气概的概念无法拒绝地与鼓手长联在一起”的时代，他却把滑铁卢之战当做是各种混乱力量搅成乱糟糟的一团来加以描述。他毫无顾忌地承认，在远征俄国（历史学家称这是世界历史上的史诗）期间，他感到无聊至极。他不羞于证实，前往意大利的一次再会情人之旅，要比祖国的命运重要得多；莫扎特的一个咏叹调要比一次政治危机更为有趣。“他才不管征服呢”，法国被外国军队占领，这与他何干，因为他早就是一个泛欧主义者，一个世界主义者，他连一分钟也不去关心战争运气的疯狂更迭，时髦的观点，爱国主义（“最愚蠢的笑柄”）和民族主义，而唯一关心的是使他的精神本性成为真实成为现实。在世界历史的可怖的雪崩中他强调他的这种个人的东西是那样的自负和温柔，这使人们在读他的日记时，都不时感到怀疑，他在所有这些历史性的日子里是否真的是在场的证人。但在某种意义上司汤达确也根本就不在场，甚至是在战争中骑马驰骋或坐在办公桌前，他也只是自己跟自己在一起。他从没有感到出于装模作样，出于感同身受而有义务从心灵上去参与到事件中去，这些事件无法从心灵上触动他；正如歌德在具有历史意义的（日子里，在《年记》中只写下他阅读中文读物的文字一样。司汤达在他的时代中令世界为之震动的时刻里唯一记下的是他最最个人的重要事情：他的时代的历史和他的历史如同有着另外一种字母和另外一种词汇。因此，司汤达成了他的周围世界的一个不可信的证人，这就如他是他个人世界的一个出色的证人一样。对于他），这个最完美的，最值得称赞的和出色的自我中心主义者而言，所有的事件无一例外地和唯一地都归结为感情，这是司汤达―贝尔，这个一次性的和不再复归的个体，从世界进程中所体验和所经历426 精神世界的缔造者的感情。或许从没有一个艺术家为了他的自我，比这个英雄的和坚定的自我中心者更顽强地、更激烈地、更耽于幻想地生活过，更艺术地去发展本我。"""
    text2 = '<都是>'
    text = [{'paragraphContent': text1, 'paragraphNumber': 1, 'pageIndex': 1}]
    a = check_punc(text)
    for i in a:
        print(i)
        # pass

