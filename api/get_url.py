from flask import Blueprint, request, jsonify
import demo
import requests
bp = Blueprint('get_url', __name__)

@bp.route('/get_url', methods=['POST'])
def get_result():
    data = request.get_json()
    text = data.get('text', None)

    url=f"https://api2.lawsnote.com/2/judgements/{text}"
    resp=requests.get(url)
    resp_json=resp.json()
    #print(resp_json['data']['judgement'])
    main_text=''
    for i in resp_json['data']['judgement']:
        if 'type' in i:
            continue
        if '主　文' in i:
            main_text='主文'
        main_text=i+main_text
    print(main_text)
    #打開一個檔案用來寫入。如果檔案已經存在，它會被覆蓋。
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(main_text)
    msg=demo.result('output.txt')
    print(msg)

    return jsonify(msg), 200