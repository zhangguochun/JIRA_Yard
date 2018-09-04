#!/usr/bin/env bash
rm pic/*
docker build -t jiraapp:v1 .
docker save --output ~/Downloads/jiraapp_v1.tar jiraapp:v1
scp ~/Downloads/jiraapp_v1.tar gzhang@10.110.121.79:jira.tar
