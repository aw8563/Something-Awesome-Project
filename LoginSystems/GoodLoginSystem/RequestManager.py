from flask import request, abort
from collections import deque
from time import time


class RequestManager:

    def __init__(self, limit=60, timeframe=60):
        # maximum number of requests in a given time period before they are blocked
        # they must be positive. Will be set to 1 if negative
        # by default they are set to maximum of 60 requests per minute
        self.limit = max(limit, 1)
        self.timeframe = max(timeframe, 1)

        # map with key = ip address, value = deque that stores timestamps of requests
        self.requests = {}

    def checkRequest(self, ip):
        now = time()
        dq = self.requests.get(ip) # timestamps of when the ip requested

        if dq: # ip has requested previously
            # remove the times older than currenttime - timeframe
            while (len(dq) > 0 and now - dq[0] > self.timeframe):
                dq.popleft()

            # if there are too many requests, return false
            if len(dq) >= self.limit:
                return False

        else: # ip has not visited before
            # add to map
            dq = deque()
            self.requests[ip] = dq

        # add new time in
        dq.append(time())
        return True

    # decorate with this function to make the page not take too many requests
    def limitRequestsDecorator(self, function):
        def wrapper():
            # if too many requests, return 403 error
            if not self.checkRequest(request.environ['REMOTE_ADDR']):
                abort(403)

            # otherwise return the appropriate page
            return function()
        return wrapper
