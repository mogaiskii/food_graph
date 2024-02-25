from api.rest import rest_app


@rest_app.get("/health")
async def health_check():
    return {"status": "OK"}
