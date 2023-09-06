import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, bearertoken: str) -> None:
        self.bearertoken = bearertoken

    def __call__(self, req: requests.PreparedRequest) -> requests.PreparedRequest:
        req.headers["Authorization"] = f"Bearer {self.bearertoken}"
        return req
