import hashlib


def tokenBuilder(password, **kwargs):
    token_params = {key: value for key, value in kwargs.items() if not isinstance(value, dict)}
    token_params['Password'] = password
    sorted_params = sorted(token_params.keys())
    concatenated_string = ''
    for param in sorted_params:
        if param == "Token":
            continue
        data = token_params[param]
        if data:
            if isinstance(data, bool):
                data = str(data).lower()
            concatenated_string += str(data)
    
    token = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()
    return token
