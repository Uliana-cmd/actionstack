from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.plan import PlanCreate, PlanRead
from app.dependencies import get_db, get_current_user
from app.crud import plan as plan_crud

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("", response_model=PlanRead, status_code=201)
def create_plan(
    data: PlanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return plan_crud.create(db, data, user_id=current_user.id)


@router.get("", response_model=list[PlanRead])
def list_plans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return plan_crud.list_for_user(db, user_id=current_user.id)