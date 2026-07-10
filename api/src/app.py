from typing import Annotated, Any, Dict

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.agent.gemini_planner import GeminiPlanner, create_gemini_planner
from src.agent.orchestrator import investigate_dispute
from src.data.disputes import disputes
from src.models import Dispute, DisputesResponse, ErrorResponse, HealthResponse


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React dev server
            "http://127.0.0.1:3000",
            "http://0.0.0.0:3000",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )


def get_planner() -> GeminiPlanner:
    return create_gemini_planner()


app = FastAPI(title="ChargeShield API", description="AI-powered dispute investigation system", version="1.0.0")

configure_cors(app)

PlannerDep = Annotated[GeminiPlanner, Depends(get_planner)]


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(ok=True)


@app.get("/api/disputes", response_model=DisputesResponse)
async def get_disputes() -> DisputesResponse:
    disputes_list = [Dispute(**dispute_data) for dispute_data in disputes.values()]
    return DisputesResponse(disputes=disputes_list)


@app.post(
    "/api/disputes/{dispute_id}/investigate",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Dispute not found",
        },
        500: {
            "model": ErrorResponse,
            "description": "Investigation failed",
        },
    },
)
async def investigate_dispute_endpoint(dispute_id: str, planner: PlannerDep) -> Dict[str, Any]:
    if dispute_id not in disputes:
        error_response = ErrorResponse(message=f"Dispute ID {dispute_id} not found")
        return JSONResponse(status_code=404, content=error_response.model_dump())

    dispute = disputes[dispute_id]

    try:
        result = await investigate_dispute(dispute, planner)
    except Exception as exc:
        error_response = ErrorResponse(message=f"Investigation failed, reason: {str(exc)}, error: {type(exc)}")
        return JSONResponse(status_code=500, content=error_response.model_dump())

    return result
