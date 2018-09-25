import json

class Response:
    def __init__(self):
        self.response_dict = {}

    def to_json(self):
        return self.response_dict

    def to_str(self):
        return json.dumps(self.response_dict, ensure_ascii=False)

def get_response(return_code, return_desc, score, decision, request_id):
    response = Response()
    response.response_dict = {
        'return_code': return_code,
        'return_info': return_desc,
        'score': score,
        'decision': decision,
        'request_id': request_id
    }
    return response


