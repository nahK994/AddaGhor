import os
import time

def run_service(service_name, port):
    return f"gnome-terminal -e 'bash -c \"kill -9 `lsof -t -i:{port}`; cd {service_name}; source env/bin/activate; uvicorn app.main:app --host 0.0.0.0 --port {port} --reload; bash\" '" 

def run_service_consumer(service_name):
    return f"gnome-terminal -e 'bash -c \"cd {service_name}; source env/bin/activate; export PYTHONPATH='{os.getcwd()}/{service_name}'; python3 app/consumer.py; bash\" '" 

os.system("docker start rabbitmq")
time.sleep(10)

os.system(run_service('User', 8000))

os.system(run_service('Post', 8001))
os.system(run_service_consumer('Post'))

os.system(run_service('React', 8002))
os.system(run_service_consumer('React'))

os.system(run_service('Comment', 8003))
os.system(run_service_consumer('Comment'))

os.system(run_service('Timeline', 8004))
os.system(run_service_consumer('Timeline'))

print("done")

# https://stackoverflow.com/questions/43332703/open-terminal-run-command-python
# https://stackoverflow.com/questions/43728431/relative-imports-modulenotfounderror-no-module-named-x


# 8000 ==> User
# 8001 ==> Post
# 8002 ==> React
# 8003 ==> Comment
# 8004 ==> Timeline