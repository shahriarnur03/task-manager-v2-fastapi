# Task App Architecture Notes

This file is a learning guide for making the current FastAPI task app more reusable, easier to reason about, and ready for future features like student-owned tasks and task sharing.

The goal is not to make the project complicated. The goal is to give every file one clear job.

## Current Situation

Your app already has a good beginner-friendly base:

- `src/api/routers/task_route.py` handles HTTP endpoints.
- `src/schemas/task.py` defines request and response data shapes.
- `src/db/models.py` defines the database table.
- `src/core/response.py` keeps response formatting reusable.
- `src/core/exceptions.py` keeps error formatting consistent.

The main confusion is here:

- `src/services/task_service.py` currently talks directly to the database.
- That means the service is acting like both a service and a repository.
- `src/repositories/` exists, but `task_repository.py` is missing from the current code tree.

So when you ask "is this service task or repository task?", your feeling is correct. The boundary is not clear yet.

## Simple Mental Model

Think of the app in layers:

1. Router

   Job: HTTP only.

   The router should understand FastAPI things like path params, query params, request body, status codes, and dependencies.

   It should not know database query details.

2. Schema

   Job: API data shape.

   Schemas describe what data comes into the API and what data goes out.

   They should not contain database logic.

3. Service

   Job: business rules.

   The service answers questions like:

   - Is this student allowed to see this task?
   - Can this task be shared?
   - What should happen when a task is completed?
   - Should we raise not found or forbidden?

   The service should call the repository when it needs data.

4. Repository

   Job: database queries.

   The repository should contain SQLAlchemy query logic:

   - create row
   - find row by id
   - list rows with pagination
   - update row
   - delete row
   - query tasks owned by a student
   - query tasks shared with a student

5. DB Model

   Job: database table mapping.

   Models represent tables and relationships.

## Recommended Folder Shape

Keep the current project style, but make the boundaries clearer:

```text
src/
  api/
    routers/
      task_route.py
      student_route.py
  core/
    config.py
    exceptions.py
    response.py
  db/
    connection.py
    deps.py
    models.py
  repositories/
    task_repository.py
    student_repository.py
    task_share_repository.py
  schemas/
    task.py
    student.py
    response.py
  services/
    task_service.py
    student_service.py
    task_share_service.py
```

You do not need to create all files immediately. Add them only when the feature needs them.

## Naming Advice

Use names that explain the layer.

Good schema names:

- `TaskCreate`
- `TaskUpdate`
- `TaskRead`
- `TaskListItem`
- `TaskShareCreate`
- `TaskShareRead`

Avoid using only `Task` for a schema if you also have a SQLAlchemy model named `Task`. It becomes confusing because `Task` can mean database model or API response.

Better:

- Database model: `Task`
- Response schema: `TaskRead`
- Create schema: `TaskCreate`
- Update schema: `TaskUpdate`

Also consider using Python-style field names inside your app:

- `is_completed`
- `owner_id`
- `created_at`

If you want API JSON to show camelCase later, Pydantic can handle aliases. Internally, snake_case is easier in Python.

## Current Code Suggestions

These are the highest-impact improvements for your current app.

1. Split repository from service.

   Move direct SQLAlchemy code from `task_service.py` into `task_repository.py`.

   After that:

   - router calls service
   - service calls repository
   - repository talks to database

2. Add separate create, update, and read schemas.

   Right now `TaskCreate` is also used for update.

   That is okay for learning, but in real apps create and update often become different.

   Example idea:

   - create requires `title`
   - update may allow only `title`
   - complete/uncomplete may have its own endpoint or schema

3. Keep response helpers.

   Your `success_response` and `paginated_response` helpers are a good reusable idea.

4. Move database URL into settings.

   `DATABASE_URL` is currently hardcoded in `src/db/connection.py`.

   For production, load it from environment variables using `pydantic-settings`.

5. Use migrations instead of `Base.metadata.create_all`.

   `create_all` is fine when learning.

   For production, Alembic is better because it tracks database changes step by step.

6. Add ownership before sharing.

   Do not build sharing first.

   First make sure every task belongs to one student. Sharing becomes much easier after ownership is clear.

## Future Feature Design

You said later:

- student has their own task
- student can send/share task to another student
- student can see their own tasks and tasks shared by others

That suggests three main concepts:

1. Student

   A student is a user of the app.

   Important fields:

   - id
   - name
   - email
   - created_at

2. Task

   A task belongs to one owner student.

   Important fields:

   - id
   - title
   - is_completed
   - owner_id
   - created_at
   - updated_at

3. TaskShare

   A task share connects one task to another student.

   Important fields:

   - id
   - task_id
   - shared_with_student_id
   - shared_by_student_id
   - permission
   - created_at

The `permission` field can start simple:

- `view`
- `edit`

For the first version, you can support only `view`. Add `edit` later.

## Relationship Rules

Use these rules in your mind before coding:

- A task has exactly one owner.
- A student can own many tasks.
- A task can be shared with many students.
- A student can receive many shared tasks.
- The owner can always see their own task.
- A shared student can see the task only if a share row exists.
- Only the owner should be able to share the task.
- Only the owner should be able to delete the task.

These rules belong in the service layer, not in the router.

## Endpoint Ideas

Start simple and grow slowly.

Current task endpoints:

```text
POST   /tasks
GET    /tasks
GET    /tasks/{task_id}
PUT    /tasks/{task_id}
DELETE /tasks/{task_id}
```

Future student-aware task endpoints:

```text
POST   /tasks
GET    /tasks/mine
GET    /tasks/shared-with-me
GET    /tasks/{task_id}
PATCH  /tasks/{task_id}
DELETE /tasks/{task_id}
POST   /tasks/{task_id}/shares
DELETE /tasks/{task_id}/shares/{student_id}
```

You can also keep `GET /tasks` and use a query:

```text
GET /tasks?view=mine
GET /tasks?view=shared
GET /tasks?view=all
```

For beginners, separate endpoints are easier to understand.

## How Each Layer Would Work

Example flow: create task.

```text
router receives request
router gets current student from auth dependency
router calls task_service.create_task(...)
service applies rule: task owner is current student
service calls task_repository.create(...)
repository saves task to database
service returns task
router formats success response
```

Example flow: get task by id.

```text
router receives task_id
router gets current student
router calls task_service.get_task_for_student(...)
service asks repository for task
service checks if current student is owner or shared student
service returns task or raises 404/403
router formats response
```

Example flow: share task.

```text
router receives task_id and target student id
router gets current student
router calls task_share_service.share_task(...)
service checks task exists
service checks current student owns the task
service checks target student exists
service checks task is not already shared with that student
service calls task_share_repository.create(...)
router returns success response
```

## Beginner-Friendly Build Order

Follow this order when you code. It avoids too many moving parts at once.

1. Rename schemas mentally first.

   Change API schema names from general names to clear names:

   - `TaskCreate`
   - `TaskUpdate`
   - `TaskRead`

2. Create `task_repository.py`.

   Move database query functions there.

   Keep the service function names similar for now so the app still feels familiar.

3. Make `task_service.py` call `task_repository.py`.

   At this stage, behavior should stay almost the same.

4. Add tests for service behavior.

   Test service rules, not FastAPI response formatting first.

5. Add `Student` model and schema.

   Do not add auth yet if that feels too much.

   You can temporarily pass `student_id` manually while learning.

6. Add `owner_id` to tasks.

   After this, every task should belong to a student.

7. Add "my tasks" listing.

   Query tasks where `Task.owner_id == current_student.id`.

8. Add `TaskShare` model.

   This is the join table between tasks and students.

9. Add "shared with me" listing.

   Query task shares where `TaskShare.shared_with_student_id == current_student.id`.

10. Add permission checks.

   Put these checks in service functions.

## Service vs Repository Cheat Sheet

Put this in repository:

- SQLAlchemy filters
- joins
- offset and limit
- commit and refresh
- finding rows by id
- counting rows

Put this in service:

- "student can only edit their own task"
- "student can view own or shared task"
- "only owner can share"
- "do not share task twice with same student"
- choosing which repository function to call
- raising app-level errors

Put this in router:

- route path
- request body
- query params
- dependency injection
- HTTP status code
- response model
- calling response helper

## Production-Level Ideas For Later

Do these later, not all at once:

- Add `created_at` and `updated_at` columns.
- Add `TaskStatus` enum if task state grows beyond true/false.
- Add Alembic migrations.
- Add settings with environment variables.
- Add authentication and `get_current_student`.
- Add pagination schemas/helpers for all list endpoints.
- Add unique constraint so the same task cannot be shared twice with the same student.
- Add indexes on `owner_id`, `task_id`, and `shared_with_student_id`.
- Add tests for permission rules.

## Good Test Cases To Write Later

Start with these:

- create task returns task with correct title
- list tasks returns pagination shape
- update missing task returns not found
- delete missing task returns not found
- student can see own task
- student cannot see another student's private task
- owner can share task
- non-owner cannot share task
- shared student can see shared task
- same task cannot be shared twice with same student

## Final Direction

Your next best move is not to add the student-sharing feature immediately.

First make the current task feature clean:

```text
router -> service -> repository -> database
```

Once that feels natural, add:

```text
student ownership -> my tasks -> task sharing -> shared with me
```

That order will keep the project beginner-friendly while still moving toward production-level structure.
