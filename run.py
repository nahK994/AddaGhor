import os

def get_command(port):
    return f"gnome-terminal -e 'bash -c \"kill -9 `lsof -t -i:{port}`; source env/bin/activate; uvicorn app.main:app --host 0.0.0.0 --port {port} --reload; bash\" '" 

os.chdir('User')
os.system(get_command(8000))

os.chdir('../Post')
os.system(get_command(8001))

os.chdir('../React')
os.system(get_command(8002))

print("done")

# https://stackoverflow.com/questions/43332703/open-terminal-run-command-python


# 8000 ==> User
# 8001 ==> Post
# 8002 ==> React