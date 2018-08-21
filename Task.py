class Task():

    def __init__(self, json):
        self.json=json

    def get_task(self):
        tasks=[]

        for task in self.json["issues"]:
            try:
                key=task["key"]

                assignee = task["fields"]["assignee"]["displayName"]

                issuetype = task["fields"]["issuetype"]["name"]

                status = task["fields"]["status"]["name"]

                progress = task['fields']['aggregateprogress']['progress']

                total = task['fields']['aggregateprogress']['total']
            except (TypeError):
                continue

            tasks.append([key,assignee, issuetype, status, progress, total])

        return tasks

