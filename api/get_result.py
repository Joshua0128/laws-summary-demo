from flask import Blueprint, request, jsonify
import demo
bp = Blueprint('get_result', __name__)

@bp.route('/get_result', methods=['POST'])
def get_result():
    data = request.get_json()
    text = data.get('text', None)

    # 打開一個檔案用來寫入。如果檔案已經存在，它會被覆蓋。
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    msg=demo.result('output.txt')


    return jsonify({'msg': msg}), 200