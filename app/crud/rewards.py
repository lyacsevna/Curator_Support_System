from sqlalchemy.orm import Session
from ..models.rewards import Reward
from ..schemas.rewards import RewardCreate

def get_reward_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reward).offset(skip).limit(limit).all()

def get_student_rewards(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Reward).filter(Reward.student_id == student_id).offset(skip).limit(limit).all()

def create_reward_record(db: Session, reward: RewardCreate):
    db_reward = Reward(**reward.model_dump())
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward