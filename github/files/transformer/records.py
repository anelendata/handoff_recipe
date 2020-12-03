#!/usr/bin/python
import io, json, logging, sys, os

LOGGER = logging.getLogger(__name__)

def run(properties_file):
    with open(properties_file, "r") as f:
        properties = json.load(f)

    LOGGER.info("Fixing schema")
    for stream in properties["streams"]:
        if not stream["schema"].get("selected"):
            continue
        stream["type"] = "SCHEMA"
        print(json.dumps(stream))

    lines = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    for line in lines:
        o = json.loads(line)
        if o["type"].lower() == "schema":
            continue
        print(json.dumps(o))


if __name__ == "__main__":
    run(sys.argv[1])
