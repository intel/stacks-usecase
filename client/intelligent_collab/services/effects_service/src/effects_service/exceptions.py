class EffectError(Exception):
    """parent exception"""

    pass


class EffectApplyException(EffectError):
    """error occured during effect apply."""

    pass


class EffectSendException(EffectApplyException):
    """error occured during sending modified frame."""

    pass
