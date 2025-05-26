from fastapi.responses import JSONResponse

def response_success_handler(message: str, data=None):
    return JSONResponse(status_code=200, content={"success": True, "message": message, "data": data})

def response_error_handler(status: int, message: str):
    return JSONResponse(status_code=status, content={"success": False, "message": message})
