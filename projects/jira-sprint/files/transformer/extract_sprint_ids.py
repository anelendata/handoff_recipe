#!/usr/bin/python
import argparse, datetime, dateutil, io, json, logging, sys, os
from typing import Dict
import jsonschema
from jsonschema import validate


LOGGER = logging.getLogger(__name__)


def filter_and_transform(schema: Dict = None) -> None:
    """Extract JIRA Sprint IDs
    - filter_closed (bool): Exclude closed sprints if true
    - created_from (datetime): Exclude older sprints if set
    """
    LOGGER.info("Running extract_ids")
    lines = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    output = {"rows_read": 0}
    for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            print(line)
            raise

        if o["type"].lower() == "record":
            output["rows_read"] += 1
        record = o.get("record", {})

        if schema:
            try:
                validate(record, schema)
            except jsonschema.exceptions.ValidationError:
                LOGGER.info("INFO Skipping Record: %s state: %s startDate %s" %
                               (record.get("id"), record.get("state"), record.get("startDate")))
                continue

        # filters
#            if filter_closed:
#                state = record.get("state")
#                if state and state == "closed":
#                    continue
#            if start_date_from:
#                start_date = record.get("startDate")
#                if start_date and start_date < start_date_from:
#                    continue

        # extarct and transform
        id_ = record.get("id")
        if id_ is not None:
            print(id_)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema",
        default=None,
        help="Schema file to filter the incompatible records")

    parser.add_argument(
        "--filter_closed",
        action="store_true",
        help="Filter out closed sprints")
    parser.add_argument(
        "--start_date_from",
        default=None,
        help="Filter out older sprints")

    args = parser.parse_args()

    if args.start_date_from:
        args.start_date_from  = dateutil.parser.parse(args.start_date_from)

    if args.schema:
        with open(args.schema, "r") as f:
            args.schema = json.load(f)
    filter_and_transform(args.schema)
