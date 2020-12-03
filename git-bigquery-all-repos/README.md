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
│   ├── target_config.json (edit this to set the destination dataset)
│   └── transformer
│       ├── properties.py
│       ├── records.py
│       └── tap_config_github.py
├── project.yml (review this)
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
handoff cloud create bucket -p . --stage prod
handoff project push -p . -s prod
handoff container build
handoff container push
handoff task create -p . -s prod
handoff schedule -p . -s prod
```

