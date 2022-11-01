from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    base_url = request.base_url
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id or custom_id.strip() == '':
            custom_id = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        flash('Ваша ссылка готова :', 'success')
        return render_template('home.html', form=form, base_url=base_url, custom_id=custom_id)
    return render_template('home.html', form=form, base_url=base_url)


@app.route('/<custom_id>', methods=['GET'])
def link_redirect_view(custom_id):
    urls = URL_map.query.filter_by(short=custom_id).first()
    if urls is not None:
        return redirect(urls.original, HTTPStatus.FOUND)
    return abort(HTTPStatus.NOT_FOUND)
