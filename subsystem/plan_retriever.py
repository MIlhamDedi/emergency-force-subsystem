import requests
import time
from subsystem.config import BASE_URL, CMO_URL
solution_id_list = []


def get_plan():
    while True:
        try:
            r1 = requests.get(CMO_URL)
            plan_list = r1.json()
            for _ in plan_list:
                if _['solution_id'] not in solution_id_list:
                    r2 = requests.post(
                        BASE_URL + '/api/plan',
                        data={
                            'id': _['solution_id'],
                            'crisis_id': _["crisis_id"],
                            'details': _['detail'],
                            "time": _['date_time_of_send']
                        })
                    solution_id_list.append(_['solution_id'])
                    if r2.status_code == 200:
                        print(f"added plan with id {_['solution_id']}")
                    if r2.status_code == 400:
                        print(
                            f"Wrong Format on solution_id {_['solution_id']}"
                        )
                    if r2.status_code == 403:
                        solution_id_list.append(_['solution_id'])
                        print(f"Plan with id {_['solution_id']} already exist")
            time.sleep(20)
        except (KeyboardInterrupt, SystemExit):
            break
