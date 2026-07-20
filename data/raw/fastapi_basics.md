# FastAPI Basics

FastAPI is a Python web framework for building APIs. It is built on top of
Starlette for the web layer and Pydantic for data validation, and it uses
standard Python type hints to define request and response shapes.

## Defining a route

A route is created by decorating a function with an HTTP method decorator,
such as `@app.get("/items/{item_id}")`. The function's parameters are
automatically parsed from the path, query string, or request body based on
their type hints.

## Request validation

FastAPI uses Pydantic models to validate incoming request bodies. If a
client sends data that does not match the model's field types or
constraints, FastAPI automatically returns a 422 Unprocessable Entity
response with details about which fields failed validation.

## Dependency injection

FastAPI has a built-in dependency injection system. A dependency is a
callable — often a function — that FastAPI calls before the route handler
runs, and whose return value is passed into the handler as an argument.
Dependencies are commonly used for shared logic like database sessions,
authentication, or pagination parameters.

## Automatic documentation

Because FastAPI reads type hints and Pydantic models, it can generate
interactive API documentation automatically. By default this is available
at the `/docs` path (Swagger UI) and the `/redoc` path (ReDoc).

## Async support

Route handlers can be defined with `async def` to take advantage of
asynchronous I/O, which is useful when a handler needs to await network
calls, such as database queries or requests to external services. Handlers
can also be defined as regular `def` functions; FastAPI runs those in a
thread pool automatically.

## Troubleshooting: 422 errors

A 422 response usually means the request body, query parameters, or path
parameters did not match what the route's type hints or Pydantic model
expect. Check the `detail` field in the JSON response — it lists exactly
which field failed and why.
