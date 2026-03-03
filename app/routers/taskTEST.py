@router.put("/tasks/{task_id}")
async def update_task(task_id: int, payload: TaskUpdate, user=Depends(auth), db=Depends(get_db)):

    # 1. Load the task
    task = await db.get(Task, task_id)

    # 2. Capture old values
    old = {
        "status": task.status,
        "title": task.title
    }

    # 3. Apply updates
    task.status = payload.status
    task.title = payload.title or task.title
    await db.commit()

    # 4. Capture new values
    new = {
        "status": task.status,
        "title": task.title
    }

    # 5. Write audit log entry
    await write_audit_log(
        db,
        entity_type="task",          # literal string
        entity_id=task_id,           # the row being changed
        account_id=task.account_id,  # comes from the entity or user context
        performed_by=user.user_id,   # logged-in user
        action="update",             # literal string
        details={"old": old, "new": new}
    )

    return task

