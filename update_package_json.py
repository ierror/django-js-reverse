import pathlib
import json

from packaging import version as packaging_version


def to_npm_version(py_version):
    parsed = packaging_version.Version(py_version)
    base = parsed.base_version

    def fmt(tag, tag_num):
        return f"{base}-{tag}.{tag_num}"

    tags = [
        tag
        for tag in [
            parsed.pre,
            ("post", parsed.post) if parsed.post is not None else None,
            ("dev", parsed.dev) if parsed.dev is not None else None,
        ]
        if tag is not None
    ]
    if not tags:
        return base

    tags, nums = zip(*tags)
    return f"{base}-{'-'.join(tags)}.{'.'.join([str(v) for v in nums])}"


def main(data):
    py_version = data.get("dev_version") or data.get("new_version")
    npm_version = to_npm_version(py_version)
    with open("package.json", "r+") as f:
        json_data = json.load(f)
        f.seek(0)
        json.dump(
            {**json_data, "version": npm_version}, f, sort_keys=True, indent=2
        )
        f.write("\n")
        f.truncate()
