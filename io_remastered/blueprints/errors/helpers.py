from flask import request, jsonify
from io_remastered.utils.requests_utils import is_js_request


def headless_error(error):
    if is_js_request(request):
        return jsonify({"status": error.code, "message": f"an error has occured: {error.code}"}), error.code
    
    return None
