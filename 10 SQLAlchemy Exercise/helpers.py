def session_handler(session, autoclose=True):
    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                session.commit()

                return result

            except Exception as e:
                session.rollback()
                raise e

            finally:
                if autoclose:
                    session.close()

        return wrapper
    return decorator
