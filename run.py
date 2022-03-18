import os
import time

def get_command(service_name, port):
    return f"gnome-terminal -e 'bash -c \"cd {service_name}; kill -9 `lsof -t -i:{port}`; source env/bin/activate; uvicorn app.main:app --host 0.0.0.0 --port {port} --reload; bash\" '" 

os.system("docker start rabbitmq")
time.sleep(2)

os.system(get_command('User', 8000))

os.system(get_command('Post', 8001))

os.system(get_command('React', 8002))

os.system("gnome-terminal -e 'bash -c \"source env/bin/activate; cd React/app/; python3 consumer.py; bash\" '")

os.system(get_command('Comment', 8003))

os.system(get_command('Timeline', 8004))

print("done")

# https://stackoverflow.com/questions/43332703/open-terminal-run-command-python


# 8000 ==> User
# 8001 ==> Post
# 8002 ==> React