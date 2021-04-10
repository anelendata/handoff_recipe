# Extract JIRA Sprints and Issues

What it does:

- Fetch all Boards
- Filter out non-Scrum Boards
- Make Board ID list
- Fetch the Sprints under each Scrum Board
- Replicate Sprint info to BigQuery
- Fetch the Issues under each Sprint whose state is not closed
- Replicate Issues info to BigQuery

## Files

```
jira-sprint
├── .secrets
│   └── secrets.yml (edit this. Don't commit to code repository)
├── files
│   ├── catalog
│   │   ├── jira_boards.json
│   │   ├── jira_issues.json
│   │   └── jira_sprints.json
│   ├── config
│   │   ├── google_client_secret.json (template. do not edit)
│   │   ├── tap_config_board.json
│   │   ├── tap_config_issue.json
│   │   ├── tap_config_sprint.json
│   │   ├── tap_rest_api_spec.json
│   │   ├── target_config_issue.json
│   │   └── target_config_sprint.json
│   ├── schema
│   │   ├── filter_closed
│   │   ├── filter_pre_2019
│   │   ├── jira_boards.json
│   │   ├── jira_issues.json
│   │   └── jira_sprints.json
│   └── transformer
│       ├── extract_board_ids.py
│       ├── clean_issues.py
│       └── extract_sprint_ids.py
├── project.yml
└── README.md (this file)
```
