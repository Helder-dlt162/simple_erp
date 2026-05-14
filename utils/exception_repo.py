from db.models.logger import LogLevel
from db.repositories.logger import log


def repo_exception(message, e, http_code):
    error_obj  = {"message": message, "error": e}
    log(LogLevel.ERROR, str(error_obj))
    return{"code": http_code, "body":error_obj}