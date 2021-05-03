import asyncio
import time
import os
import requests
import pprint


def fetch(url):

    started_at = time.monotonic()
    response = requests.get(url)
    took = time.monotonic()-started_at
    return{'status_code': response.status_code,
           'request_time': took}

# A function to take unmade requests from a queue, perform the work, and add result to the queue
async def worker(name, queue, results):

    # get the event loop that our current asynchronous code is running within
    loop = asyncio.get_event_loop()

    while True:
        # get the URL from  the queue
        url = await queue.get()  # wait for a value to be returned to us

        if os.getenv('DEBUG'):
            print(f'{name:20} : {url}')

        future_result = loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        queue.task_done()


# Divide up work into batches and collect final results
async def distribute_work(url, requests, concurrency, results):

    # We'll start by creating an asyncio.Queue that we can add our URL
    # to once for each request that we'd like to make
    queue = asyncio.Queue()

    # Add an item to the queue for each request we want to make
    for _ in range(requests):
        queue.put_nowait(url)

    # Create workers to match the concurrency
    tasks = []
    for i in range(requests):
        task = asyncio.create_task(worker(f'worker{i+1}', queue, results))
        tasks.append(task)

    started_at = time.monotonic()
    # waiting for the items in the queue to be processed
    await queue.join()
    total_time = time.monotonic() - started_at

    # print(f'{concurrency} workers took {total_time:.2f} seconds to complete {requests} requests')

    # cancel all the tasks to avoid infinite loops
    for tasks in tasks:
        task.cancel()
    return total_time


# Entrypoint to making requests (SYCHRONUS function)
def assault(url, requests, concurrency):
    results = []
    total_time = asyncio.run(distribute_work(url, requests, concurrency, results))
    # pprint.pprint(results)
    return total_time, results
