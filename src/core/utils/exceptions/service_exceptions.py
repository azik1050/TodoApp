from abc import ABC


class BaseServiceException(ABC, Exception):
    status_code: int


class RecordNotFound(BaseServiceException):
    status_code = 404


class RecordAlreadyExists(BaseServiceException):
    status_code = 404


class RuleViolation(BaseServiceException):
    status_code = 400


class ServerError(BaseServiceException):
    status_code = 500
