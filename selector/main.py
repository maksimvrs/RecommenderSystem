from flask import Flask, request, jsonify
from selector.db import *
import numpy as np

from selector.mlkit import MLKit

app = Flask(__name__)

specs = ['perseverance', 'collectivism', 'success', 'hang', 'adaptability', 'self_esteem_conflict',
         'empathy', 'determination', 'leadership', 'hard_work', 'initiative', 'emotional_stability', 'pseudology']

ml = MLKit(specs, specs)

# for value in specs:
#     column = Column(value, Integer)
#     add_column('developers', column)
#
# for value in specs:
#     column = Column(value, Integer)
#     add_column('mentors', column)


@app.route('/')
def index():
    return "It is work!"


@app.route('/add/developer/<login>', methods=['POST'])
def add_devaloper(login):
    session = Session()
    if request.is_json:
        data = request.json
        engine.execute('INSERT INTO developers (%s)  VALUES (%s) ON CONFLICT (login) DO UPDATE SET %s' %
                       (', '.join(list(['login'] + [spec for spec in specs if data.get(spec)])),
                        ', '.join(
                            list(['\'' + login + '\''] + [str(data.get(spec)) for spec in specs if data.get(spec)])),
                        ', '.join([spec + '=' + str(data.get(spec)) for spec in specs if data.get(spec)])))
    session.commit()
    return jsonify({'status': 'ok'})


@app.route('/add/mentor/<login>', methods=['POST'])
def add_mentor(login):
    session = Session()
    if request.is_json:
        data = request.json
        engine.execute('INSERT INTO mentors (%s)  VALUES (%s) ON CONFLICT (login) DO UPDATE SET %s' %
                       (', '.join(list(['login'] + [spec for spec in specs if data.get(spec)])),
                        ', '.join(
                            list(['\'' + login + '\''] + [str(data.get(spec)) for spec in specs if data.get(spec)])),
                        ', '.join([spec + '=' + str(data.get(spec)) for spec in specs if data.get(spec)])))
    session.commit()
    return jsonify({'status': 'ok'})


@app.route('/add/review', methods=['POST'])
def add_review():
    session = Session()
    developer = request.args.get('developer')
    mentor = request.args.get('mentor')
    if len(engine.execute('SELECT * FROM developers WHERE login = %s' % "\'" + developer + "\'").keys()) < 1 or \
            len(engine.execute('SELECT * FROM mentors WHERE login = %s' % "\'" + mentor + "\'").keys()) < 1:
        return jsonify({'error': 'developer or mentor ont found'})
    engine.execute('INSERT INTO precedents (developer, mentor)  VALUES (%s, %s)' %
                   ("\'" + developer + "\'", "\'" + mentor + "\'"))
    learn()
    session.commit()
    return jsonify({'status': 'ok'})


@app.route('/get/<login>', methods=['GET'])
def get(login):
    try:
        result = engine.execute('SELECT * FROM developers WHERE login = %s' % "\'" + login + "\'")
        predict = None
        for value in result:
            predict_vector = ml.predict(value[1:])
            if predict_vector is None:
                return jsonify({'error': 400})
            predict = predict_mentor(predict_vector)
            predict = [{'mentor': pred[0], 'distance': pred[1]} for pred in predict]
    except:
        return jsonify({'error': 'database error'})

    return jsonify({'predict': predict})


def predict_mentor(predict_vector):
    print(type(predict_vector))
    mentors = engine.execute('SELECT * FROM mentors')
    predict = []
    for mentor in mentors:
        dist = sum(map(lambda x: abs(x[0] - x[1]), zip(mentor[1:], list(predict_vector))))
        predict.append((mentor[0], dist / len(predict_vector)))
    predict.sort(key=lambda x: x[1])
    return predict[:20]


def learn():
    print("Learning")
    X_train = np.empty((0, len(specs)))
    y_train = np.empty((0, len(specs)))
    precedents = engine.execute('SELECT * FROM precedents')
    is_empty = True
    for value in precedents:
        is_empty = False
        developer = engine.execute('SELECT * FROM developers WHERE login = %s' % "\'" + value[1] + "\'")
        mentor = engine.execute('SELECT * FROM mentors WHERE login = %s' % "\'" + value[2] + "\'")
        for value in developer:
            X_train = np.vstack((X_train, value[1:]))
        for value in mentor:
            y_train = np.vstack((y_train, value[1:]))

    if not is_empty:
        X_train[np.isnan(np.array(X_train, dtype=np.float64))] = 0
        y_train[np.isnan(np.array(y_train, dtype=np.float64))] = 0

        ml.fit(X_train, y_train)


if __name__ == '__main__':
    learn()
    app.run(host='0.0.0.0', port=5000, debug=True)
