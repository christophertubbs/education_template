# STYLE.md

# Programming Style Guide

## 1. Purpose

This document defines the programming style and implementation conventions for this repository.

All new code and substantially modified code must follow these rules unless a documented technical constraint requires otherwise.

The primary goals are:

* readability;
* maintainability;
* testability;
* explicit behavior;
* strong typing;
* useful documentation;
* portability between deployment environments;
* use of established libraries and framework conventions;
* avoidance of unnecessary cleverness.

Code should be straightforward for another developer or coding agent to understand without reconstructing the author's intent.

---

## 2. General Principles

Prefer simple, explicit implementations over clever or compressed code.

Code should communicate intent through:

* descriptive names;
* small functions;
* explicit control flow;
* clear abstractions;
* type annotations;
* documentation;
* structured logging;
* automated tests.

Avoid unnecessary indirection, abstraction, inheritance, metaprogramming, or framework construction.

Abstraction should solve an identified problem rather than anticipate every theoretically possible future requirement.

However, abstractions are encouraged where radically different implementations may reasonably be required in different environments.

Examples include:

* retrieving data from local storage versus Amazon S3;
* retrieving S3 data through different providers or credential mechanisms;
* interacting with different remote APIs;
* performing web requests through different transports;
* changing persistence implementations;
* supporting local, cloud, and hosted execution environments.

---

# 3. Formatting

## 3.1 Indentation

Use exactly **4 spaces** for each indentation level.

Do not use tabs for indentation.

Example:

```python
def process_records(records: list[str]) -> None:
    """Process the provided records.

    :param records: Records to process.
    """

    for record in records:
        process_record(record)
```

---

## 3.2 Control Flow

Do not write loops, conditional statements, exception handlers, or similar control-flow constructs on a single line.

Do not write:

```python
if enabled: start_service()
```

Write:

```python
if enabled:
    start_service()
```

Do not write:

```python
for record in records: process_record(record)
```

Write:

```python
for record in records:
    process_record(record)
```

The same rule applies even when the body contains only one statement.

Explicit formatting is preferred over saving vertical space.

---

## 3.3 Line Length

Prefer lines that remain reasonably readable in normal editors and code-review tools.

A formatter's configured line-length limit should be followed when one exists.

Do not contort otherwise readable code merely to avoid a moderately long line.

When an expression becomes difficult to read, break it into appropriately named intermediate values rather than constructing deeply nested expressions.

---

# 4. Naming

## 4.1 Descriptive Names

Variable and function names must describe their purpose.

Names should convey the role of the value rather than merely its type or position.

Prefer:

```python
current_user
source_repository
generated_project_path
request_timeout_seconds
course_identifier
```

Avoid vague names such as:

```python
data
thing
value
obj
tmp
foo
bar
x
y
```

when a more meaningful name is available.

---

## 4.2 Single-Character Variable Names

Single-character variable names are prohibited except where required by an external API or mathematical notation that would genuinely become less readable when renamed.

Do not write:

```python
for x in records:
    process_record(x)
```

Write:

```python
for record in records:
    process_record(record)
```

---

## 4.3 Abbreviations

Avoid abbreviations that require the reader to infer meaning.

Names such as the following are not acceptable:

```python
idx
ctx
cfg
mgr
req
resp
tmp
val
```

Prefer:

```python
index
context
configuration
manager
request
response
temporary_path
value
```

Common domain-standard abbreviations may be used where spelling them out would reduce clarity.

Examples may include:

* HTTP;
* URL;
* API;
* UUID;
* JSON;
* SQL;
* S3.

---

## 4.4 Function Names

Function names should describe the action they perform.

Prefer:

```python
load_project_configuration()
create_generated_repository()
retrieve_course_material()
validate_project_name()
```

Avoid names such as:

```python
handle()
process()
do_work()
run_thing()
```

unless the surrounding abstraction makes their meaning unambiguous.

---

## 4.5 Boolean Names

Boolean variables and functions should read naturally as conditions.

Prefer:

```python
is_authenticated
has_completed_course
should_retry_request
can_generate_project
```

Avoid:

```python
authentication
complete
retry
flag
```

when the value specifically represents a Boolean state.

---

# 5. Functions

## 5.1 Function Size

Prefer short, simple, focused functions.

A function should generally perform one coherent operation.

Functions should be easy to:

* understand;
* test independently;
* reuse;
* replace;
* reason about during failure.

When a function performs several unrelated operations, extract appropriately named helper functions or services.

Do not split functions mechanically merely to reduce line count. Extraction should improve comprehension or testability.

---

## 5.2 Function Inputs and Outputs

Prefer explicit parameters and return values.

Avoid hidden dependence on global mutable state.

Where practical, functions should receive the information they require through arguments.

Prefer returning meaningful values instead of modifying unrelated external state.

Side effects should be obvious from the function's name and documentation.

---

## 5.3 Type Hints

Use type annotations as extensively as reasonably possible.

All new functions should normally annotate:

* every parameter;
* return types;
* public attributes;
* important local variables where inference is ambiguous;
* collection element types;
* callback signatures;
* nullable values.

Example:

```python
from pathlib import Path


def create_project_directory(
    project_root: Path,
    project_name: str,
) -> Path:
    """Create and return a directory for a generated project.

    :param project_root: Root directory in which generated projects are stored.
    :param project_name: Name of the project to create.
    :return: Path to the newly created project directory.
    """

    project_directory: Path = project_root / project_name
    project_directory.mkdir(parents=True, exist_ok=False)

    return project_directory
```

Avoid using `Any` merely to silence a type checker.

Use `Any` when the value genuinely cannot be represented more precisely or when interacting with an untyped external interface.

Prefer modern type syntax supported by the configured Python version.

---

# 6. Documentation

## 6.1 Required Docstrings

Every module, class, and function must have a docstring.

This includes:

* public functions;
* private functions;
* helper functions;
* methods;
* constructors where meaningful;
* classes;
* modules;
* asynchronous functions.

Docstrings must use **reStructuredText-compatible formatting**.

---

## 6.2 Module Docstrings

Every Python module must begin with a module docstring describing its purpose.

Example:

```python
"""Provide services for creating and managing generated project repositories.

This module contains the application-level logic used to create project
directories, populate generated files, and initialize independent Git
repositories.
"""
```

---

## 6.3 Function Docstrings

Function and method docstrings should describe:

* what the function does;
* important behavior;
* parameters;
* return values;
* raised exceptions when they are meaningful to callers.

Example:

```python
def load_configuration(configuration_path: Path) -> dict[str, object]:
    """Load application configuration from a JSON document.

    :param configuration_path: Path to the configuration file.
    :return: Parsed configuration values.
    :raises FileNotFoundError: If the configuration file does not exist.
    :raises ValueError: If the configuration document is invalid.
    """
```

Do not write useless docstrings that merely repeat the function name.

Avoid:

```python
def load_configuration() -> None:
    """Load configuration."""
```

Provide enough context that another developer can understand why the function exists and how it behaves.

---

## 6.4 Class Docstrings

Every class must document its purpose and important behavior.

Example:

```python
class ProjectRepository:
    """Represent an independently generated project repository.

    Instances provide operations for initializing, validating, and interacting
    with a generated Git repository.
    """
```

---

# 7. Class Member Documentation

Class member variables must be documented with string literals immediately following their declaration.

This requirement applies whether the member is declared:

* at class scope;
* inside `__init__`;
* outside `__init__`;
* through later assignment when the member forms part of the object's expected state.

Example:

```python
class ProjectGenerator:
    """Generate complete project workspaces."""

    project_root: Path
    """Root directory containing generated projects."""

    template_directory: Path
    """Directory containing project-generation templates."""

    def __init__(
        self,
        project_root: Path,
        template_directory: Path,
    ) -> None:
        """Initialize the project generator.

        :param project_root: Root directory for generated projects.
        :param template_directory: Directory containing generation templates.
        """

        self.project_root: Path = project_root
        """Root directory containing generated projects."""

        self.template_directory: Path = template_directory
        """Directory containing project-generation templates."""
```

For dynamically introduced members:

```python
self.generated_repository_path: Path | None = None
"""Path to the generated repository after successful project generation."""
```

Do not rely solely on a class docstring to document member variables.

Member documentation should explain purpose, units, expected values, or lifecycle where those details are not obvious.

---

# 8. Classes and Abstractions

## 8.1 Prefer Composition

Prefer composition over inheritance unless inheritance represents a genuine substitutable relationship.

Avoid constructing deep class hierarchies solely to share small amounts of code.

Use inheritance primarily when implementations must satisfy a common behavioral contract.

---

## 8.2 Environment-Dependent Implementations

Introduce abstractions when substantially different implementations may be required depending on deployment environment or external system.

For example, data retrieval might define a common interface with implementations for:

* local filesystem storage;
* Amazon S3;
* another S3-compatible object store;
* authenticated remote APIs;
* test fixtures or in-memory data.

Conceptually:

```text
DataSource
    |
    +-- LocalDataSource
    |
    +-- S3DataSource
    |
    +-- RemoteApiDataSource
```

The rest of the application should depend on the meaningful abstraction rather than environment-specific implementation details.

Do not create interfaces merely because another implementation is theoretically possible.

Create them when different implementations are plausible, already required, or materially improve testing.

---

## 8.3 Dependency Injection

Where practical, provide external dependencies to services rather than constructing them deeply inside business logic.

Useful injectable dependencies include:

* HTTP clients;
* storage providers;
* repositories;
* clocks;
* external API clients;
* project templates;
* filesystem interfaces where isolation is necessary.

This improves testing and allows implementations to vary between environments.

---

# 9. Asynchronous Programming

Use asynchronous functionality when it provides a meaningful benefit.

Good candidates include:

* network requests;
* concurrent remote API calls;
* object-storage operations;
* waiting on independent external resources;
* other I/O-bound operations supported by asynchronous libraries.

Do not use asynchronous code merely because it exists.

Avoid converting CPU-bound synchronous work into `async` functions without an actual concurrency benefit.

Do not block an asynchronous event loop with long-running synchronous operations.

Where asynchronous HTTP access is required, prefer an established asynchronous HTTP client such as:

* `httpx`;
* `aiohttp`.

For ordinary synchronous HTTP requests, `requests` is preferred.

---

# 10. Libraries and Dependencies

## 10.1 Prefer Established Libraries

Prefer mature, widely used, actively maintained libraries over custom implementations of solved problems.

Examples include:

* `requests` for synchronous HTTP clients;
* `httpx` or `aiohttp` for asynchronous HTTP clients;
* `jinja2` for general-purpose template rendering;
* Django's established facilities when operating within Django;
* `pydantic` when robust external data validation is appropriate;
* `pytest` for testing where configured;
* `pathlib` for filesystem paths.

Do not reinvent functionality that a dependable, established library already provides.

---

## 10.2 Low-Level HTTP Libraries

Avoid directly using low-level HTTP facilities such as:

* `http.client`;
* `urllib.request`;
* custom socket-level HTTP implementations.

Use them only when an established higher-level library cannot satisfy a documented requirement.

If a lower-level library is required, document why.

---

## 10.3 Dependency Selection

Before adding a new dependency:

1. determine whether an existing dependency already provides the functionality;
2. determine whether the Python standard library provides a sufficiently clear solution;
3. consider maintenance activity and ecosystem adoption;
4. consider compatibility with supported environments;
5. avoid adding large frameworks for trivial functionality.

The goal is not to avoid dependencies at all costs.

The goal is to avoid unnecessary or obscure dependencies while taking advantage of well-established libraries.

---

# 11. Logging

## 11.1 Logging Instead of Printing

Use structured application logging extensively.

Do not use `print()` for application diagnostics, operational messages, error reporting, or debugging information that belongs in logs.

`print()` may be used where standard output is itself the documented application interface, such as:

* CLI command output;
* intentionally emitted machine-readable output;
* explicit interactive terminal behavior.

Diagnostic behavior must use logging.

---

## 11.2 Logging Configuration

Logging configuration must be separated from normal application modules.

The project should provide a dedicated logging configuration module responsible for loading logging configuration.

Logging configuration should be stored in a JSON file, normally named:

```text
logging.json
```

The configuration should be compatible with:

```python
logging.config.dictConfig(...)
```

Application modules should not duplicate logging configuration.

Conceptually:

```text
application/
├── logging_configuration.py
└── configuration/
    └── logging.json
```

The exact location may vary according to project structure.

---

## 11.3 Module Loggers

Application modules should obtain named loggers using:

```python
import logging


LOGGER: logging.Logger = logging.getLogger(__name__)
```

Logging calls should use the module logger.

Example:

```python
LOGGER.info(
    "Generating project %s in %s",
    project_name,
    project_directory,
)
```

Prefer logger argument substitution over eagerly constructing formatted strings:

```python
LOGGER.debug(
    "Loaded %d curriculum records",
    record_count,
)
```

rather than:

```python
LOGGER.debug(f"Loaded {record_count} curriculum records")
```

This avoids unnecessary formatting when the log level is disabled.

---

## 11.4 Logging Levels

Use logging levels consistently.

### `DEBUG`

Detailed diagnostic information useful during development or troubleshooting.

Examples:

* resolved paths;
* request parameters without sensitive data;
* branch decisions;
* counts;
* generated command arguments;
* detailed state transitions.

### `INFO`

Normal significant application events.

Examples:

* application startup;
* project generation started;
* project generation completed;
* remote data retrieval completed;
* repository initialized.

### `WARNING`

Unexpected conditions from which the application can reasonably continue.

### `ERROR`

Operations that failed and require attention but do not necessarily terminate the entire process.

### `CRITICAL`

Severe failures that make continued operation unsafe or impossible.

---

## 11.5 Sensitive Information

Never log:

* passwords;
* API tokens;
* authentication headers;
* private keys;
* session secrets;
* full credential objects;
* sensitive personal information.

Logging should provide enough context for diagnosis without leaking protected information.

---

# 12. Exceptions and Error Handling

Catch exceptions where the code can:

* add useful context;
* recover;
* translate an implementation-specific exception into a domain-specific exception;
* perform required cleanup.

Do not catch broad exceptions merely to suppress failures.

Avoid:

```python
try:
    perform_operation()
except Exception:
    pass
```

Do not silently ignore unexpected errors.

When re-raising with additional context, preserve the original exception chain where appropriate:

```python
raise ProjectGenerationError(
    f"Unable to initialize repository at {project_directory}"
) from error
```

Errors should generally be logged at the layer responsible for handling or presenting the failure, not redundantly at every layer through which the exception passes.

---

# 13. Filesystem Operations

Use `pathlib.Path` for filesystem paths unless an external API explicitly requires another representation.

Prefer:

```python
project_file: Path = project_directory / "SPEC.md"
```

over:

```python
project_file = project_directory + "/SPEC.md"
```

Paths received from users or generated from external values must be validated before use.

Code that generates projects must prevent path traversal outside configured project roots.

---

# 14. External Processes

Use `subprocess` with argument lists rather than shell command construction unless shell behavior is explicitly required.

Prefer:

```python
subprocess.run(
    [
        "git",
        "-C",
        str(project_directory),
        "status",
    ],
    check=True,
)
```

Avoid:

```python
os.system(f"git -C {project_directory} status")
```

Do not construct shell commands from untrusted values.

Capture and log useful process output when failures need to be diagnosed.

---

# 15. Testing

Code should be designed for practical automated testing.

Prefer functions and services that:

* have explicit dependencies;
* have deterministic behavior where practical;
* do not depend unnecessarily on global state;
* return useful results;
* isolate external I/O behind reasonable boundaries.

Tests should verify externally meaningful behavior rather than internal implementation details when practical.

Complex logic should not exist solely inside:

* Django views;
* management commands;
* CLI entry points;
* framework hooks.

Move such logic into independently testable functions or services.

---

# 16. Comments

Comments should explain **why**, not narrate obvious code.

Useful comment:

```python
# S3-compatible providers may return directory markers as zero-length objects,
# so they must be ignored before creating curriculum resources.
```

Unhelpful comment:

```python
# Increment count.
count += 1
```

Prefer expressive code over comments when better naming can make intent obvious.

---

# 17. Imports

Prefer clear, explicit imports.

Avoid wildcard imports:

```python
from module import *
```

Group imports according to the project's formatter/linter conventions, normally:

1. Python standard library;
2. third-party dependencies;
3. local application imports.

Do not manipulate `sys.path` as a substitute for correct package structure.

---

# 18. Constants

Use descriptive named constants for values with domain or configuration meaning.

Prefer:

```python
DEFAULT_REQUEST_TIMEOUT_SECONDS: float = 30.0
```

over repeatedly embedding:

```python
30
```

throughout application code.

Do not create constants for values whose meaning is already obvious and purely local.

---

# 19. Configuration

Environment-specific values should normally come from configuration rather than being hard-coded into business logic.

Examples include:

* external service URLs;
* project-generation roots;
* timeouts;
* credentials;
* logging configuration paths;
* storage providers;
* feature flags.

Provide safe and reasonable defaults where appropriate.

Secrets must not be committed to source control.

---

# 20. Preferred Design Characteristics

When several reasonable implementations are available, prefer the one that is:

1. easiest to understand;
2. easiest to test;
3. explicit about dependencies;
4. strongly typed;
5. easy to replace when environment-specific behavior changes;
6. based on established libraries;
7. observable through useful logging;
8. minimally coupled to unrelated application components.

The shortest implementation is not necessarily the simplest implementation.

Likewise, the most abstract implementation is not necessarily the most reusable one.

Use enough structure to make behavior clear and replaceable without constructing infrastructure for hypothetical problems.
