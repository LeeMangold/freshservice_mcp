# Implementation Plan: Analytics Functions for Freshservice MCP Server

## Overview
Add 5 new analytics functions to the Freshservice MCP server to provide aggregated ticket statistics, agent workload metrics, team comparisons, and enhanced search capabilities.

## Prerequisites & Dependencies

### New Imports Required
```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Optional
```

### Caching Strategy
- Implement a simple in-memory cache with TTL for agent/group lookups
- Cache duration: 300 seconds (5 minutes) - balances freshness with API efficiency
- Use module-level dictionary: `_cache = {"agents": None, "groups": None, "timestamp": None}`

## Existing Patterns to Follow

### Pagination Pattern (from `filter_agents`)
```python
page = 1
all_results = []
while True:
    response = await client.get(url, params={"page": page, "per_page": 30})
    data = response.json()
    all_results.extend(data.get("items", []))

    link_header = response.headers.get("Link", "")
    pagination_info = parse_link_header(link_header)
    if not pagination_info.get("next"):
        break
    page = pagination_info["next"]
```

### Error Handling Pattern (from `get_all_agents`)
```python
try:
    response = await client.get(url, headers=headers, params=params)
    response.raise_for_status()
    return {"success": True, "data": ...}
except httpx.HTTPStatusError as e:
    error_text = e.response.json() if e.response else e.response.text
    return {
        "error": f"Failed to ...: {str(e)}",
        "status_code": e.response.status_code if e.response else None,
        "details": error_text
    }
except Exception as e:
    return {"error": f"Unexpected error: {str(e)}"}
```

### Query Wrapping (from `filter_tickets`)
```python
# Freshservice API requires queries wrapped in double quotes
encoded_query = urllib.parse.quote(f'"{query}"')
```

## Function Implementations

### 1. `get_agent_lookup()` - Agent/Group Name Cache

**Location:** Add after `get_auth_headers()` (around line 3260)

**Purpose:** Provide cached mapping of IDs to names to avoid repeated API calls

**Signature:**
```python
@mcp.tool()
async def get_agent_lookup() -> Dict[str, Any]:
    """Returns cached dictionaries mapping agent IDs to names and group IDs to names.

    Returns:
        {
            "agents": {agent_id: {"name": "Full Name", "email": "email@domain.com"}},
            "groups": {group_id: "Group Name"},
            "cached_at": "ISO timestamp",
            "ttl_seconds": 300
        }
    """
```

**Implementation Details:**
- Check module-level cache first (`_cache`)
- If cache is older than 300 seconds or empty, refresh:
  - Fetch all agents using pagination (call `/api/v2/agents`)
  - Fetch all agent groups using pagination (call `/api/v2/groups`)
  - Store in `_cache` with current timestamp
- Return cached data

**API Endpoints:**
- GET `/api/v2/agents` (paginated)
- GET `/api/v2/groups` (paginated)

**Estimated Lines:** ~80 lines

---

### 2. `search_tickets_all()` - Paginated Ticket Search

**Location:** Add after `filter_tickets` (around line 386)

**Purpose:** Wrapper around `filter_tickets` that auto-paginates and returns all results

**Signature:**
```python
@mcp.tool()
async def search_tickets_all(
    query: str,
    max_results: int = 500,
    fields: Optional[List[str]] = None,
    workspace_id: Optional[int] = None
) -> Dict[str, Any]:
    """Search tickets with automatic pagination returning all results up to max_results.

    Args:
        query: Filter query (e.g., "status:2 AND priority:3")
        max_results: Maximum tickets to return (default: 500, max: 1000)
        fields: Optional list of field names to include in response
        workspace_id: Optional workspace filter

    Returns:
        {
            "success": True,
            "tickets": [...],
            "total_fetched": int,
            "pages_fetched": int,
            "truncated": bool  # True if max_results was hit
        }
    """
```

**Implementation Details:**
- Use existing `filter_tickets` API pattern
- Auto-paginate through results (30 per page)
- Stop when: (a) no more pages OR (b) max_results reached
- Optionally filter returned fields if `fields` parameter provided
- Cap max_results at 1000 to prevent abuse

**API Endpoints:**
- GET `/api/v2/tickets/filter?query={query}&page={page}`

**Estimated Lines:** ~70 lines

---

### 3. `get_ticket_stats()` - Aggregated Ticket Statistics

**Location:** Add after `search_tickets_all` (around line 456)

**Purpose:** Return aggregated statistics for tickets matching filters

**Signature:**
```python
@mcp.tool()
async def get_ticket_stats(
    group_id: Optional[int] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None,
    workspace_id: Optional[int] = None
) -> Dict[str, Any]:
    """Get aggregated ticket statistics with automatic pagination.

    Args:
        group_id: Filter by agent group ID
        created_after: ISO date string (e.g., "2024-01-01")
        created_before: ISO date string (e.g., "2024-12-31")
        workspace_id: Filter by workspace

    Returns:
        {
            "success": True,
            "stats": {
                "total_tickets": int,
                "by_status": {"Open": 10, "Pending": 5, ...},
                "by_priority": {"Low": 20, "Medium": 15, ...},
                "by_agent": {"Agent Name": 5, ...},
                "by_type": {"Incident": 30, "Service Request": 10}
            },
            "filters": {
                "group_id": ...,
                "created_after": ...,
                "created_before": ...,
                "workspace_id": ...
            },
            "date_range": {"start": "...", "end": "..."}
        }
    """
```

**Implementation Details:**
- Build query string from parameters:
  - `group_id` → `group_id:{value}`
  - `created_after` → `created_at:>'{date}'`
  - `created_before` → `created_at:<'{date}'`
  - Combine with `AND`
- Fetch ALL tickets using pagination (reuse pattern from `filter_agents`)
- Aggregate in memory using `defaultdict(int)`:
  - Count by status (map IDs to names: 2→"Open", 3→"Pending", etc.)
  - Count by priority (map IDs to names: 1→"Low", 2→"Medium", etc.)
  - Count by agent (use `get_agent_lookup()` for names)
  - Count by type
- Return aggregated stats with human-readable names

**API Endpoints:**
- GET `/api/v2/tickets/filter?query={query}&page={page}`

**Data Mapping:**
- Status: Use existing `TicketStatus` enum (OPEN=2, PENDING=3, RESOLVED=4, CLOSED=5)
- Priority: Use existing `TicketPriority` enum (LOW=1, MEDIUM=2, HIGH=3, URGENT=4)

**Estimated Lines:** ~150 lines

---

### 4. `get_agent_workload()` - Per-Agent Metrics

**Location:** Add after `get_ticket_stats` (around line 606)

**Purpose:** Calculate workload metrics for specific agent(s)

**Signature:**
```python
@mcp.tool()
async def get_agent_workload(
    agent_id: Optional[int] = None,
    group_id: Optional[int] = None,
    period: Optional[str] = "30d",
    created_after: Optional[str] = None,
    created_before: Optional[str] = None
) -> Dict[str, Any]:
    """Get workload metrics for agent(s) with automatic pagination.

    Args:
        agent_id: Specific agent ID (if None, returns all agents in group)
        group_id: Agent group ID (required if agent_id is None)
        period: Time period shorthand ("7d", "30d", "90d") - used if created_after not provided
        created_after: ISO date string (overrides period)
        created_before: ISO date string (defaults to now)

    Returns:
        {
            "success": True,
            "agents": [
                {
                    "agent_id": int,
                    "agent_name": "Full Name",
                    "email": "...",
                    "tickets_assigned": int,
                    "tickets_resolved": int,
                    "tickets_closed": int,
                    "tickets_open": int,
                    "avg_resolution_hours": float,
                    "resolution_times": [hours, ...]  # For resolved tickets
                },
                ...
            ],
            "date_range": {"start": "...", "end": "..."},
            "group_name": "..." if group_id else None
        }
    """
```

**Implementation Details:**
- Validate: Either `agent_id` OR `group_id` must be provided
- Parse `period` (e.g., "30d" → 30 days before today) if `created_after` not provided
- Build query:
  - If `agent_id`: `agent_id:{value} AND created_at:>'{date}'`
  - If `group_id`: `group_id:{value} AND created_at:>'{date}'`
- Fetch all matching tickets using pagination
- Group tickets by `responder_id`
- For each agent:
  - Count total assigned
  - Count resolved (status=4)
  - Count closed (status=5)
  - Count open (status=2)
  - Calculate avg resolution time (resolved_at - created_at) for resolved tickets
- Use `get_agent_lookup()` to map IDs to names

**API Endpoints:**
- GET `/api/v2/tickets/filter?query={query}&page={page}`

**Date Calculations:**
```python
if created_after is None:
    days = int(period.rstrip('d'))
    created_after = (datetime.now() - timedelta(days=days)).isoformat()
if created_before is None:
    created_before = datetime.now().isoformat()
```

**Estimated Lines:** ~180 lines

---

### 5. `get_team_comparison()` - Multi-Team Comparison

**Location:** Add after `get_agent_workload` (around line 786)

**Purpose:** Compare multiple teams side-by-side

**Signature:**
```python
@mcp.tool()
async def get_team_comparison(
    group_ids: List[int],
    created_after: Optional[str] = None,
    created_before: Optional[str] = None
) -> Dict[str, Any]:
    """Compare multiple agent groups side by side with aggregated metrics.

    Args:
        group_ids: List of agent group IDs to compare (2-10 groups)
        created_after: ISO date string (defaults to 30 days ago)
        created_before: ISO date string (defaults to now)

    Returns:
        {
            "success": True,
            "comparison": [
                {
                    "group_id": int,
                    "group_name": "Team Name",
                    "total_tickets": int,
                    "open_tickets": int,
                    "resolved_tickets": int,
                    "closed_tickets": int,
                    "closure_rate": float,  # (resolved + closed) / total
                    "avg_resolution_hours": float,
                    "top_agents": [
                        {"agent_name": "...", "ticket_count": int},
                        ...
                    ]  # Top 5 agents by ticket count
                },
                ...
            ],
            "date_range": {"start": "...", "end": "..."},
            "summary": {
                "total_tickets_all_groups": int,
                "average_closure_rate": float
            }
        }
    """
```

**Implementation Details:**
- Validate: 2 ≤ len(group_ids) ≤ 10
- Default date range: 30 days if not provided
- For each group_id:
  - Build query: `group_id:{id} AND created_at:>'{start}' AND created_at:<'{end}'`
  - Fetch all tickets (paginate)
  - Aggregate:
    - Total count
    - Count by status (open, resolved, closed)
    - Calculate closure rate: (resolved + closed) / total
    - Calculate avg resolution time
    - Get top 5 agents by ticket count
- Use `get_agent_lookup()` for group and agent names
- Return side-by-side comparison

**API Endpoints:**
- GET `/api/v2/tickets/filter?query={query}&page={page}`

**Estimated Lines:** ~200 lines

---

## Module-Level Changes

### Cache Dictionary (add near top of file, after imports)
```python
# Cache for agent/group lookups (TTL: 5 minutes)
_lookup_cache: Dict[str, Any] = {
    "agents": None,
    "groups": None,
    "timestamp": None
}
```

### New Helper Functions

#### `_parse_period(period: str) -> datetime`
Convert period shorthand to datetime
```python
def _parse_period(period: str) -> datetime:
    """Parse period like '30d' to datetime."""
    if period.endswith('d'):
        days = int(period[:-1])
        return datetime.now() - timedelta(days=days)
    raise ValueError(f"Invalid period format: {period}")
```

#### `_map_status_name(status_id: int) -> str`
Map status ID to human-readable name
```python
def _map_status_name(status_id: int) -> str:
    """Map ticket status ID to human-readable name."""
    mapping = {2: "Open", 3: "Pending", 4: "Resolved", 5: "Closed"}
    return mapping.get(status_id, f"Status-{status_id}")
```

#### `_map_priority_name(priority_id: int) -> str`
Map priority ID to human-readable name
```python
def _map_priority_name(priority_id: int) -> str:
    """Map ticket priority ID to human-readable name."""
    mapping = {1: "Low", 2: "Medium", 3: "High", 4: "Urgent"}
    return mapping.get(priority_id, f"Priority-{priority_id}")
```

#### `_calculate_resolution_time(created_at: str, resolved_at: str) -> float`
Calculate hours between creation and resolution
```python
def _calculate_resolution_time(created_at: str, resolved_at: str) -> Optional[float]:
    """Calculate resolution time in hours."""
    try:
        created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        resolved = datetime.fromisoformat(resolved_at.replace('Z', '+00:00'))
        delta = resolved - created
        return delta.total_seconds() / 3600  # Convert to hours
    except (ValueError, AttributeError):
        return None
```

**Estimated Lines for Helpers:** ~60 lines

---

## Testing Strategy

### Test File Updates
Add tests to [tests/test-fs-mcp.py](tests/test-fs-mcp.py):

```python
async def test_get_agent_lookup():
    result = await get_agent_lookup()
    print(result)

async def test_search_tickets_all():
    result = await search_tickets_all(
        query="status:2",
        max_results=100
    )
    print(f"Found {result['total_fetched']} tickets")

async def test_get_ticket_stats():
    result = await get_ticket_stats(
        group_id=18000169214,  # Security Team
        created_after="2024-01-01"
    )
    print(result)

async def test_get_agent_workload():
    result = await get_agent_workload(
        agent_id=18000806759,  # Lee Mangold
        period="30d"
    )
    print(result)

async def test_get_team_comparison():
    result = await get_team_comparison(
        group_ids=[18000169214, 18000169215],  # Multiple teams
        created_after="2024-01-01"
    )
    print(result)
```

---

## Implementation Order

1. **Phase 1: Foundation** (30 min)
   - Add new imports (`datetime`, `defaultdict`)
   - Add module-level cache dictionary
   - Add helper functions (`_map_status_name`, `_map_priority_name`, `_calculate_resolution_time`, `_parse_period`)

2. **Phase 2: Cache Layer** (45 min)
   - Implement `get_agent_lookup()` with caching logic
   - Test cache functionality

3. **Phase 3: Basic Search** (30 min)
   - Implement `search_tickets_all()`
   - Test pagination and max_results limit

4. **Phase 4: Statistics** (60 min)
   - Implement `get_ticket_stats()`
   - Test aggregation logic with various filters

5. **Phase 5: Agent Metrics** (60 min)
   - Implement `get_agent_workload()`
   - Test period parsing and resolution time calculations

6. **Phase 6: Team Comparison** (60 min)
   - Implement `get_team_comparison()`
   - Test multi-group comparison logic

7. **Phase 7: Testing & Documentation** (45 min)
   - Add all test functions
   - Update CLAUDE.md with new functions
   - Update README.md if needed

**Total Estimated Time:** 5.5 hours

---

## Code Size Estimates

| Component | Lines of Code |
|-----------|--------------|
| Helper functions | ~60 |
| get_agent_lookup | ~80 |
| search_tickets_all | ~70 |
| get_ticket_stats | ~150 |
| get_agent_workload | ~180 |
| get_team_comparison | ~200 |
| Tests | ~80 |
| **Total** | **~820 lines** |

---

## API Rate Limiting Considerations

- Freshservice typically limits to ~500 requests/hour
- Each analytics function may make multiple paginated requests
- The `get_agent_lookup()` cache reduces repeated agent/group API calls
- For large datasets, pagination could trigger rate limits
- Consider adding optional `rate_limit_delay` parameter if needed

---

## Error Handling Requirements

All functions must handle:
1. Invalid date formats → return error with example format
2. Invalid group_ids/agent_ids → return error with details from API
3. Pagination failures → return partial results with error indicator
4. Empty result sets → return success with empty stats/zero counts
5. Cache refresh failures → return stale cache with warning if available

---

## Documentation Updates Needed

### CLAUDE.md
Add new section after "Module Categories":

```markdown
### Analytics & Reporting Tools

The server includes advanced analytics functions that handle pagination automatically and return human-readable results:

- **get_agent_lookup()**: Cached mapping of agent/group IDs to names (5-minute TTL)
- **search_tickets_all()**: Paginated ticket search returning all results up to max_results
- **get_ticket_stats()**: Aggregated statistics (counts by status, priority, agent, type)
- **get_agent_workload()**: Per-agent metrics including resolution times and ticket counts
- **get_team_comparison()**: Side-by-side comparison of multiple agent groups

All analytics functions:
- Handle Freshservice API pagination automatically (30/page limit)
- Return human-readable names instead of IDs
- Support date range filtering with ISO dates or period shorthand ("7d", "30d", "90d")
- Include comprehensive error handling
```

### README.md
Add new table under "Components & Tools":

```markdown
### Analytics & Reporting

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_agent_lookup` | Cached agent/group name mappings | None (auto-refreshes every 5 min) |
| `search_tickets_all` | Auto-paginated ticket search | `query`, `max_results`, `fields`, `workspace_id` |
| `get_ticket_stats` | Aggregated ticket statistics | `group_id`, `created_after`, `created_before`, `workspace_id` |
| `get_agent_workload` | Agent workload metrics | `agent_id`, `group_id`, `period`, `created_after`, `created_before` |
| `get_team_comparison` | Compare multiple teams | `group_ids`, `created_after`, `created_before` |
```

---

## Success Criteria

- [ ] All 5 functions implemented and tested
- [ ] Pagination works correctly (tested with >100 tickets)
- [ ] Agent/group name cache working with 5-minute TTL
- [ ] Date filtering works with both ISO dates and period shorthand
- [ ] Human-readable output (no raw IDs in user-facing fields)
- [ ] Comprehensive error handling for all edge cases
- [ ] Tests added to test-fs-mcp.py
- [ ] Documentation updated (CLAUDE.md and README.md)
- [ ] All functions follow existing code patterns and style

---

## Future Enhancements (Not in Scope)

- Export to CSV/JSON file
- Graphical charts/visualizations
- Scheduled reports
- Webhook notifications
- Custom metric definitions
- Historical trend analysis
