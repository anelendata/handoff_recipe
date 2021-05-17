#!/usr/bin/python
import io, json, logging, sys, os, yaml

LOGGER = logging.getLogger(__name__)

def run(token, tables_yml, historical_sync_start_at, config_prefix, state_prefix,):
    """Extract Github repository names and generate tap-github config
    """
    LOGGER.info("Generating tap_config_github.json")
    lines = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

    with open(tables_yml, "r") as f:
        selected = yaml.load(f, Loader=yaml.FullLoader)

    for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            print(line)
            raise

        repo_name = o.get("record", {}).get("full_name")
        if not repo_name:
            continue

        config = {
            "access_token": token,
            "repository": repo_name
        }
        config_file = config_prefix + "_" + repo_name.replace("/", "_") + ".json"
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        state_file = state_prefix + "_" + repo_name.replace("/", "_") + ".json"
        if os.path.isfile(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)
        else:
            state = {"bookmarks": {repo_name: {}}}

        bookmarks = state["bookmarks"].get(repo_name, state["bookmarks"])

        for s in selected:
            if not bookmarks.get(s, {}).get("since"):
                bookmarks[s] = {"since": historical_sync_start_at}

        state = {"bookmarks": {repo_name: bookmarks}}

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

        print(repo_name.replace("/", "_"))

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
