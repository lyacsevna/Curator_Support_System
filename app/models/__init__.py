from .base import Base
from .study_programs import StudyProgram
from .curators import Curator
from .groups import Group
from .students import Student
from .student_history import StudentHistory
from .performance import Performance
from .activities import Activity
from .financial_support import FinancialSupport
from .dormitory import Dormitory
from .rewards import Reward
from .documents import Document
from .curator_plans import CuratorPlan


# Устанавливаем relationships для всех моделей
from sqlalchemy.orm import relationship

# StudyProgram
StudyProgram.groups = relationship("Group", back_populates="study_program")

# Curator
Curator.groups = relationship("Group", back_populates="curator")
Curator.plans = relationship("CuratorPlan", back_populates="curator")

# Group
Group.study_program = relationship("StudyProgram", back_populates="groups")
Group.curator = relationship("Curator", back_populates="groups")
Group.students = relationship("Student", back_populates="group")
Group.plans = relationship("CuratorPlan", back_populates="group")

# Student
Student.group = relationship("Group", back_populates="students")
Student.history = relationship("StudentHistory", back_populates="student")
Student.performance = relationship("Performance", back_populates="student")
Student.activities = relationship("Activity", back_populates="student")
Student.financial_support = relationship("FinancialSupport", back_populates="student")
Student.dormitory = relationship("Dormitory", back_populates="student")
Student.rewards = relationship("Reward", back_populates="student")


# StudentHistory
StudentHistory.student = relationship("Student", back_populates="history")
StudentHistory.group = relationship("Group")

# Performance
Performance.student = relationship("Student", back_populates="performance")

# Activity
Activity.student = relationship("Student", back_populates="activities")

# FinancialSupport
FinancialSupport.student = relationship("Student", back_populates="financial_support")

# Dormitory
Dormitory.student = relationship("Student", back_populates="dormitory")

# Reward
Reward.student = relationship("Student", back_populates="rewards")

# CuratorPlan
CuratorPlan.group = relationship("Group", back_populates="plans")
CuratorPlan.curator = relationship("Curator", back_populates="plans")

__all__ = [
    'Base',
    'StudyProgram',
    'Curator',
    'Group',
    'Student',
    'StudentHistory',
    'Performance',
    'Activity',
    'FinancialSupport',
    'Dormitory',
    'Reward',
    'Document',
    'CuratorPlan'
]