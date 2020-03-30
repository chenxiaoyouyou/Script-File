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
    chinese_yinhao_nesting = []    # 引号嵌套
    english_yinhao_nesting = []
    traditional_yinhao_nesting = []   # 港台地区引号嵌套
    shuminghao_nesting = []   # 书名号嵌套
    kuohao_nesting_list = []
    chinese_smallkuohao = []  # （）
    li_left_fangkuohao = []  # 〔〕
    li_left_middlekuohao = []  # 【】
    li_left_bigkuohao = []  # {}
    li_left_shuminghao = []  # 《》
    li_allleft_shuminghao = []
    li_left_Chinese_danyinhao = []  # ‘
    li_left_Chinese_shuangyinhao = []  # “
    li_left_jiaohao = []
    li_left_English_danyinhao = []  # '
    li_left_English_shuangyinhao = []  # "
    # li_left_English_smallkuohao = []  # ()
    # li_left_English_middlekuohao = []  # []
    # li_left_English_quanjiao_middlekuohao = []  # []
    # li_left_dan = []
    li_left_allbiaodian = []
    li_left_dianhao = []
    # li_left_dianhao1 = []
    flag_shuangyin = -1
    flag_danyin = -1
    left_must_be_banjiao_yinhao = ['s', 'm', 't']
    left_must_be_banjiao_yinhao_2 = ['re', 'll']
    right_must_be_banjiao_yinhao = ['s']
    all_biaodian = ['.', '。', '!', '！', '?', '？', '…', ':', '：', ';', '、', '；', '—', ',', '，', '·']
    dianhao = ['.', '。', '!', '！', '?', '？', ':', '：', ';', '、', '；', ',', '，']
    yinhao_left = ["'", "\"", "‘", "“"]  # ‘’    “”
    yinhao_right = ["”", "’", "'", '"']
    kuohao_left = ["[", "{", "【", '(', '（', '〔', "［", "《"]
    kuohao_right = ["]", "}", "】", ")", '）', '〕', '］', '》']
    character_end = all_biaodian + yinhao_right + yinhao_left + kuohao_right + kuohao_left
    kuohao = []
    yinhao = []
    flag = 0
    # flag1 = 0

    # 用于配对符号
    yingshe = {'[': ']', ']': '[', '{': '}', '}': '{', '【': '】', '】': '【', '(': ')', ')': '(', '（': '）', '）': '（',
               '〔': '〕', '〕': '〔', '［': '］', '］': '［', '《': '》', '》': '《', "'": "'", '"': '"', "‘": "’", "’": "‘",
               "“": "”", "”": "“"}
    # 排除句首的）
    pattern_kuohao_1 = "[ 0-9.ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+?[\)）]"
    pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    pattern_kuohao_2 = "[a-zA-Z][\)）]"
    pattern_kuohao_2 = re.compile(pattern_kuohao_2)

    # 括号的首位置检查每句话只进行一次
    flag_start = True

    for i, char in enumerate(text):
        if char in [' ', '\t', '\n']:
            continue
        # 判断段首标点符号
        # 需求取消
        # if char in ['.','。','!','！','?','？','……',',','，','：','；',';',':','、'] and flag1 ==0:
        #   error_list.append((page,number,i+1,text[i],'','段首不能出现符号',1))
        # else:
        #   flag1 = 1

        if char in all_biaodian:
            li_left_allbiaodian.append(i)

        if char in ["「", "」", "『", "』"]:
            traditional_yinhao_nesting.append({"i": i, "info": char})
            continue

        # 判断小括号
        # 检查左半边
        if char == '（':
            kuohao_nesting_list.append({"i":i, "info":char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == '）':

            # 句首的直接排除
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue

            kuohao_nesting_list.append({"i":i, "info":char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "（" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == "〔":
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == "〕":
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "〔" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '(':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == ')':
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1

            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "(" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '[':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == ']':
            kuohao_nesting_list.append({"i":i, "info":char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "[" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少[','需补充[',1))
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '［':
            kuohao_nesting_list.append({"i":i, "info":char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == '］':
            kuohao_nesting_list.append({"i":i, "info":char})
            # kuohao.append({"i":i, "info":char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1

            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "［" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少［','需补充［',1))
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '【':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == '】':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1

            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "【" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少【','需补充【',1))
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '{':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == '}':
            kuohao_nesting_list.append({"i":i, "info":char})

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "{" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少{','需补充{',1))
                kuohao.append({"i": i, "info": char, "flag": 0})
            continue

        if char == '“':
            li_left_Chinese_shuangyinhao.append({"i": i, "info": char})
            chinese_yinhao_nesting.append({"i": i, "info": char})
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            yinhao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == '”':
            # print(li_left_Chinese_shuangyinhao)
            if li_left_Chinese_shuangyinhao == []:
                li_left_Chinese_shuangyinhao.append({"i": i, "info": char})
            else:
                if li_left_Chinese_shuangyinhao[-1]["info"] == "“":
                    li_left_Chinese_shuangyinhao.pop()
            chinese_yinhao_nesting.append({"i": i, "info": char})
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_yinhao = yinhao[::-1]
            for iii in temp_yinhao:
                if iii["info"] == "“" and iii["flag"] == 0:
                    yinhao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少“','需补充“',1))
                yinhao.append({"i": i, "info": char, "flag": 0})
            continue
        if char == "<":
            shuminghao_nesting.append({"info": char, "i": i})
            continue
        if  char == ">":
            shuminghao_nesting.append({"info": char, "i": i})
            continue
        if char == '《':
            shuminghao_nesting.append({"info": char, "i": i})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag": 0})
            flag = 1
        # continue
        if char == '》':
            shuminghao_nesting.append({"i": i, "info": char})
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "《" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少《','需补充《',1))
                kuohao.append({"i": i, "info": char, "flag": 0})
        # continue

        if char == '‘':
            chinese_yinhao_nesting.append({"i": i, "info": char})
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            yinhao.append({"i": i, "info": char, "flag": 0})
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
            chinese_yinhao_nesting.append({"i": i, "info": char})
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_yinhao = yinhao[::-1]
            for iii in temp_yinhao:
                if iii["info"] == "‘" and iii["flag"] == 0:
                    yinhao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少‘','需补充‘',1))
                yinhao.append({"i": i, "info": char, "flag": 0})
            continue

        if char ==  "「":
            traditional_yinhao_nesting.append({"info": char, "i":i})
            continue
        if char == "『":
            traditional_yinhao_nesting.append({"info": char, "i":i})
            continue
        if char == "」":
            traditional_yinhao_nesting.append({"info": char, "i":i})
            continue
        if char == "』":
            traditional_yinhao_nesting.append({"info": char, "i":i})
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
            english_yinhao_nesting.append({"i": i, "info": char})
            if len(li_left_English_danyinhao) > 0:
                li_left_English_danyinhao.pop()

                for iii in yinhao:
                    if iii["i"] == flag_danyin:
                        yinhao.remove(iii)
                        flag_danyin = -1
            else:
                li_left_English_danyinhao.append(i)
                # else:
                yinhao.append({"i": i, "info": char, "flag": 0})
                flag_danyin = i
            continue

        if char == '"':
            english_yinhao_nesting.append({"i": i, "info": char})
            if len(li_left_English_shuangyinhao) > 0:
                li_left_English_shuangyinhao.pop()

                for iii in yinhao:
                    if iii["i"] == flag_shuangyin:
                        yinhao.remove(iii)
                        flag_shuangyin = -1
                # print(yinhao)
            else:
                # if flag_shuangyin == 0:
                li_left_English_shuangyinhao.append(i)
                # else:
                yinhao.append({"i": i, "info": char, "flag": 0})
                flag_shuangyin = i
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

    # 判断是搭配错误还是遗漏
    kuohao = sorted(kuohao, key=lambda x: x["i"])
    kuohao = remove_qiantao_kuohao(kuohao, text)
    # print(kuohao)
    flag_temp = -1
    # print(kuohao)
    if len(kuohao) == 1:
        item = kuohao[0]
        error_list.append([page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
    else:
        for i, item in enumerate(kuohao):
            if flag_temp != -1:
                flag_temp = -1
                continue

            if i + 1 != len(kuohao):
                if item["info"] in kuohao_left:
                    if kuohao[i + 1]["info"] in kuohao_right:
                        temp = kuohao[i + 1]
                        if yingshe[item["info"]] != temp["info"]:
                            error_list.append([page, number, item["i"], "", item["info"], "成对标点符号格式须一致", 1])
                            error_list.append([page, number, temp["i"], "", temp["info"], '成对标点符号格式须一致', 1])
                        else:
                            error_list.append(
                                [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
                            error_list.append(
                                [page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1])

                    else:
                        temp = kuohao[i + 1]
                        error_list.append(
                            [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
                        error_list.append(
                            [page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1])
                    flag_temp = 1
                else:
                    error_list.append(
                        [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
            else:
                error_list.append(
                    [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
    # print(error_list)
    yinhao = sorted(yinhao, key=lambda x: x["i"])
    flag_temp = -1
    # print(yinhao)
    if len(yinhao) == 1:
        item = yinhao[0]
        # yinhao_error_list.append(item)
        error_list.append([page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
    else:

        for i, item in enumerate(yinhao):
            if flag_temp != -1:
                flag_temp = -1
                continue
            if i + 1 != len(yinhao):
                if item["info"] in yinhao_left:
                    if yinhao[i + 1]["info"] in yinhao_right:
                        temp = yinhao[i + 1]
                        # yinhao_error_list_for_pair.append(item)
                        # yinhao_error_list_for_pair.append(temp)
                        if yingshe[item["info"]] != temp["info"]:
                            error_list.append([page, number, item["i"], "", item["info"], "成对标点符号格式须一致", 1])
                            error_list.append([page, number, temp["i"], "", temp["info"], '成对标点符号格式须一致', 1])
                        else:
                            # yinhao_error_list_for_pair.append(item)
                            error_list.append(
                                [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
                            error_list.append(
                                [page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1])
                    else:
                        temp = yinhao[i + 1]
                        # yinhao_error_list_for_pair.append(temp)
                        # yinhao_error_list_for_pair.append(item)
                        error_list.append(
                            [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
                        error_list.append(
                            [page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1])
                    flag_temp = 1
                else:
                    # yinhao_error_list_for_pair.append(item)
                    error_list.append(
                        [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])
            else:
                # yinhao_error_list_for_pair.append(item)
                error_list.append(
                    [page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1])

    chinese_yinhao_nesting_error = yinhao_nesting(chinese_yinhao_nesting, label="“")
    english_yinhao_nesting_error = yinhao_nesting(english_yinhao_nesting, label='"')
    shuminghao_nesting_error = yinhao_nesting(shuminghao_nesting, label="《")
    nesting_error = chinese_yinhao_nesting_error + english_yinhao_nesting_error + shuminghao_nesting_error

    kuohao_nesting_error = kuohao_nesting(kuohao_nesting_list)
    for temp1 in kuohao_nesting_error:
        for temp2 in error_list:
            if temp1["i"] == temp2[2]:
                break
        else:
            error_list.append([page, number, temp1["i"], "", temp1["info"], temp1["errmsg"], 2])

    for temp1 in nesting_error:
        for temp2 in error_list:
            if temp1["i"] == temp2[2]:
                if {"i": temp1["i"], "info": temp1["info"]} in li_left_Chinese_shuangyinhao:
                    break
                else:
                    temp2[5] = temp1["errmsg"]
                break
        else:
            error_list.append([page, number, temp1["i"], "", temp1["info"], temp1["errmsg"], 2])

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

    # 清除出可能的 1）误用
    error_list_dict = remove_kuohao_for_xvhao(error_list_dict, text)

    # 判断标点是否连续使用
    # flag_4_wenhao = 0
    # flag_4_tanhao = 0
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


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def yinhao_nesting(yinhao_list, label="“"):
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
    item_last = {"info": ""}     # 上一个状态
    for i in range(length-1):
        item_current = yinhao_list[i]
        if i != 0:
            item_last = yinhao_list[i-1]
        item_next = yinhao_list[i+1]
        if item_current["info"] == item_next["info"]:
            item_current.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            error_list.append(item_current)
            item_next.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            error_list.append(item_next)

        flag = item_last["info"] == right1 or item_last["info"] == ""

        if item_current["info"] == left2 and item_next["info"] == left1 and flag:
            item_current.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            item_next.update(errmsg="{}应写在{}之内".format(left2+right2, left1+right1))
            error_list.append(item_current)
            error_list.append(item_next)

    temp = copy.deepcopy(yinhao_list)
    temp.reverse()
    item_last = {"info": ""}
    for i in range(length-1):
        item_current = temp[i]
        item_next = temp[i+1]
        if i != 0:
            item_last = temp[i - 1]
        flag = item_last["info"] == left1 or item_last["info"] == ""
        if item_current["info"] == right2 and item_next["info"] == right1 and flag:
            item_current.update(errmsg="{}应写在{}之内".format(left2 + right2, left1 + right1))
            item_next.update(errmsg="{}应写在{}之内".format(left2 + right2, left1 + right1))
            error_list.append(item_current)
            error_list.append(item_next)

    return error_list


def kuohao_nesting(kuohao_nesting):

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
    middle_left = {"[", "［", "【"}
    middle_right = {"]", "】", "］"}
    big_left = {"{"}
    big_right = {"}"}
    item_last = {"i":0, "info":""}

    for i in range(length-1):
        item_current = kuohao_nesting[i]
        item_next = kuohao_nesting[i+1]
        if i != 0:
            item_last = kuohao_nesting[i-1]
        if item_current["info"] == item_next["info"]:
            item_current.update(errmsg="套用错误")
            item_next.update(errmsg="套用错误")
            error_list.append(item_current)
            error_list.append(item_next)
        if item_current["info"] in small_left:
            if item_last["info"] in big_left:
                item_current.update(errmsg="套用错误")
                item_last.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_last)
        elif item_current["info"] in middle_left:
            if item_last["info"] in small_left:
                item_current.update(errmsg="套用错误")
                item_last.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_last)
        elif item_current["info"] in big_left:
            if item_last["info"] in small_left or item_last["info"] in middle_left:
                item_current.update(errmsg="套用错误")
                item_last.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_last)
        elif item_current["info"] in small_right:
            if item_next["info"] in big_right:
                item_current.update(errmsg="套用错误")
                item_next.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_next)
        elif item_current["info"] in middle_right:
            if item_next["info"] in small_right:
                item_current.update(errmsg="套用错误")
                item_next.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_next)
        elif item_current["info"] in big_right:
            if item_next["info"] in small_right or item_next["info"] in middle_right:
                item_current.update(errmsg="套用错误")
                item_next.update(errmsg="套用错误")
                error_list.append(item_current)
                error_list.append(item_next)
    # print(error_list)
    return error_list


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


def remove_kuohao_for_xvhao(error_list, text):
    # 去除 1） 第一条  此类误报, 移除在段落中的误报
    pattern_kuohao_1 = "[\)）][ 0-9ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]+"
    pattern_kuohao_1 = re.compile(pattern_kuohao_1)
    pattern_kuohao_2 = "[\)）][a-zA-Z ]+"
    pattern_kuohao_2 = re.compile(pattern_kuohao_2)
    pattern_kuohao_3 = "[\)）][ 0-9\.]+"
    pattern_kuohao_3 = re.compile(pattern_kuohao_3)

    idx_to_remove = []
    for idx, item in enumerate(error_list):
        newtext = text[:item["offset"] + 1][::-1]
        if item["content"] == ")" and item["lookup"] == "需补充(":
            if pattern_kuohao_2.match(newtext):
                if len(pattern_kuohao_2.match(newtext).group().strip().strip(")").strip()) <= 2:
                    idx_to_remove.append(idx)
            elif pattern_kuohao_3.match(newtext):
                res = pattern_kuohao_3.match(newtext).group().strip().strip(")").strip()
                if "." in res:
                    if len(res) <= 7:
                        idx_to_remove.append(idx)
                else:
                    if len(res) <= 2:
                        idx_to_remove.append(idx)
            elif pattern_kuohao_1.match(newtext):
                if len(pattern_kuohao_1.match(newtext).group().strip().strip(")").strip()) <= 2:
                    idx_to_remove.append(idx)

        elif item["content"] == "）" and item["lookup"] == "需补充（":
            if pattern_kuohao_2.match(newtext):
                if len(pattern_kuohao_2.match(newtext).group().strip().strip("）").strip()) <= 2:
                    idx_to_remove.append(idx)
            elif pattern_kuohao_3.match(newtext):
                res = pattern_kuohao_3.match(newtext).group().strip().strip("）").strip()

                if "." in res:
                    if len(res) <= 7:
                        idx_to_remove.append(idx)
                else:
                    if len(res) <= 2:
                        idx_to_remove.append(idx)

            elif pattern_kuohao_1.match(newtext):
                if len(pattern_kuohao_1.match(newtext).group().strip().strip("）").strip()) <= 2:
                    idx_to_remove.append(idx)
    idx_to_remove.sort(reverse=True)
    for i in idx_to_remove:
        error_list.pop(i)
    return error_list


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
    engdict = pickle.load(open("edict.pickle", 'rb'))
    # print(left_words + right_words)
    for i in left_words + right_words:
        if i not in engdict:
            flag = True
    if flag:
        return False
    return True


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
        # try:
        result = check(Inputtext, Inputnumber, Inputpage)
        # except:
        # continue
        result_list = result_list + result
    return result_list


if __name__ == '__main__':
    # check_punc(text)‘’
    text1 = """❅    ………………      （3.7）"""
    text2 = '“sfd f“fds ”发多少”'
    # text3 = "设有n个DMU（），每个DMU都有m种输出，如表3-1所示：为对第i种输入的投入量；为对第k种输出的产出量；为对第i种输入的一种度量（“权”）；为对第k种输出的一种度量（“权”）（j=1,2，…，n；i=1,2，…，m；k=1,2，…，s），而且有：，，，。"
    text = [{'paragraphContent': text1, 'paragraphNumber': 1, 'pageIndex': 1}]
    # print(text1[203:215])
    # print(text2[15])
    a = check_punc(text)
    print(a)
    for i in a:
        print(i)
        pass
# ‘’
# 自我描述的天才   38
# “'s”，“'m”，“'re”，“'ll”，“s'”,“'t”，单引号一定为英文半角形式， 如果为英文，不做成对检查；
# 中文's这种情况，要怎么处理？
