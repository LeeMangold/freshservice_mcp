# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server for Freshservice, enabling AI models to interact with Freshservice's IT Service Management platform. The server exposes Freshservice API operations as MCP tools that can be called by Claude or other AI assistants.

## Development Commands

### Setup
```bash
# Install uv if not already installed
pip install uv

# Install dependencies
uv sync

# Activate virtual environment (if needed)
source .venv/bin/activate
```

### Running the Server
```bash
# Run the server manually (requires API credentials)
uvx freshservice-mcp --env FRESHSERVICE_APIKEY=<your_key> --env FRESHSERVICE_DOMAIN=<your_domain>

# Or run via Python module
python -m freshservice_mcp.server
```

### Testing
```bash
# Run a specific test function (tests use asyncio)
python tests/test-fs-mcp.py

# The test file contains individual async test functions that can be enabled by uncommenting them
# at the bottom of the file in the __main__ block
```

## Architecture

### Core Components

**[src/freshservice_mcp/server.py](src/freshservice_mcp/server.py)** - Single monolithic file containing all MCP tool implementations (~97 functions, ~3000+ lines)

The architecture is straightforward:
- All tool implementations are defined as `@mcp.tool()` decorated async functions
- Each tool makes HTTP requests to Freshservice API endpoints using `httpx.AsyncClient`
- Authentication uses HTTP Basic Auth with API key (encoded in `get_auth_headers()`)
- All tools are registered with the FastMCP instance (`mcp = FastMCP("freshservice_mcp")`)
- Server entry point is `main()` which calls `mcp.run(transport='stdio')`

### Key Architectural Patterns

1. **Enum-based Constants**: Status codes, priorities, and other Freshservice constants are defined as IntEnum/Enum classes at the top of server.py (TicketSource, TicketStatus, TicketPriority, ChangeStatus, etc.)

2. **Authentication**: Single `get_auth_headers()` helper function creates Basic Auth headers with base64-encoded API key

3. **Error Handling**: Most tools follow this pattern:
   ```python
   try:
       response = await client.get/post/put/delete(url, headers=headers, ...)
       response.raise_for_status()
       return response.json()
   except httpx.HTTPStatusError as e:
       return {"error": f"...", "status_code": ..., "details": ...}
   except Exception as e:
       return {"error": f"Unexpected error: {str(e)}"}
   ```

4. **Pagination**: Some tools (get_tickets, get_changes, filter operations) include pagination support using Link headers. The `parse_link_header()` helper extracts next/prev page numbers from Link headers.

5. **Query Wrapping**: Filter functions (filter_tickets, filter_agents, filter_changes) automatically wrap queries in double quotes as required by the Freshservice API. Users should pass queries without outer quotes (e.g., `"status:3"` not `"\"status:3\""`).

### Module Categories

The server implements tools across these Freshservice domains:
- **Tickets**: create, update, delete, get, filter, ticket notes, replies, conversations
- **Changes**: create, update, close, delete, get, filter, change tasks, change notes
- **Service Requests**: list service items, create service requests, get requested items
- **Products**: CRUD operations for asset products
- **Requesters**: CRUD operations, filtering, requester groups, group membership
- **Agents**: CRUD operations, filtering, agent groups
- **Workspaces**: list and get workspace details
- **Canned Responses**: list responses and folders
- **Solution Articles**: CRUD operations for categories, folders, and articles; publish articles

## Critical Implementation Details

### Query Syntax Requirements

**IMPORTANT**: When working with filter functions (filter_tickets, filter_changes, filter_agents), these functions automatically wrap the query in double quotes. Users should provide queries WITHOUT outer quotes:

✅ Correct: `filter_tickets(query="status:3")`
❌ Wrong: `filter_tickets(query="\"status:3\"")`

The functions handle URL encoding and quote wrapping internally. See [README.md](README.md#-important-query-syntax-for-filtering) for query examples.

### Environment Variables

Required environment variables (loaded via python-dotenv):
- `FRESHSERVICE_DOMAIN`: Your Freshservice domain (e.g., `yourcompany.freshservice.com`)
- `FRESHSERVICE_APIKEY`: Your Freshservice API key

These are validated at module load time and used by `get_auth_headers()`.

### MCP Tool Registration

All public API functions use the `@mcp.tool()` decorator from FastMCP. The decorator:
- Automatically generates tool schemas from function signatures and docstrings
- Handles async execution
- Makes the function available to MCP clients

### Testing Strategy

The [tests/test-fs-mcp.py](tests/test-fs-mcp.py) file contains integration tests that make real API calls. To run specific tests:

1. Uncomment the desired test in the `__main__` block at the bottom
2. Update test data (IDs, emails, etc.) to match your Freshservice instance
3. Run `python tests/test-fs-mcp.py`

Tests are not automated via pytest - they're manual integration tests.

## Common Patterns When Adding New Tools

1. Add the `@mcp.tool()` decorator
2. Make the function async
3. Accept typed parameters with Optional[] where appropriate
4. Build the API URL using f-strings with FRESHSERVICE_DOMAIN
5. Use `get_auth_headers()` for authentication
6. Use `async with httpx.AsyncClient() as client:` context manager
7. Call `response.raise_for_status()` to trigger errors
8. Return `response.json()` for successful responses
9. Catch `httpx.HTTPStatusError` and `Exception` separately
10. Return error dictionaries with `"error"`, `"status_code"`, and `"details"` keys

## Code Style Notes

- Uses Python 3.13 (see [.python-version](.python-version))
- Type hints are used extensively (typing module)
- Pydantic BaseModel for complex input schemas
- Logging is configured but minimally used (only in main())
- No external configuration files beyond pyproject.toml and .env
