import requests
from datetime import datetime
import time
LAST_CHECK = datetime.now()


def get_plan():
    global LAST_CHECK
    while True:
        try:
            r1 = requests.get('https://bigbigcmo.herokuapp.com/api/ef/')
            plan_list = r1.json()
            with open('workfile', 'a') as f:
                print(str(LAST_CHECK) + ": " + str(plan_list), file=f)
            for _ in plan_list:
                plan_time = datetime.strptime(_['date_time_of_send'],
                                              "%Y-%m-%d %H:%M:%S")
                if plan_time > LAST_CHECK:
                    r2 = requests.post(
                        'https://cz3003-ef.herokuapp.com/api/plan',
                        data={
                            'crisis_id': _["crisis_id"],
                            'details': _['detail'],
                            "time": _['date_time_of_send']
                        })
                    if r2.status_code == 400:
                        print(f"Wrong Plan Format on Plan from {plan_time}")
            LAST_CHECK = datetime.now()
            time.sleep(15)
        except (KeyboardInterrupt, SystemExit):
            break
