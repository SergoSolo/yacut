import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'].strip() == '':
        data['custom_id'] = get_unique_short_id()
    else:
        short = data['custom_id']
        if URL_map.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
        elements = re.compile(r'^[A-Za-z0-9]{1,16}$')
        if elements.match(short) is None:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
