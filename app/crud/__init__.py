# Импортируем все CRUD модули для удобного доступа
from .study_programs import (
    get_program, get_programs, create_program,
    update_program, delete_program
)
from .curators import (
    get_curator, get_curators, get_curator_by_email,
    create_curator, authenticate_curator
)
from .groups import (
    get_group, get_groups, create_group,
    update_group, delete_group
)
from .students import (
    get_student, get_students, get_students_by_group,
    create_student, update_student, delete_student
)
from .student_history import (
    get_history_records, get_history_for_student,
    create_history_record
)
from .performance import (
    get_performance_record, get_performance_records,
    get_student_performance, create_performance_record,
    update_performance_record, delete_performance_record
)
from .activities import (
    get_activity, get_activities, get_student_activities,
    create_activity, update_activity, delete_activity
)
from .financial_support import (
    get_financial_support_records, get_student_financial_support,
    create_financial_support_record
)
from .dormitory import (
    get_dormitory_record, get_dormitory_records,
    get_student_dormitory, create_dormitory_record,
    update_dormitory_record, delete_dormitory_record
)
from .rewards import (
    get_reward_records, get_student_rewards,
    create_reward_record
)
from .documents import (
    get_document, get_documents, get_entity_documents,
    create_document_record, delete_document_record
)
from .curator_plans import (
    get_curator_plan, get_curator_plans, get_group_plans,
    create_curator_plan, update_curator_plan, delete_curator_plan
)

__all__ = [
    'get_program', 'get_programs', 'create_program', 'update_program', 'delete_program',
    'get_curator', 'get_curators', 'get_curator_by_email', 'create_curator', 'authenticate_curator',
    'get_group', 'get_groups', 'create_group', 'update_group', 'delete_group',
    'get_student', 'get_students', 'get_students_by_group', 'create_student', 'update_student', 'delete_student',
    'get_history_records', 'get_history_for_student', 'create_history_record',
    'get_performance_record', 'get_performance_records', 'get_student_performance',
    'create_performance_record', 'update_performance_record', 'delete_performance_record',
    'get_activity', 'get_activities', 'get_student_activities', 'create_activity',
    'update_activity', 'delete_activity',
    'get_financial_support_records', 'get_student_financial_support', 'create_financial_support_record',
    'get_dormitory_record', 'get_dormitory_records', 'get_student_dormitory',
    'create_dormitory_record', 'update_dormitory_record', 'delete_dormitory_record',
    'get_reward_records', 'get_student_rewards', 'create_reward_record',
    'get_document', 'get_documents', 'get_entity_documents', 'create_document_record', 'delete_document_record',
    'get_curator_plan', 'get_curator_plans', 'get_group_plans', 'create_curator_plan',
    'update_curator_plan', 'delete_curator_plan'
]