import os
import time

def get_command_delete_DB(service_name):
    return f"cd {service_name}; rm -rf sql_app.db;"

def get_command_init_DB(service_name):
    return f"gnome-terminal -e 'bash -c \"cd {service_name}; source env/bin/activate; alembic upgrade head; bash\" '" 

def init_DB(service_name):
    try:
        os.system(get_command_delete_DB(service_name))
        os.system(get_command_init_DB(service_name))
    except:
        os.system(get_command_init_DB(service_name))

init_DB('User')
init_DB('Post')
init_DB('React')
init_DB('Comment')
init_DB('Timeline')

print("done")

# https://stackoverflow.com/questions/43332703/open-terminal-run-command-python


# 8000 ==> User
# 8001 ==> Post
# 8002 ==> React