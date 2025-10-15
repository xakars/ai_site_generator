from fastapi import Request


def get_s3_client(request: Request):
    return request.app.state.s3_client
