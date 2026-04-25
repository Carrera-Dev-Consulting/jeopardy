from jeopardy.api import app, api_settings
import uvicorn


uvicorn.run(
    app,
    host=api_settings.host,
    port=api_settings.port,
)
