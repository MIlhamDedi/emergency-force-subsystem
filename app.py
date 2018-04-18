#! /usr/bin/env python3
from subsystem import app
from multiprocessing import Process
from subsystem.plan_retriever import get_plan
side_process = Process(target=get_plan)
side_process.start()

if __name__ == '__main__':
    app.run(debug=True)
