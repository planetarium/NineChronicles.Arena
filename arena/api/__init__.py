from fastapi import APIRouter

from arena.api import dummy, arena

router = APIRouter(
    prefix="/api",
    # tags=["API"],
)

__all__ = [
    arena,
    dummy,
]

for view in __all__:
    router.include_router(view.router)
