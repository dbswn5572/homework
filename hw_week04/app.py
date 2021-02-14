from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.orderlistdb

@app.route('/')
def shopping():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def write_orders():
	# 1. 클라이언트가 준 name, cnt, address, phone 가져오기.
    name = request.form['name']
    cnt = request.form['cnt']
    address = request.form['address']
    phone = request.form['phone']
    print(name, cnt, address, phone)
	# 2. DB에 정보 삽입하기
    order = {
        'name': name,
        'cnt': cnt,
        'address': address,
        'phone': phone
    }
    db.orders.insert_one(order)

	# 3. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '주문 정상 완료되었습니다 :)'})


@app.route('/order', methods=['GET'])
def read_orders():
    orders = list(db.orders.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)