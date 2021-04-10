#!/usr/bin/python
import io, json, logging, sys, os

LOGGER = logging.getLogger(__name__)

def extract_ids(board_type="scrum"):
    """Extract JIRA Board IDs
    - Filter out non-scrum JIRA boards
    - Extract only Jira Board ID from JSON
    - Write out the ID string to stdout (newline separated)
    """
    LOGGER.info("Running extract_ids")
    lines = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    output = {"rows_read": 0}
    for line in lines:
        try:
            o = json.loads(line)
            if o["type"].lower() == "record":
                output["rows_read"] += 1
            record = o.get("record", {})

            # filters
            type_ = record.get("type")
            if type_ != board_type:
                continue

            # extract and transform
            id_ = record.get("id")
            if id_ is not None:
                print(id_)

        except json.decoder.JSONDecodeError:
            print(line)
            raise

if __name__ == "__main__":
    board_type = "scrum"
    if len(sys.argv) > 1:
        board_type = sys.argv[1]
    extract_ids(board_type)
