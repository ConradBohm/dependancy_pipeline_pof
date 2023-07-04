import json
import re

def retrieve_indexes(logs):
    """
    Finds the lines in the log file at which the objects containing dependency info start and stop.
    These objects would be sent to the repo API, but dryRun is enabled so instead objects are printed.
    Contains some error handling.
    """
    line_indexes = []

    if len(logs) == 0:
        print('Empty log file - perhaps the job did not run in time')

    for index, line in enumerate(logs):
        if '"validationError":"Invalid JSON (parsing failed)"' in line:
            info = json.loads(line)
            repo = info["repository"]
            debug_message = info["error"]["validationMessage"]
            print("====================================================")
            print("invalid repo config in repo:", repo )
            print(debug_message)
            print("====================================================")
        elif '"msg":"semanticCommits: disabled"' in line:
            line_indexes.append(index+4)
        else:
            continue

    return line_indexes #, end_indexes

def find_repo_dependencies(line_indexes, logs):
    """
    Grabs the text from the log file and constructs usable python dicts from the text.
    Returns as a list of objects, organised by repo.
    """
    dep_objects = []
    cleaned_dep_objs = []

    for line in line_indexes:
        object = logs[line]
        dep_objects.append(object)

    for item in dep_objects:
        temp_obj = json.loads(item)
        key = list(temp_obj["config"].keys())[0]
        final_obj = temp_obj["config"][f"{key}"][0]["deps"]
        final_obj.append(temp_obj["repository"])
        cleaned_dep_objs.append(final_obj)

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

    starts = retrieve_indexes(log_lines)
    dependencies_per_repo = find_repo_dependencies(starts, log_lines)
    print_repo_dependencies(dependencies_per_repo)

path = '/app/logs/logs.txt'
parse_logs(path)
