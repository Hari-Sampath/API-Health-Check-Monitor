class API:
    def __init__(self, data):
        self.name = data["name"]
        self.group = data.get("group", "default")
        self.url = data["url"]
        self.method = data.get("method", "GET")
        self.headers = data.get("headers", {})
        self.params = data.get("params", {})
        self.body = data.get("body", None)
        self.expected = data.get("expected", {})


class Config:
    def __init__(self, raw):
        self.project = raw.get("project", {})
        self.settings = raw.get("settings", {})
        self.scheduler = raw.get("scheduler", {})
        self.apis = [API(api) for api in raw.get("apis", [])]