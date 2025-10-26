from fastapi import HTTPException, status

class DataValidationError(HTTPException):
    def __init__(self, field: str, message: str = "is required"):
        detail = {"error": "Validation failed", "details": {field: message}}
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
