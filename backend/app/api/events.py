"""Event ingestion endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventListResponse, EventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
def ingest_event(payload: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(
        user_id=payload.user_id,
        event_type=payload.event_type,
        event_name=payload.event_name,
        properties=payload.properties,
        source=payload.source,
        timestamp=payload.timestamp or datetime.now(timezone.utc),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.post("/batch", response_model=list[EventResponse], status_code=201)
def batch_ingest(
    payloads: list[EventCreate], db: Session = Depends(get_db)
) -> list[Event]:
    events: list[Event] = []
    for payload in payloads:
        event = Event(
            user_id=payload.user_id,
            event_type=payload.event_type,
            event_name=payload.event_name,
            properties=payload.properties,
            source=payload.source,
            timestamp=payload.timestamp or datetime.now(timezone.utc),
        )
        db.add(event)
        events.append(event)
    db.commit()
    for e in events:
        db.refresh(e)
    return events


@router.get("/{user_id}", response_model=EventListResponse)
def get_user_events(
    user_id: str,
    event_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> dict:
    query = db.query(Event).filter(Event.user_id == user_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    total = query.count()
    events = (
        query.order_by(Event.timestamp.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {"events": events, "total": total}
