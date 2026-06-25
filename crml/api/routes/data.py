from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/data/stats")
async def data_stats(request: Request):
    store = request.app.state.store
    return store.stats()
