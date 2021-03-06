"""
This code is the entry-point
"""
import json
from typing import TextIO
import click
from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    """

    :param requests: Number of requests
    :param concurrency: Number of concurrent requests
    :param json_file: (optional) path tp JSON file to persist the results
    :param url: url to request
    :return: None
    """
    # output_file = None
    # if json_file:
    #     try:
    #         output_file = open(json_file, "w")
    #     except OSError:
    #         print(f"Unable to open file{json_file}")
    #         sys.exit(1)
    total_time, request_dict = assault(url, requests, concurrency)
    results = Results(total_time, request_dict)
    display(results, json_file)


def display(results: Results, json_file: TextIO):
    """

    :param results: Instance of the Results List
    :param json_file: path to the JSON file
    :return:
    """
    if json_file:
        with open(json_file, "w") as output_file:
            print(f"We're writing to a JSON file at {json_file}")
            json.dump(
                {
                    "Successful requests": results.successful_requests(),
                    "Slowest            ": results.slowest(),
                    "fastest            ": results.fastest(),
                    "Average            ": results.average_time(),
                    "Total time         ": results.total_time,
                    "Requests Per Minute": results.requests_per_minute(),
                    "Requests Per Second": results.requests_per_second(),
                },
                output_file,
            )
            # output_file.close()
            print("... Done!")

    else:
        # print to screen
        print(".... Done!")
        print("---Results---")
        print(f"Successful requests\t{results.successful_requests()}")
        print(f"Slowest            \t{results.slowest()}s")
        print(f"fastest            \t{results.fastest()}s")
        print(f"Average            \t{results.average_time()}s")
        print(f"Total time         \t{results.total_time}s")
        print(f"Requests Per Minute\t{results.requests_per_minute()}")
        print(f"Requests Per Second\t{results.requests_per_second()}")
