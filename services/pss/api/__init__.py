from .documents import router as documents_router
from .verification import router as verification_router
from .compliance import router as compliance_router


__all__ = ["documents_router", "verification_router", "compliance_router"]
