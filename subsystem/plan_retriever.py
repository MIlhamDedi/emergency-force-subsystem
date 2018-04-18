import requests
import time
solution_id_list = []


def get_plan():
    global LAST_CHECK
    while True:
        try:
            r1 = requests.get('https://bigbigcmo.herokuapp.com/api/ef/')
            plan_list = r1.json()
            for _ in plan_list:
                if _['solution_id'] not in solution_id_list:
                    r2 = requests.post(
                        'https://cz3003-ef.herokuapp.com/api/plan',
                        data={
                            'crisis_id': _["crisis_id"],
                            'details': _['detail'],
                            "time": _['date_time_of_send']
                        })
                    solution_id_list.append(_['solution_id'])
                    if r2.status_code == 400:
                        print(
                            f"Wrong Format on solution_id {_['solution_id']}"
                        )
            time.sleep(20)
        except (KeyboardInterrupt, SystemExit):
            break
