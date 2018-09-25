from .decision import RESULTCODE

def execute(json_data, field, feature, score, rule, decision, exec_info):
    exec_info['risk_flow_execute'].append(__name__)

    decision.return_score = 0
    decision.return_result = RESULTCODE.DENY
    decision.return_limit = 0

    decision.finish = True
    return True, None
