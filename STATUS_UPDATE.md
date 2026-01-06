# Ticket Status Mapping Update

## Issue

The `TicketStatus` enum and `_map_status_name()` helper function were missing two valid ticket statuses:
- **In Progress** (status ID: 6)
- **Pending Return** (status ID: 7)

This caused analytics functions to display these statuses as `"Status-6"` and `"Status-7"` instead of human-readable names.

## Solution

Updated both the enum definition and the mapping function to include all ticket statuses.

### 1. Updated `TicketStatus` Enum

**Location:** [src/freshservice_mcp/server.py](src/freshservice_mcp/server.py) lines 57-63

```python
class TicketStatus(IntEnum):
    OPEN = 2
    PENDING = 3
    RESOLVED = 4
    CLOSED = 5
    IN_PROGRESS = 6          # ✅ Added
    PENDING_RETURN = 7        # ✅ Added
```

### 2. Updated `_map_status_name()` Function

**Location:** [src/freshservice_mcp/server.py](src/freshservice_mcp/server.py) lines 4172-4189

```python
def _map_status_name(status_id: int) -> str:
    """Map ticket status ID to human-readable name."""
    mapping = {
        2: "Open",
        3: "Pending",
        4: "Resolved",
        5: "Closed",
        6: "In Progress",      # ✅ Added
        7: "Pending Return"    # ✅ Added
    }
    return mapping.get(status_id, f"Status-{status_id}")
```

## Complete Ticket Status Reference

| Status ID | Status Name | Enum Constant |
|-----------|-------------|---------------|
| 2 | Open | `TicketStatus.OPEN` |
| 3 | Pending | `TicketStatus.PENDING` |
| 4 | Resolved | `TicketStatus.RESOLVED` |
| 5 | Closed | `TicketStatus.CLOSED` |
| 6 | In Progress | `TicketStatus.IN_PROGRESS` |
| 7 | Pending Return | `TicketStatus.PENDING_RETURN` |

## Impact on Analytics Functions

This update affects all analytics functions that display status information:

### `get_ticket_stats()`
**Before:**
```json
{
  "by_status": {
    "Open": 10,
    "Pending": 5,
    "Status-6": 8,
    "Status-7": 3
  }
}
```

**After:**
```json
{
  "by_status": {
    "Open": 10,
    "Pending": 5,
    "In Progress": 8,
    "Pending Return": 3
  }
}
```

### `get_agent_workload()`
Now correctly counts tickets in "In Progress" and "Pending Return" states with human-readable names.

### `get_team_comparison()`
Team statistics now include proper status names for all ticket states.

## Backward Compatibility

✅ **Fully backward compatible** - No breaking changes
✅ **Existing code works unchanged** - Functions still accept numeric status IDs
✅ **Improved output** - Better human-readable status names

## Testing

To verify the update works correctly:

```python
# Test with tickets in all statuses
result = await get_ticket_stats(
    created_after="2024-01-01"
)

print(result['stats']['by_status'])
# Should now show: "Open", "Pending", "Resolved", "Closed", "In Progress", "Pending Return"
```

## Files Modified

1. [src/freshservice_mcp/server.py](src/freshservice_mcp/server.py)
   - Lines 57-63: `TicketStatus` enum
   - Lines 4181-4188: `_map_status_name()` function mapping

---

**Update applied:** 2026-01-05
**Statuses added:** In Progress (6), Pending Return (7)
