class RESULTCODE:
    APPROVE = 'APPROVE'
    DENY = 'DENY'


class Decision:
    def __init__(self):
        self.finish = False

        self.return_score = None
        self.return_result = None
        self.return_limit = None


    def to_json(self):
        decision_dict = {}
        for name in filter(lambda x: x[0:2] != '__' and x != 'to_json', dir(self)):
            value = getattr(self, name)
            if value is not None:
                decision_dict[name] = value
        return decision_dict