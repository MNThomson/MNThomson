#!/usr/bin/env python

import os
import json
import requests

class GitHub(object):
    def __init__(self, token):
        self.headers = {'Authorization': 'token %s' % token}

    def get(self, endpoint):
        endpoint = endpoint.replace(":user", os.getenv("User"))
        return requests.get(f"https://api.github.com{endpoint}", headers=self.headers).json()

gh = GitHub(os.getenv("GITHUB_TOKEN"))

def getRepos():
    repos = []
    repos_json = gh.get(f"/users/:user/repos")
    for repo in repos_json:
        repos.append(repo["name"])
    return repos

def getWorkflows(repos):
    covered = 0
    success = 0
    total = 0
    for repo in repos:
        workflows = gh.get(f"/repos/:user/{repo}/actions/workflows")
        if int(workflows["total_count"]) > 0:
            covered += 1
            total += workflows["total_count"]
            for workflow in workflows["workflows"]:
                wf_id = workflow["id"]
                workflow_data = gh.get(f"/repos/:user/{repo}/actions/workflows/{wf_id}/runs")
                if len(workflow_data["workflow_runs"]) == 0:
                    continue
                elif workflow_data["workflow_runs"][0]["conclusion"] == "success":
                    success += 1
    return covered, success, total

def output(repos, covered, success, total):
    data = {}
    data["Repositories_Covered"] = str(int(covered/len(repos) * 100)) + "% (" + str(covered) + "/" + str(len(repos)) + ")" #Ex: "50% (3/6)"
    data["Passing_Workflows"] = str(int(success/total * 100)) + "% (" + str(success) + "/" + str(total) + ")" #"75% (3/4)"
    with open('stats.json', 'w', encoding="utf8") as stats_file:
        stats_file.write(json.dumps(data, indent = 4))
        print(data)

if __name__=="__main__":
    repos = getRepos()
    covered, success, total = getWorkflows(repos)
    output(repos, covered, success, total)
