from fastapi import APIRouter
# Перенесите импорты на уровень модуля, а не внутри функции
from .study_programs import router as study_programs_router
from .curators import router as curators_router
from .groups import router as groups_router
from .students import router as students_router
from .student_history import router as student_history_router
from .performance import router as performance_router
from .activities import router as activities_router
from .financial_support import router as financial_support_router
from .dormitory import router as dormitory_router
from .rewards import router as rewards_router
from .documents import router as documents_router
from .curator_plans import router as curator_plans_router


api_router = APIRouter()


api_router.include_router(study_programs_router, prefix="/study-programs", tags=["study-programs"])
api_router.include_router(curators_router, prefix="/curators", tags=["curators"])
api_router.include_router(groups_router, prefix="/groups", tags=["groups"])
api_router.include_router(students_router, prefix="/students", tags=["students"])
api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
api_router.include_router(student_history_router, prefix="/student-history", tags=["student-history"])
api_router.include_router(performance_router, prefix="/performance", tags=["performance"])
api_router.include_router(activities_router, prefix="/activities", tags=["activities"])
api_router.include_router(financial_support_router, prefix="/financial-support", tags=["financial-support"])
api_router.include_router(dormitory_router, prefix="/dormitory", tags=["dormitory"])
api_router.include_router(rewards_router, prefix="/rewards", tags=["rewards"])
api_router.include_router(curator_plans_router, prefix="/curator-plans", tags=["curator-plans"])