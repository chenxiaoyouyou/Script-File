# coding=utf-8
from flask import Flask, request, jsonify
from check_punc import check_punc
import sys
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
# CORS(app, supports_credentials=True)

# detector = UnitDetector()


# /api/punctuation_test/
@app.route("/api/punctuation_test/", methods=["POST", "GET"])
@cross_origin(origin='172.18.34.25:7000', headers=['Content-Type'])
def find():
    # data = request.get_json()
    data = request.data
    # print(data)
    # print(data1)
    if not data:
        return jsonify(errmsg="请输入文本")
    # print(123)
    # text = data.get("text")
    # print(text)
    # if not text:
    #     return jsonify(errmsg="请求数据错误")
    text = data.decode(encoding='utf-8')
    if type(text) is not str:
        return jsonify(errmsg="输入错误")

    text_list = text.split("\n")
    para_list = []
    # print(text_list)
    for i, strings in enumerate(text_list):
        para_list.append({"paragraphContent":strings, "paragraphNumber": i, "pageIndex":0})

    res = check_punc(para_list)
    res_to_return = []
    for item in res:
        res_to_return.append({'pos': item['offset']+1, 'info': item['lookup']})

    return str(res_to_return)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=True)
    else:
        app.run()

