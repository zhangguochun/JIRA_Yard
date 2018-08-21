class Story():

    def __init__(self, json):
        self.json=json

    def get_story(self):
        stories=[]

        for story in self.json["issues"]:
            try:
                key=story["key"]

                for storyDeveloper in story["fields"]["customfield_12866"]:
                    developer=storyDeveloper["displayName"]
                    break # Always get the 1st story developer

                sp=story["fields"]["customfield_10242"]  #story point
                status=story["fields"]["status"]["name"]

                bug=0
                for subtask in story["fields"]["subtasks"]:
                    if (subtask["fields"]["issuetype"]["name"]=="Bug Sub-Task"):
                        bug+=1

            except (TypeError):
                continue

            stories.append([key,developer,sp,status,bug])


        return  stories
