#!/usr/bin/python
import io, json, logging, sys, os

LOGGER = logging.getLogger()


def has_key(o, key):
    if type(o) is not dict:
        return False
    return o.get("avatarUrls", {}).get(key)


def fix_key(obj):
    new_obj = dict()
    new_obj.update(obj)
    type_ = obj["type"] if type(obj["type"]) is str else obj["type"][1]
    if type_.lower() == "object":
        keys = list(obj["properties"].keys())
        for key in keys:
            new_obj["properties"][key] = fix_key(obj["properties"][key])
            invalid_1st_letter = [str(x) for x in range(0, 10)]
            if key[0] in invalid_1st_letter:
                new_obj["properties"]["_" + key] = new_obj["properties"].pop(key)

    elif type_.lower() == "array":
        new_obj["items"] = fix_key(obj["items"])

    return new_obj

def transform():
    """Rename invalid column keys
    """
    lines = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
    output = {"rows_read": 0}
    for line in lines:
        try:
            o = json.loads(line)

            if o["type"].lower() == "schema":
                o["schema"] = fix_key(o["schema"])

            if o["type"].lower() == "record":
                output["rows_read"] += 1

                # Replace the invalid keys
                for key in o["record"]["fields"].keys():
                    if has_key(o.get("record", {}).get("fields", {}).get(key), "48x48"):
                        o["record"]["fields"][key]["avatarUrls"]["_48x48"] = o["record"]["fields"][key]["avatarUrls"].pop("48x48")
                    if has_key(o.get("record", {}).get("fields", {}).get(key), "32x32"):
                        o["record"]["fields"][key]["avatarUrls"]["_32x32"] = o["record"]["fields"][key]["avatarUrls"].pop("32x32")
                    if has_key(o.get("record", {}).get("fields", {}).get(key), "24x24"):
                        o["record"]["fields"][key]["avatarUrls"]["_24x24"] = o["record"]["fields"][key]["avatarUrls"].pop("24x24")
                    if has_key(o.get("record", {}).get("fields", {}).get(key), "16x16"):
                        o["record"]["fields"][key]["avatarUrls"]["_16x16"] = o["record"]["fields"][key]["avatarUrls"].pop("16x16")

            print(json.dumps(o))

        except json.decoder.JSONDecodeError:
            print(line)
            raise


if __name__ == "__main__":
    transform()
