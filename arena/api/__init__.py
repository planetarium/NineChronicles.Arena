from fastapi import APIRouter

from arena.api import dummy

router = APIRouter(
    prefix="/api",
    # tags=["API"],
)

__all__ = [
    dummy,
]

for view in __all__:
    router.include_router(view.router)
