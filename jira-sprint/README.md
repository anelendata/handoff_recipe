# Load all JIRA Sprints & Issue to BigQuery

## What it does

- Fetch all Boards
- Filter out non-Scrum Boards
- Make Board ID list
- Fetch the Sprints under each Scrum Board
- Replicate Sprint info to BigQuery
- Fetch the Issues under each Sprint whose state is not closed
- Replicate Issues info to BigQuery

## How to run locally

### Install handoff

```
pip install handoff
```

### Secrets

1. JIRA API key

Go to [this page](https://id.atlassian.com/manage-profile/security/api-tokens) to obtain the API key:
Edit `./.secrets/secrets.yml` with your email and API key.

### Edit vars section in project.yml

- domain: Your JIRA domain
- gcp_project_id: Google Cloud Platform project ID
- dataset_id: BigQuery dataset ID (example: "jira")

### GCP service account keys

- Create or review the service account for this project. ([doc](https://cloud.google.com/iam/docs/creating-managing-service-accounts))
- Create service account keys([doc](https://cloud.google.com/iam/docs/creating-managing-service-account-keys))
- Replace `../.secrets/google_client_secret.json` in the repository directory with the JSON file downloaded in the previous step.

Reminder: Do not commit `google_client_secret.json` to git.

### Run

```
cd handoff_recipe
handoff -p jira-sprint -w workspace workspace install
handoff -p jira-sprint -w workspace run local
```

## Run on AWS Fargate

Note: Use `-s prod` option in each command below to remove `dev_` prefix from bucket, resources, task, and BigQuery dataset name.

1. Set AWS environment variables

```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
$ export AWS_DEFAULT_REGION=us-west-2
```

Or if you have `.aws/credentials` file,

```
$ export AWS_PROFILE=<your-profile>
```

2. Create Resource Group S3 Bucket and Resources

```
handoff cloud bucket create -p jira-sprint
handoff cloud resources create -p jira-sprint
```

3. Push project config, files, and secrets

```
handoff project push -p jira-sprint
```

4. Build and push Docker container

```
handoff container build -p jira-sprint
handoff container push -p jira-sprint
```

5. Create Fargate task

```
handoff cloud task create -p jira-sprint
```

6. Run

```
handoff cloud run -p jira-sprint
```

7. Schedule

```
handoff cloud schedule create -p jira-sprint -v target_id=1
```

## Clean up

Please refer to this [doc](https://dev.handoff.cloud/en/latest/09_cleanup.html).


## Tips

### Sync only active Sprints


### How to find Sprint ID in Issue


### Create schema


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
