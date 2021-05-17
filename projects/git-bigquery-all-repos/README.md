# github-bigquery-all-repos

Stitch Data and Singer's tap-github supports multiple repository, but they
do not automatially search and update the list of the repositories to fetch.

This example handoff project first fetches the list of the repositories and
generate the config files of tap-github. Then run it for each repository to
upload the tables such as commits, and pull-requests to BigQuery.

Files:
```
github/
├── files
│   ├── catalog
│   │   └── repository.json
│   ├── google_client_secret.json (don't edit: template)
│   ├── properties.json
│   ├── schema
│   │   └── repository.json
│   ├── tables.yml (review this)
│   ├── tap_config_repo.json
│   ├── target_config.json
│   └── transformer
│       ├── properties.py
│       ├── records.py
│       └── tap_config_github.py
├── project.yml (edit vars section)
├── README.md (this file)
└── .secrets
    └── secrets.yml (edit this)
```

After the necessary parameters are set, do:

```
cd github-all-repo
handoff --project . --workspace workspace workspace install
handoff -p . -w workspace run local
```

to run locally.

Example deployment command sequence to AWS Fargate:

```
export AWS_PROFILE=your-profile
handoff cloud create bucket --project . --stage prod
handoff project push -p . -s prod
handoff container build -p .
handoff container push -p .
handoff cloud resources create -p . -s prod
handoff cloud task create -p . -s prod
handoff cloud run -p . -s prod  # Run now
handoff cloud schedule -p . -s prod  # Schedule
```

