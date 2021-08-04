## Load USGS Earthquake Event data to Snowflake

This project extract USGS Earthquake event data (publicly available) and
load on Snowflake datawarehouse.

An example of the raw data can be pulled with curl command:
```
curl https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=2014-01-02&minmagnitude=1
```

![usgs map](https://articles.anelen.co/images/earthquakes.png)
(The image above, generated with the data in this article, is a map showing the location and magnitude (bubble size) of earthquakes on June 24, 2020, based on the USGS Earthquake event data. From https://articles.anelen.co/elt-google-cloud-storage-bigquery )

Please see [tap-rest-api/README.md](https://github.com/anelendata/tap-rest-api)
for the details of the Singer.io tap part of this example.

## Files

You will need to edit project.yml.
```
usgs-snowflake
├── files
│   ├── catalog
│   │   └── earthquakes.json
│   ├── custom_spec.json
│   ├── schema
│   │   └── earthquakes.json
│   ├── tap_config.json
│   └── target_config.json
├── project.yml (edit this file at "replace me!!!")
├── README.md
└── sample_records.json
```

After the necessary parameters are set, do:

```
cd usgs-snowflake
handoff --project . --workspace workspace workspace install
handoff -p . -w workspace run local -v start_datetime="2021-01-01T00:00:00" end_datetime="2021-01-02T00:00:00"
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

