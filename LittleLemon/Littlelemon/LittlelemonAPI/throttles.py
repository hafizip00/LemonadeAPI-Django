from rest_framework.throttling import UserRateThrottle

class TenCallsThrottles(UserRateThrottle):
    scope = 'ten'