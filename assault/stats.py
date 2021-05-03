from typing import List, Dict
import numpy as np

class Results():
    """
    Results handles calculating statistics based on a list of requests that were made;
    Here is an example of what the information will look like:
    Successful requests 3000
    Slowest 0.010s
    Fastest 0.001s
    Average 0.003s
    Total time 2.400s
    Requests Per Minute 90000
    Requests Per Second 1250
    """

    def __init__(self, total_time:float, requests:List[Dict]):
        self.total_time = total_time
        self.requests = sorted(requests, key=lambda r: r['request_time'])

    def slowest(self) -> float:
        """
        :return: the slowest request's completion time
        >>> results = Results(10.6, [{
        ... 'status_code': 200,
        ... 'request_time': 3.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 6.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.slowest()
        6.1
        """
        return self.requests[-1]['request_time']

    def fastest(self) -> float:
        """
        :return: the fastest request's completion time
        >>> results = Results(10.6, [{
        ... 'status_code': 200,
        ... 'request_time': 3.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 6.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.fastest()
        1.04
        """
        return self.requests[0]['request_time']

    def average_time(self) -> float:
        """
        :return: the average request's completion time
        >>> results = Results(10.6, [{
        ... 'status_code': 200,
        ... 'request_time': 3.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 6.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.average_time()
        3.513333333333333
        """
        return np.mean([r['request_time'] for r in self.requests])

    def successful_requests(self) -> int:
        """
        :return: the number of successfully completed requests
        >>> results = Results(10.6, [{
        ... 'status_code': 200,
        ... 'request_time': 3.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 6.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.successful_requests()
        2
        """
        return len([r['status_code'] for r in self.requests if r['status_code'] in range(200, 299)])

    def requests_per_minute(self)->int:
        """

        :return: the number of requests that could be made in one minute
        >>> results = Results(10.6, [{
        ... 'status_code': 200,
        ... 'request_time': 3.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 6.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.requests_per_minute()
        17
        """
        # 4/10.6*60
        return round(len(self.requests)/self.total_time*60)

    def requests_per_second(self)->int:
        """

        :return: the number of requests that could be made in one second
        >>> results = Results(1.5, [{
        ... 'status_code': 200,
        ... 'request_time': 1.4
        ... },{
        ... 'status_code': 500,
        ... 'request_time': 1.1
        ... },{
        ... 'status_code': 200,
        ... 'request_time': 1.04
        ... }])
        >>> results.requests_per_second()
        2
        """
        # 3/1.5
        return round(len(self.requests)/self.total_time)

