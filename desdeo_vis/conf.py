"""
Globally configure default settings for plotting and widgets.
"""

_settings = {
    'max_as_min': True
}


def conf(**kwargs):
    """
    Set configuration values

    Parameters
    ----------
    max_as_min
        Whether to reformulate maximized functions as minimized functions.
    """
    for k, v in kwargs.items():
        _settings[k] = v


def get_conf(setting: str):
    """
    Get a configuration value

    Parameters
    ----------
    setting
        The configuration key to get.
    """
    return _settings[setting]
