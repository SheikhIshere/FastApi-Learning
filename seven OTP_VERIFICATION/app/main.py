from fastapi import FastAPI

app = FastAPI()


@app.get('/', include_in_schema=False)
def warning():
    return {'error': 'Permission denied'}

@app.get('/health-check')
def check():
    return {'message': 'fuck you'}

"""
title=settings.app_name,
version=settings.app_version,
description="A professional FastAPI application with SMTP functionality",
openapi_url=f"/api/v1/openapi.json"
"""