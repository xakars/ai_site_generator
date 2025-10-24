from fastapi import Request


def get_s3_client(request: Request):
    return request.app.state.s3_client


def get_gotenberg_client(request: Request):
    return request.app.state.gotenberg_client
