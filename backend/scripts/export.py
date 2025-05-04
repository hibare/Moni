"""Export Jobs to JSON file"""

import logging
import getpass
import urllib3
import json
import argparse

FORMAT = "%(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("export_jobs")


def export_jobs(
    hostname: str,
    api_token: str,
    http_schema: str = "http",
    output_file: str = "moni_jobs.json",
) -> None:
    """Export Jobs"""

    endpoint = "/api/v1/jobs/"
    headers = {"Authorization": f"Token {(api_token)}"}

    url = "%s://%s%s" % (http_schema, hostname, endpoint)

    try:
        logger.info("Fetching data...")

        http = urllib3.PoolManager()
        response = http.request(
            "GET",
            url,
            headers=headers,
        )

        if response.status == 200:
            jobs = json.loads(response.data.decode())

            logger.info("Found %s jobs", len(jobs))

            with open(output_file, "w", encoding="utf_8") as output_fh:
                output_fh.write(json.dumps(jobs, indent=4))

            logger.info("Saved jobs to %s", output_file)
        elif response.status == 401:
            logger.error("Invalid API key")
        elif response.status == 403:
            logger.error("Forbidden")
        else:
            logger.error("Something went wrong")

    except Exception as e:
        logger.error("Failed to export jobs: %s", str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", dest="hostname", required=True, help="Server hostname / FQDN"
    )
    args = parser.parse_args()

    hostname = args.hostname
    api_token = getpass.getpass(prompt="Enter API token: ")

    export_jobs(hostname, api_token)
