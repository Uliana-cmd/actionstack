from sqlalchemy.orm import Session
from app.models.department import Department
from app.models.user import User


def get_descendant_department_ids(db: Session, root_id: int) -> set[int]:
    """
    Возвращает id отдела и всех его потомков (рекурсивно).
    """
    result = {root_id}
    frontier = [root_id]

    while frontier:
        rows = (
            db.query(Department.id)
            .filter(Department.parent_id.in_(frontier))
            .all()
        )
        new_ids = {row[0] for row in rows} - result
        result |= new_ids
        frontier = list(new_ids)

    return result


def get_subtree_user_ids(db: Session, root_user_id: int) -> set[int]:
    """
    Возвращает id пользователя и всех его подчинённых (рекурсивно).
    """
    result = {root_user_id}
    frontier = [root_user_id]

    while frontier:
        rows = (
            db.query(User.id)
            .filter(User.manager_id.in_(frontier))
            .all()
        )
        new_ids = {row[0] for row in rows} - result
        result |= new_ids
        frontier = list(new_ids)

    return result


def would_create_cycle(db: Session, dept_id: int, new_parent_id: int | None) -> bool:
    """
    Проверяет, создаст ли перенос отдела цикл.
    True — если переносить нельзя.
    """
    if new_parent_id is None:
        return False
    if dept_id == new_parent_id:
        return True
    descendants = get_descendant_department_ids(db, dept_id)
    return new_parent_id in descendants


def would_create_user_cycle(db: Session, user_id: int, new_manager_id: int | None) -> bool:
    """
    Проверяет, создаст ли смена руководителя цикл.
    True — если менять нельзя.
    """
    if new_manager_id is None:
        return False
    if user_id == new_manager_id:
        return True
    subordinates = get_subtree_user_ids(db, user_id)
    return new_manager_id in subordinates


def build_department_tree(db: Session) -> list[dict]:
    """
    Собирает плоский список отделов в дерево для фронта.
    """
    all_departments = db.query(Department).all()

    by_parent: dict[int | None, list[Department]] = {}
    for d in all_departments:
        by_parent.setdefault(d.parent_id, []).append(d)

    def build_node(d: Department) -> dict:
        return {
            "id": d.id,
            "name": d.name,
            "head_user_id": d.head_user_id,
            "children": [build_node(child) for child in by_parent.get(d.id, [])],
        }

    roots = by_parent.get(None, [])
    return [build_node(r) for r in roots]