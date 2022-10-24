from flask.json.provider import DefaultJSONProvider


class CustomJSONEncoder(DefaultJSONProvider):
    '''
    Can be used to override behavior for encoding all json strings
    '''
