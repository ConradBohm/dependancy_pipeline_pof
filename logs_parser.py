import json
import re

def retrieve_indexes(logs):
    """
    Finds the lines in the log file at which the objects containing dependency info start and stop.
    These objects would be sent to the repo API, but dryRun is enabled so instead objects are printed.
    Contains some error handling.
    """
    start_indexes = []
    end_indexes = []

    if len(logs) == 0:
        print('Empty log file - perhaps the job did not run in time')

    for index, line in enumerate(logs):
        if " INFO: Repository has invalid config" in line:
            print("invalid repo config")
            break
        elif "DEBUG: packageFiles with updates" in line:
            start_indexes.append(index)
        elif "DEBUG: Repository timing splits" in line:
            end_indexes.append(index)
        else:
            continue

    return start_indexes, end_indexes

def find_repo_dependencies(start_indexes, end_indexes, logs):
    """
    Grabs the text from the log file and constructs usable python dicts from the text.
    Returns as a list of objects, organised by repo.
    """
    dep_objects = []
    cleaned_dep_objs = []

    for start, end in zip(start_indexes, end_indexes):
        object = logs[start+1:end-2]
        dep_objects.append(object)

    for item in dep_objects:
        temp = [x.strip() for x in item]
        temp_str = '{'+''.join(temp)+'}'
        temp_obj = json.loads(temp_str)
        key = list(temp_obj["config"].keys())[0]
        final_obj = temp_obj["config"][f"{key}"][0]["deps"]
        cleaned_dep_objs.append(final_obj)

    for num, object in enumerate(cleaned_dep_objs):
        log_string = logs[end_indexes[num]]
        repo_name_temp = log_string.split('repository=',1)[1]
        repo_name = repo_name_temp[:-2]
        object.append(repo_name)
        print(object)

    return cleaned_dep_objs

def print_repo_dependencies(dep_objects):
    """
    A way to visualise the retrieved dependency info. Could be used instead to send payloads to 
    alerting software / Jira / etc.
    """
    for object in dep_objects:
        print("\n\n\n====================================================")
        print("Repo: ", object[-1])
        object.pop()
        print('----------------------------------------------------')
        for item in object:
            if len(item['updates']) > 0:
                print('----------------------------------------------------')
                print('Name: ',item['depName'])
                print('Version: ', item['currentVersion'])
                print('New Version: ', item['updates'][0]['newVersion'])
                print('Release Type: ', item['updates'][0]['updateType'])
                

def parse_logs(log_file_path):
    log_lines = open(f"{log_file_path}", "r").readlines()

    starts, ends = retrieve_indexes(log_lines)
    print('hello')
    print(starts, ends)
    dependencies_per_repo = find_repo_dependencies(starts, ends, log_lines)
    print_repo_dependencies(dependencies_per_repo)

path = 'logs.txt'
parse_logs(path)
