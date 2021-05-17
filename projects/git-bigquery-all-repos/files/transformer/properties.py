#!/usr/bin/python
import io, json, logging, sys, os, yaml

LOGGER = logging.getLogger(__name__)

def run(input_file, output_file, tables_yml):
    with open(input_file, "r") as f:
        properties = json.load(f)
    streams = properties["streams"]

    with open(tables_yml, "r") as f:
        selected = yaml.load(f, Loader=yaml.FullLoader)

    for stream in streams:
        if stream["tap_stream_id"] == "issue_events":
            assignee_schema = stream["schema"]["properties"]["issue"][
                "properties"]["assignee"]["properties"]

    for stream in streams:
        # add _sdc_batched_at
        stream["schema"]["properties"]["_sdc_batched_at"] = {
            "type": ["null", "string"],
            "format": "date-time"
        }

        if stream["tap_stream_id"] in selected:
            stream["schema"]["selected"] = True

        # Fix issues["assignee"] as its property is usually empty
        if stream["tap_stream_id"] == "issues":
            stream["schema"]["properties"]["assignee"]["properties"].update(
            assignee_schema)

    with open(output_file, "w") as f:
        json.dump(properties, f, indent=2)

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])
