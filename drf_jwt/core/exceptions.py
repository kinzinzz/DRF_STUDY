from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    
    # 모든 exception을 DRF에서 제공하는 exception handler를 response로 먼저 받음
    response = exception_handler(exc, context)
    
    # 처리할 수 있는 exception error
    handlers = {
        'ValidationError': _handle_generic_error
    }
    
    # exception type 식별
    exception_class = exc.__class__.__name__

    # exception type 식별
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
	# 처리할 수 없는 exception type이면 DRF에서 제공하는 exception_handler를 그대로 사용
    return response

def _handle_generic_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response