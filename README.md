## Steps to start getting data

```
mkdir -p $HOME/jira-data

docker run -d -p 9090:8080 -v $HOME/jira-data:/var/atlassian/jira --name jira blacklabelops/jira

export JIRA_SERVER="http://$(curl http://instance-data/latest/meta-data/public-ipv4):9090"
```

## JIRA Collector

Application collects all the JIRA metrics required

## Agile Portafolio component

The requirements for this components are:
* Pull all the Work In Progress Stories (WIP)
* Pull all the New Stories (TO-DO)