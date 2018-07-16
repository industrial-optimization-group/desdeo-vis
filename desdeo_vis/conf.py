_settings = {
    'max_as_min': True
}


def conf(**kwargs):
    for k, v in kwargs:
        _settings[k] = v


def get_conf(setting):
    return _settings[setting]
