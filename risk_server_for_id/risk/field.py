
class Field:
    def __init__(self):
        pass
    def _to_json(self):
        field_dict = {}
        for name in filter(lambda x: x[0:1] != '_', dir(self)):
            if name in ['user_address_amap_text', 'company_address_amap_text']:
                value = getattr(self, name)
                field_dict[name] = value
        return field_dict 
