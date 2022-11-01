from datetime import datetime
from urllib.parse import urljoin

from flask import request

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        base_url = request.host_url
        return dict(
            url=self.original,
            short_link=urljoin(base_url, self.short)
        )

    def from_dict(self, data):
        setattr(self, 'short', data['custom_id'])
        setattr(self, 'original', data['url'])
