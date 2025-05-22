# Импортируем все схемы для удобного доступа
from .study_programs import StudyProgram, StudyProgramCreate, StudyProgramUpdate
from .curators import Curator, CuratorCreate, CuratorUpdate, Token, TokenData
from .groups import Group, GroupCreate, GroupUpdate
from .students import Student, StudentCreate, StudentUpdate
from .student_history import StudentHistory, StudentHistoryCreate
from .performance import Performance, PerformanceCreate, PerformanceUpdate
from .activities import Activity, ActivityCreate, ActivityUpdate
from .financial_support import FinancialSupport, FinancialSupportCreate
from .dormitory import Dormitory, DormitoryCreate, DormitoryUpdate
from .rewards import Reward, RewardCreate
from .documents import Document, DocumentCreate
from .curator_plans import CuratorPlan, CuratorPlanCreate, CuratorPlanUpdate

__all__ = [
    'StudyProgram', 'StudyProgramCreate', 'StudyProgramUpdate',
    'Curator', 'CuratorCreate', 'CuratorUpdate', 'Token', 'TokenData',
    'Group', 'GroupCreate', 'GroupUpdate',
    'Student', 'StudentCreate', 'StudentUpdate',
    'StudentHistory', 'StudentHistoryCreate',
    'Performance', 'PerformanceCreate', 'PerformanceUpdate',
    'Activity', 'ActivityCreate', 'ActivityUpdate',
    'FinancialSupport', 'FinancialSupportCreate',
    'Dormitory', 'DormitoryCreate', 'DormitoryUpdate',
    'Reward', 'RewardCreate',
    'Document', 'DocumentCreate',
    'CuratorPlan', 'CuratorPlanCreate', 'CuratorPlanUpdate'
]