import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        total_ms = int((time.perf_counter() - start) * 1000)

        # Only inject for JSON responses
        if isinstance(response, JSONResponse):
            payload = response.body
            # Decode and modify JSON
            import json
            data = json.loads(payload.decode())
            if isinstance(data, dict):
                data["total_time_taken"] = total_ms
                # Return new JSONResponse with same status & headers
                return JSONResponse(content=data, status_code=response.status_code, headers=dict(response.headers))

        # fallback: add a header if not JSONResponse
        response.headers["X-Total-Time"] = str(total_ms)
        return response
