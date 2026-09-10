from sqlalchemy import text
from sqlalchemy.engine import Engine


def get_descendant_department_ids(engine: Engine, root_id: int) -> set[int]:
    """
    Возвращает id отдела и всех его потомков (рекурсивно).
    """
    result = {root_id}
    frontier = [root_id]

    while frontier:
        with engine.connect() as conn:
            rows = conn.execute(
                text("SELECT id FROM departments WHERE parent_id = ANY(:ids)"),
                {"ids": frontier},
            ).fetchall()
        new_ids = {r[0] for r in rows} - result
        result |= new_ids
        frontier = list(new_ids)

    return result


def would_create_cycle(engine: Engine, dept_id: int, new_parent_id: int | None) -> bool:
    """
    Проверяет, создаст ли перенос отдела цикл.
    True — если переносить нельзя.
    """
    if new_parent_id is None:
        return False
    if dept_id == new_parent_id:
        return True
    descendants = get_descendant_department_ids(engine, dept_id)
    return new_parent_id in descendants


def build_department_tree(engine: Engine) -> list[dict]:
    """
    Собирает плоский список отделов в дерево для фронта.
    """
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, name, parent_id, manager_id FROM departments")
        ).fetchall()

    departments = [
        {"id": r[0], "name": r[1], "parent_id": r[2], "manager_id": r[3]}
        for r in rows
    ]

    by_parent: dict[int | None, list[dict]] = {}
    for d in departments:
        by_parent.setdefault(d["parent_id"], []).append(d)

    def build_node(d: dict) -> dict:
        return {
            "id": d["id"],
            "name": d["name"],
            "manager_id": d["manager_id"],
            "children": [build_node(child) for child in by_parent.get(d["id"], [])],
        }

    roots = by_parent.get(None, [])
    return [build_node(r) for r in roots]