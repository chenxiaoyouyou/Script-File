# coding=utf-8
# -*- coding: utf-8 -*-
import time
import re
import copy
import pickle

"""
增加嵌套规则前的最后一个版本

"""


def check(text, number, page):
    error_list = []
    li_left_smallkuohao = []  # （）
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
    li_left_English_smallkuohao = []  # ()
    li_left_English_middlekuohao = []  # []
    li_left_English_quanjiao_middlekuohao = []  # []
    # li_left_dan = []
    li_left_allbiaodian = []
    li_left_dianhao = []
    li_left_dianhao1 = []
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
    flag1 = 0

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
        # 判断小括号
        # 检查左半边
        if char == '（':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            
            continue
        if char == '）':

            # 句首的直接排除
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] ==0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "（" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == "〔":
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            continue
        if char == "〕":
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "〔" and iii["flag"] == 0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '(':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            continue
        if char == ')':
            if flag_start:
                start_text = text[:i + 1]
                if pattern_kuohao_1.match(start_text) or pattern_kuohao_2.match(start_text):
                    flag_start = False
                    continue

            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1

            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "(" and iii["flag"]==0:
                    kuohao.remove(iii)
                    break
            else:
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '[':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})

            continue
        if char == ']':
            
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
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '［':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            continue
        if char == '］':
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
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '【':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            continue
        if char == '】':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1

            temp_kuohao = kuohao[::-1]
            for iii in temp_kuohao:
                if iii["info"] == "【" and iii["flag"]==0:
                    kuohao.remove(iii)
                    break
            else:
                # error_list.append((page,number,i+1,text[i],'缺少【','需补充【',1))
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '{':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            continue
        if char == '}':
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
                kuohao.append({"i": i, "info": char, "flag":0})
            continue

        if char == '“':
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            yinhao.append({"i": i, "info": char, "flag":0})
            continue
        if char == '”':
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
                yinhao.append({"i": i, "info": char,"flag":0})
            continue

        if char == '《':
            for iii in kuohao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            kuohao.append({"i": i, "info": char, "flag":0})
            flag = 1
        # continue
        if char == '》':
            
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
                kuohao.append({"i": i, "info": char, "flag":0})
        # continue

        if char == '‘':
            for iii in yinhao:
                if iii["info"] == char and iii["flag"] == 0:
                    iii["flag"] = 1
            yinhao.append({"i": i, "info": char, "flag":0})
            continue
        if char == '’':
            # 判断‘s等几个特殊情况
            # 需明确此时的content和lookup
            if text[i + 1:i + 2] in left_must_be_banjiao_yinhao:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append((page, number, i, text[i], "’", "修改为'", 1))
                continue
            if text[i + 1:i + 3] in left_must_be_banjiao_yinhao_2:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append((page, number, i, text[i], "’", "修改为'", 1))
                continue
            if text[i - 1:i] in right_must_be_banjiao_yinhao:
                if remove_danyinhao_wubao(i, text, character_end):
                    error_list.append((page, number, i, text[i], "’", "修改为'", 1))
                continue

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
                yinhao.append({"i": i, "info": char, "flag":0})
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

            if len(li_left_English_danyinhao) > 0:
                li_left_English_danyinhao.pop()

                for iii in yinhao:
                    if iii["i"] == flag_danyin:
                        yinhao.remove(iii)
                        flag_danyin = -1

            else:
                li_left_English_danyinhao.append(i)
                # else:
                yinhao.append({"i": i, "info": char, "flag":0})
                flag_danyin = i
            continue

        if char == '"':
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
                yinhao.append({"i": i, "info": char, "flag":0})
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
                error_list.append((page, number, i - 1, text[i - 1], '、', '删除、', 1))

    # 判断是搭配错误还是遗漏
    kuohao = sorted(kuohao, key=lambda x: x["i"])

    flag_temp = -1
    # print(kuohao)
    if len(kuohao) == 1:
        item = kuohao[0]
        error_list.append((page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
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
                            error_list.append((page, number, item["i"], "", item["info"], "成对标点符号格式须一致", 1))
                            error_list.append((page, number, temp["i"], "", temp["info"], '成对标点符号格式须一致', 1))
                        else:
                            error_list.append((page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
                            error_list.append((page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1))
                        
                    else:
                        temp = kuohao[i + 1]
                        error_list.append(
                            (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
                        error_list.append(
                            (page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1))
                    flag_temp = 1
                else:
                    error_list.append(
                        (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
            else:
                error_list.append(
                    (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))

    yinhao = sorted(yinhao, key=lambda x: x["i"])
    flag_temp = -1
    # print(yinhao)
    if len(yinhao) == 1:
        item = yinhao[0]
        error_list.append((page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))

    else:

        for i, item in enumerate(yinhao):
            if flag_temp != -1:
                flag_temp = -1
                continue
            if i + 1 != len(yinhao):
                if item["info"] in yinhao_left:
                    if yinhao[i + 1]["info"] in yinhao_right:
                        temp = yinhao[i + 1]
                        if yingshe[item["info"]] != temp["info"]:
                            error_list.append((page, number, item["i"], "", item["info"], "成对标点符号格式须一致", 1))
                            error_list.append((page, number, temp["i"], "", temp["info"], '成对标点符号格式须一致', 1))
                        else:
                            error_list.append(
                            (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
                            error_list.append(
                            (page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1))
                    else:
                        temp = yinhao[i + 1]
                        error_list.append(
                            (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
                        error_list.append(
                            (page, number, temp["i"], "", temp["info"], '需补充' + yingshe[temp["info"]], 1))
                    flag_temp = 1
                else:

                    error_list.append(
                        (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))
            else:
                error_list.append(
                    (page, number, item["i"], "", item["info"], '需补充' + yingshe[item["info"]], 1))

    # 判断“但是”之前不能是表示结束的符号。、？、！；
    # if len(li_left_dan) > 0:
    #   for p in li_left_dan:
    #       if p+1 <= len(text)-1:
    #           if text[p+1] == '是' and text[p-1] in  '。？！':
    #               error_list.append((page,number,p,text[p-1],'修改为“，”','',1))

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
    flag_4_wenhao = 0
    flag_4_tanhao = 0
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
            before_3 = text[p_3_start:p_3_end]
            before_2 = text[p_2_start:p_2_end]
            before_1 = text[p_1_start:p_1_end]
            before_0 = text[p]  # 当前
            after_1 = text[p + 1:p + 2]
            after_2 = text[p + 2:p + 3]
            after_3 = text[p + 3:p + 4]
            after_4 = text[p + 4:p + 5]

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
    kuo_eng_small = []
    kuo_chi_small = []
    item_to_remove = []
    for item in error_list_dict:
        if item["content"] == "(":
            kuo_eng_small.append(item)
        elif item["content"] == "（":
            kuo_chi_small.append(item)
        elif item["content"] == ")":
            if len(kuo_eng_small) > 0 and kuo_eng_small[-1]["content"] == "(":
                item_to_remove.append(item)
                item_to_remove.append(kuo_eng_small[-1])
                kuo_eng_small.pop()
        elif item["content"] == "）":
            if len(kuo_chi_small) > 0 and kuo_chi_small[-1]["content"] == "（":
                item_to_remove.append(item)
                item_to_remove.append(kuo_chi_small[-1])
                kuo_chi_small.pop()
    for i in item_to_remove:
        error_list_dict.remove(i)

    return error_list_dict


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


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
    text1 = """[修(订了)发}电机表面油漆外观和附着力的执行标准（见5.3.3，2011年版的5.3.3）"""
    text2 = '“sfd f“fds ”发多少”'
    # text3 = "设有n个DMU（），每个DMU都有m种输出，如表3-1所示：为对第i种输入的投入量；为对第k种输出的产出量；为对第i种输入的一种度量（“权”）；为对第k种输出的一种度量（“权”）（j=1,2，…，n；i=1,2，…，m；k=1,2，…，s），而且有：，，，。"
    text = [{'paragraphContent': text1, 'paragraphNumber': 1, 'pageIndex': 1}]
    # print(text1[203:215])
    # print(text2[15])
    a = check_punc(text)
    for i in a:
        print(i)
        pass
# ‘’
# 自我描述的天才   38
# “'s”，“'m”，“'re”，“'ll”，“s'”,“'t”，单引号一定为英文半角形式， 如果为英文，不做成对检查；
# 中文's这种情况，要怎么处理？
