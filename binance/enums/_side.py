class SIDE:
    LONG = 1
    SHORT = -1

    @classmethod
    def __class_getitem__(cls, key: str) -> int:
        try:
            return getattr(cls, key.upper())
        except AttributeError:
            raise KeyError(f"Invalid key '{key}' for {cls.__name__}")