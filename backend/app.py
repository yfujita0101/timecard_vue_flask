from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import calendar
import uuid

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# API確認用jsonリスト
ATTENDANCES = []

# 今月分のを作成して追加
# 月末日を取得
today = datetime.utcnow()
end_day = calendar.monthrange(today.year, today.month)[1]

for day in range(1, end_day):
    attendance = {
        'id': uuid.uuid4().hex,
        'classification': '',
        'day': datetime(today.year, today.month, day, 0, 0, 0),
        'start': '',
        'end': '',
        'memo': '',
    }
    ATTENDANCES.append(attendance)


@app.route('/roster', methods=['GET'])
def all_roster():
    response_object = {'status': 'success'}
    response_object['attendances'] = ATTENDANCES

    return jsonify(response_object)

@app.route('/startWork', methods=['POST'])
def start_work():
    # 現在時刻を取得
    now = datetime.now()
    utc_now = datetime.utcnow()

    # 検索用日時作成
    key_day = datetime(now.year, now.month, now.day, 0, 0, 0)

    for attendance in ATTENDANCES:
        if attendance['day'] == key_day and attendance['start'] == '':
            attendance['start'] = utc_now
            attendance['classification'] = '出勤'
            response_object = {'status': 'success'}
        else:
            response_object = {'status': 'not success'}

    return jsonify(response_object)


@app.route('/endWork', methods=['POST'])
def end_work():
    # 現在時刻を取得
    now = datetime.now()
    utc_now = datetime.utcnow()

    # 検索用日時作成
    key_day = datetime(now.year, now.month, now.day, 0, 0, 0)

    for attendance in ATTENDANCES:
        if attendance['day'] == key_day and attendance['end'] == '':
            attendance['end'] = utc_now
            response_object = {'status': 'success'}
        else:
            response_object = {'status': 'not success'}

    return jsonify(response_object)


@app.route('/roster/<attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        # 送信データ取得
        post_data = request.get_json()

        print(post_data)

        # id検索して、見つかったら内容update

        for attendance in ATTENDANCES:
            if attendance['id'] == post_data['id']:
                if post_data['id'] != '':
                    attendance['classification'] = post_data['classification']
                if post_data['startTime'] != '':
                    post_date = datetime.strptime(post_data['startTime'], '%H:%M')
                    # 変更版の開始時刻作成
                    startTime = datetime(attendance['day'].year, attendance['day'].month, attendance['day'].day, post_date.hour , post_date.minute, 0) - timedelta(hours=9)
                    attendance['start'] = startTime
                if post_data['endTime'] != '':
                    post_date = datetime.strptime(post_data['endTime'], '%H:%M')
                    endTime = datetime(attendance['day'].year, attendance['day'].month, attendance['day'].day, post_date.hour, post_date.minute , 0) - timedelta(hours=9)
                    attendance['end'] = endTime
                if post_data['memo'] != '':
                    attendance['memo'] = post_data['memo']
                response_object['message'] = 'updated!'
            else:
                response_object['message'] = 'no updated!'

    return jsonify(response_object)

if __name__ == '__main__':
    app.run()
