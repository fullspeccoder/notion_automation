import json


def pick(base, *keys):
    """Return a dict composed of key value pairs for keys passed as args."""
    result = {}
    for key in keys:
        if key not in base:
            continue
        value = base.get(key)
        if value is None and key == "start_cursor":
            continue
        result[key] = value
    return result


class NotionPageBuilder:
    def __init__(self, data, icon=None, cover_url=None):
        self.data = pick(data, 'cover', 'icon',
                         'parent', 'properties', 'children')
        self._set_cover_url(cover_url)
        self._set_icon(icon)
        self._set_properties()

    def _set_cover_url(self, url):
        self.data['cover']['external']['url'] = url

    def _set_icon(self, icon):
        self.data['icon']['emoji'] = icon

    def _set_properties(self):
        # Here will need major logic to get the properties set correctly
        for key, value in self.data['properties'].items():
            print(key, value)

    def _set_children(self):
        # Here will need major logic to get the children set correctly
        pass


json_data = dict()

with open("schema.json", "r") as file:
    data = file.read()
    json_data = json.loads(data)

NotionPageBuilder(json_data, 'https://someurl.com')
