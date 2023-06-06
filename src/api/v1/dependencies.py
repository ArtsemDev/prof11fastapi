from fastapi import Header, HTTPException, status


async def headers_validator(accept: str = Header(), content_type: str = Header()):
    if accept != 'application/json' or content_type != 'application/json':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
