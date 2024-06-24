class RefreshTokenPayload:
    def __init__(self, payload: dict):
        self.payload = payload

    def __getitem__(self, key: str):
        return self.payload.get(key)

    def get(self, key: str):
        return self.payload.get(key)

    @property
    def user_id(self) -> int:
        return self.payload.get("user_id")
