"""Import jobs from json file"""

import logging
import getpass
from typing import Dict
import urllib3
import json
import argparse
from pathlib import Path
import sys


FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("import_jobs")


def import_jobs(
    hostname: str, job: Dict, api_token: str, http_schema: str = "http"
) -> None:
    """Import jobs"""

    endpoint = "/api/v1/jobs/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {(api_token)}",
    }

    url = "%s://%s%s" % (http_schema, hostname, endpoint)

    title = job.get("title")

    try:
        logger.info("Importing job `%s`", title)

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            url,
            headers=headers,
            body=json.dumps(job).encode("utf-8"),
            redirect=True,
        )

        if response.status in [200, 201]:
            logger.info("Imported job `%s`", title)
        elif response.status == 401:
            logger.error("Invalid API key")
        elif response.status == 403:
            logger.error("Forbidden")
        else:
            logger.error("Something went wrong")
    except Exception as e:
        logger.error("Failed to import job `%s`, %s", title, str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server", dest="hostname", required=True, help="Server hostname / FQDN"
    )
    parser.add_argument(
        "--file", dest="jobs_file", default="moni_jobs.json", help="Jobs JSON file"
    )
    parser.add_argument(
        "--schema", dest="schema", default="http", help="HTTP Protocol (https/http)"
    )
    args = parser.parse_args()

    hostname = args.hostname
    jobs_file = Path(args.jobs_file)
    schema = args.schema
    api_token = getpass.getpass(prompt="Enter API token: ")

    if schema not in ["http", "https"]:
        logger.error("Invalid schema specified.")
        sys.exit(1)

    logger.info("Loading jobs file %s", jobs_file.name)

    if not jobs_file.is_file():
        logger.error("Jobs file %s not found", jobs_file.name)
        sys.exit(1)

    with open(jobs_file) as jf:
        jobs = json.loads(jf.read())

    logger.info("Found %s jobs", len(jobs))

    for job in jobs:
        import_jobs(hostname, job, api_token, http_schema=schema)
