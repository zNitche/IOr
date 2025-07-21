from flask import url_for


def get_static_resource(path):
    return  url_for('static', filename=path)
