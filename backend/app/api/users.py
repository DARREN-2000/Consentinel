"""User CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.engine.fatigue import FatigueEngine
from app.engine.scoring import ScoringEngine
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserScoresResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])
scoring_engine = ScoringEngine()
fatigue_engine = FatigueEngine()


@router.post("", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    user = User(
        external_id=payload.external_id,
        email=payload.email,
        name=payload.name,
        company_name=payload.company_name,
        company_size=payload.company_size,
        lifecycle_stage=payload.lifecycle_stage,
        preferred_channel=payload.preferred_channel,
        metadata_=payload.metadata_,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=UserListResponse)
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lifecycle_stage: str | None = None,
    db: Session = Depends(get_db),
) -> dict:
    query = db.query(User)
    if lifecycle_stage:
        query = query.filter(User.lifecycle_stage == lifecycle_stage)
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"users": users, "total": total, "page": page, "page_size": page_size}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str, payload: UserUpdate, db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}/scores", response_model=UserScoresResponse)
def get_user_scores(user_id: str, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    scores = scoring_engine.update_user_scores(user_id, db)
    scores["fatigue_score"] = fatigue_engine.update_user_fatigue(user_id, db)
    scores["user_id"] = user_id
    return scores
