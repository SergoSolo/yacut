from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .models import URL_map


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[DataRequired(message='Обязательное поле!')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, message='Строка должна быть не больше 16 символов'),
            Regexp(
                r'^[A-Za-z0-9]{1,16}$',
                message='Строка должна состоять из следующих символов без пробелов: A-Z, a-z, 0-9'
            ),
            Optional()
        ],
    )
    submit = SubmitField('Создать ссылку')

    def validate_custom_id(self, field):
        if URL_map.query.filter_by(short=field.data).first() is not None:
            flash(f'Имя {field.data} уже занято!', 'error')
            raise ValidationError('Такой вариант короткой ссылки уже существует!')
