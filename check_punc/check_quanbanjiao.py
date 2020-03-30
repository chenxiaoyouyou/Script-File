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

    def find(alist, current, pair):
        if len(alist) > 0:
            last_item = alist[-1]
            if last_item['c'] == pair:
                error_list.append([page, number, current['i'], current['c'], errmsg, 1])
                error_list.append([page, number, last_item['i'], last_item['c'], errmsg, 1])
                alist.pop()

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
        if char == "\u007DD":
            find(dakuohao, item, "\uFF5B")
            continue

        if char == "\uFF1C" or char == "\u003C":
            jiankuohao.append(item)
            continue
        if char == "\uFF1E":
            find(jiankuohao, item, "\u003C")
            continue
        if char == "\u003E":
            find(jiankuohao, item, "\uFF1C")
            continue

        if char == "\u3008" or char == "\u003C":
            danshuminghao.append(item)
            continue
        if char == "\u3009":
            find(danshuminghao, item, "\u003C")
            continue
        if char == "\u003E":
            find(danshuminghao, item, "\u3008")
            continue

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
        # Inputtext = every_dict['paragraphContent']
        # Inputnumber = every_dict['paragraphNumber']
        # Inputpage = every_dict['pageIndex']
        Inputtext = every_dict['Text']
        Inputnumber = every_dict['ParagraphIndex']
        Inputpage = every_dict['PageIndex']
        result = check(Inputtext, Inputnumber, Inputpage)
        result_list = result_list + result
    return result_list


if __name__ == '__main__':
    # check_punc(text)‘’
    # '^[a-zA-Z ]*[0-9\.∶-≦≈÷=∑∏≮∴＝﹣﹢﹤≤·＜＋/≡＞*㏒－∵+≠﹥≧≒≯㏑×≥∅\(\)\[\]\{\}｛｝（）］［]+$
    text1 = """中括号，这个冒险家更换国家、城市、地位、职业、生活风格和女人，就如同在一个身体上更换要洗的衣服那样。[那些同代人在享受方面都是业余爱好者，正如卡萨诺瓦在塑造形象方面是业余爱好者一样]，这是因为，英才的永存悲剧就是，他胜任并且渴望了解生存的广阔内容和欢乐，［这是因为，英才的永存悲剧就是，他胜任并且渴望了解生存的广阔内容和欢乐，然而他却始终被束缚在自己的任务上］做自己工作室的奴隶，因为加于自身的责任而不得自由。[这是因为，英才的永存悲剧就是，他胜任并且渴望了解生存的广阔内容和欢乐，然而他却始终被束缚在自己的任务上，做自己工作室的奴隶］。每个真正的艺术家大半生都是生活在孤独之中和与自己的创作进行的斗争之中，［每个真正的艺术家大半生都是生活在孤独之中和与自己的创作进行的斗争之中，都是完全献身于贴近身边的现实的]，都是完全献身于贴近身边的现实的。"""
    text2 = '“sfd f“fds ”发多少”'
    text = [{'Text': text1, 'ParagraphIndex': 1, 'PageIndex': 1}]
    a = check_quanbanjiao(text)
    for i in a:
        print(i)

