# coding=utf-8


def check(text, number, page):

    smallkuohao = []
    fangkuohao = []
    dakuohao = []
    jiankuohao = []
    danshuminghao = []
    shuangyinhao = []
    fantiyinhao = []
    error_list = []
    errmsg = "成对标点符号格式须一致"

    def find(alist, current, pair, pair1=None):
        if len(alist) > 0:
            last_item = alist[-1]
            if last_item['c'] == pair:
                error_list.append([page, number, current['i'], current['c'], errmsg, 1])
                error_list.append([page, number, last_item['i'], last_item['c'], errmsg, 1])
                # if current['c'] == '
                return alist.pop()
            elif pair1 is not None:
                if last_item['c'] == "<":
                    return alist.pop()
        return None

    for i, char in enumerate(text):
        item = {'i': i, 'c': char}
        if char == "\uFF08":
            smallkuohao.append(item)
            continue
        if char == "\u0028":
            smallkuohao.append(item)
            continue
        if char == "\uFF09":
            find(smallkuohao, item, "\u0028")
            continue
        if char == "\u0029":
            find(smallkuohao, item, "\uFF08")
            continue
        if char == "\uFF3B" or char == "\u005B":
            fangkuohao.append(item)
            continue
        if char == "\uFF3D":
            find(fangkuohao, item, "\u005B")
            continue
        if char == "\u005D":
            find(fangkuohao, item, "\uFF3B")
            continue

        if char == "\uFF5B" or char == "\u007B":
            dakuohao.append(item)
            continue
        if char == "\uFF5D":
            find(dakuohao, item, "\u007B")
            continue
        if char == "\u007D":
            find(dakuohao, item, "\uFF5B")
            continue

        if char == "\uFF1C" or char == "\u003C" or char == "\u3008":
            jiankuohao.append(item)
            # continue
        if char == "\uFF1E":
            if len(jiankuohao) > 0:
                last_item = jiankuohao[-1]
                if last_item['c'] == "\u003c":
                    error_list.append([page, number, item['i'], item['c'], errmsg, 1])
                    error_list.append([page, number, last_item['i'], last_item['c'], errmsg, 1])
                    jiankuohao.pop()
                    # continue
                elif last_item['c'] == "\uFF1C":
                    jiankuohao.pop()
            continue
        if char == "\u3009":
            print(jiankuohao)
            if len(jiankuohao) > 0:
                last_item = jiankuohao[-1]
                if last_item['c'] == "\u003c":
                    error_list.append([page, number, item['i'], item['c'], errmsg, 1])
                    error_list.append([page, number, last_item['i'], last_item['c'], errmsg, 1])
                    jiankuohao.pop()
                    # continue
                elif last_item['c'] == "\u3008":
                    jiankuohao.pop()
                    # continue
            continue
        if char == '\u003E':
            if len(jiankuohao) > 0:
                last_item = jiankuohao[-1]
                if last_item['c'] in {"\u3008", "\uFF1C"}:
                    error_list.append([page, number, item['i'], item['c'], errmsg, 1])
                    error_list.append([page, number, last_item['i'], last_item['c'], errmsg, 1])
                    jiankuohao.pop()
                    # continue
                elif last_item['c'] == "\u003C":
                    jiankuohao.pop()
                    # continue
            continue
            # res1 = find(jiankuohao, item, "\u003C")
            # if res1 is not None:
            #     if res1 in danshuminghao:
            #         danshuminghao.remove(res1)
            # continue
        # if char == "\u003E":
        #     res1 = find(jiankuohao, item, "\uFF1C", pair1=True)
        #     if res1 is not None:
        #         if res1 in danshuminghao:
        #             danshuminghao.remove(res1)
        #         continue
            # continue

        # if char == "\u3008" or char == "\u003C":
        #     danshuminghao.append(item)
        #     continue
        # if char == "\u3009":
        #     res1 = find(danshuminghao, item, "\u003C")
        #     if res1 is not None:
        #         if res1 in jiankuohao:
        #             jiankuohao.remove(res1)
        #     continue
        # if char == "\u003E":
        #     find(danshuminghao, item, "\u3008")
        #     continue

        if char == "\u201C" or char == "\u301D":
            shuangyinhao.append(item)
            continue
        if char == "\u201D":
            find(shuangyinhao, item, "\u301D")
            continue
        if char == "\u301E":
            find(shuangyinhao, item, "\u201C")
            continue

        if char == "\u300C" or char == "\uFF62":
            fantiyinhao.append(item)
            continue
        if char == "\u300D":
            find(fantiyinhao, item, "\uFF62")
            continue
        if char == "\uFF63":
            find(fantiyinhao, item, "\u300C")
            continue

    error_list_dict = []
    for err in error_list:
        dict_err = {}
        dict_err['pageIndex'] = err[0]
        dict_err['paragraphIndex'] = err[1]
        dict_err['offset'] = err[2]
        dict_err['content'] = err[3]
        dict_err['lookup'] = err[4]
        dict_err['errortype'] = err[5]
        dict_err["rule"] = "全半角检查"
        error_list_dict.append(dict_err)
    error_list_dict.sort(key=lambda x: x['offset'])
    return error_list_dict


def check_quanbanjiao(text):
    result_list = []
    for every_dict in text:
        Inputtext = every_dict['paragraphContent']
        Inputnumber = every_dict['paragraphNumber']
        Inputpage = every_dict['pageIndex']
        # Inputtext = every_dict['Text']
        # Inputnumber = every_dict['ParagraphIndex']
        # Inputpage = every_dict['PageIndex']
        result = check(Inputtext, Inputnumber, Inputpage)
        result_list = result_list + result
    return result_list


if __name__ == '__main__':
    # check_punc(text)‘’
    # '^[a-zA-Z ]*[0-9\.∶-≦≈÷=∑∏≮∴＝﹣﹢﹤≤·＜＋/≡＞*㏒－∵+≠﹥≧≒≯㏑×≥∅\(\)\[\]\{\}｛｝（）］［]+$
    text1 = """尖括号，ꂆ＜₪做自己工作室的奴隶，因为加于自身的责任而不得自由，并受到规章制度和人间事务的束缚ꂆ＞₪做自己工作室的奴隶<只有非创造性的人能够无拘无束，挥霍浪费，成为为生活而生活的纯粹享受者>，做自己工作室的奴隶，因为加于自身的责任而不得自由，并受到规章制度和人间事务的束缚。ꂆ＜₪给自己确立了目标的人会忽略偶然事件：每个艺术家多半都只能表现他耽搁掉亲身经历的事情ꂆ>₪，做自己工作室的奴隶，ꂆ<₪并受到规章制度和人间事务的束缚。ꂆ＞₪给自己确立了目标的人会忽略偶然事件：每个艺术家多半都只能表现他耽搁掉亲身经历的事情。
单书名号，〈生活而生活的纯粹享受者。给自己确立了目标的人会忽略偶然事件：每个艺术家多半都只能表现他耽搁掉亲身经历的事情〉。<但是那些轻浮放荡的享乐者，也就是艺术家的对手们，他们几乎总是缺乏塑造丰富多彩的经历的能力>生活而生活的纯粹享受者。ꂆ〈₪给自己确立了目标的人会忽略偶然事件：每个艺术家多半都只能表现他耽搁掉亲身经历的事情ꂆ>₪，忘了自己，于是ꂆ<₪给自己确立了目标的人会忽略偶然事件：每个艺术家多半都只能表现他耽搁掉亲身经历的事情ꂆ〉₪。度和人间事务的束缚。ꂆ＞
"""
    text2 = '“sfd f“fds ”发多少”'
    text = [{'Text': text1, 'ParagraphIndex': 1, 'PageIndex': 1}]
    a = check_quanbanjiao(text)
    for i in a:
        print(i)

