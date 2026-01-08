# Freshservice MCP Server

[![smithery badge](https://smithery.ai/badge/@effytech/freshservice_mcp)](https://smithery.ai/server/@effytech/freshservice_mcp)

## Overview

A powerful MCP (Model Context Protocol) server implementation that seamlessly integrates with Freshservice, enabling AI models to interact with Freshservice modules and perform various IT service management operations. This integration bridge empowers your AI assistants to manage and resolve IT service tickets, streamlining your support workflow.

## Key Features

- **Enterprise-Grade Freshservice Integration**: Direct, secure communication with Freshservice API endpoints
- **AI Model Compatibility**: Enables Claude and other AI models to execute service desk operations through Freshservice
- **Automated ITSM Management**: Efficiently handle ticket creation, updates, responses, and asset management
- **Advanced Analytics & Reporting**: Comprehensive ticket statistics, agent workload analysis, and team performance comparisons with automatic pagination and human-readable output
- **Workflow Acceleration**: Reduce manual intervention in routine IT service tasks

## Supported Freshservice Modules

**This MCP server currently supports operations across a wide range of Freshservice modules**:

-  Tickets
-  Changes
-  Conversations
-  Products
-  Requesters
-  Agents
-  Agent Groups
-  Requester Groups
-  Canned Responses
-  Canned Response Folders
-  Workspaces
-  Solution Categories
-  Solution Folders
-  Solution Articles
-  **Analytics & Reporting**

## Components & Tools

The server provides a comprehensive toolkit for Freshservice operations:

### Ticket Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `create_ticket` | Create new service tickets | `subject`, `description`, `source`, `priority`, `status`, `email`, `group_id`, `responder_id` |
| `update_ticket` | Update existing tickets | `ticket_id`, `updates` |
| `delete_ticket` | Remove tickets | `ticket_id` |
| `filter_tickets` | Find tickets matching criteria | `query` |
| `get_ticket_fields` | Retrieve ticket field definitions | None |
| `get_tickets` | List all tickets with pagination | `page`, `per_page` |
| `get_ticket_by_id` | Retrieve single ticket details | `ticket_id` |

### Change Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_changes` | List all changes with pagination | `page`, `per_page`, `query` |
| `filter_changes` | Filter changes with advanced queries | `query`, `page`, `per_page` |
| `get_change_by_id` | Retrieve single change details | `change_id` |
| `create_change` | Create new change request | `requester_id`, `subject`, `description`, `priority`, `impact`, `status`, `risk`, `change_type` |
| `update_change` | Update existing change | `change_id`, `change_fields` |
| `close_change` | Close change with result explanation | `change_id`, `change_result_explanation` |
| `delete_change` | Remove change | `change_id` |
| `get_change_tasks` | Get tasks for a change | `change_id` |
| `create_change_note` | Add note to change | `change_id`, `body` |

### Analytics & Reporting

The server includes powerful analytics functions for ticket statistics, agent workload analysis, and team performance comparison. All analytics functions feature **automatic pagination** (handles Freshservice's 30-result-per-page limit internally) and **human-readable output** (agent/group IDs automatically resolved to names via cached lookups).

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `get_agent_lookup` | Retrieve cached agent/group name mappings (5-min TTL) | None (auto-refreshes) |
| `search_tickets_all` | Auto-paginated ticket search returning all matching results | `query`, `max_results`, `fields`, `workspace_id` |
| `get_ticket_stats` | Aggregated statistics by status, priority, agent, and type | `group_id`, `created_after`, `created_before`, `workspace_id` |
| `get_agent_workload` | Per-agent workload metrics with resolution time analysis | `agent_id`, `group_id`, `period`, `created_after`, `created_before` |
| `get_team_comparison` | Side-by-side comparison of multiple teams with closure rates | `group_ids`, `created_after`, `created_before` |

**Analytics Features:**
- ✅ **Automatic Pagination** - All functions retrieve complete datasets (not limited to 30 results)
- ✅ **Smart Caching** - Agent/group lookups cached for 5 minutes to reduce API calls
- ✅ **Human-Readable Output** - All IDs automatically resolved to names
- ✅ **Date Flexibility** - Supports ISO dates (`"2024-01-01"`) AND period shorthand (`"30d"`, `"7d"`, `"90d"`)
- ✅ **Complete Status Mappings** - Supports all 7 ticket statuses: Open (2), Pending (3), Resolved (4), Closed (5), In Progress (6), Pending Return (7)

#### 🚨 Important: Query Syntax for Filtering

When using `filter_tickets`, `filter_changes`, `search_tickets_all`, or any filtering function with the `query` parameter, **the query string must be wrapped in double quotes** for the Freshservice API to work correctly:

✅ **CORRECT**: `"status:3"`, `"approval_status:1 AND status:<6"`, `"status:2 AND priority:3"`
❌ **WRONG**: `status:3` (will cause 500 Internal Server Error)

**Common Query Examples:**

*Changes:*
- `"status:3"` - Changes awaiting approval
- `"approval_status:1"` - Approved changes
- `"approval_status:1 AND status:<6"` - Approved changes that are not closed
- `"planned_start_date:>'2025-07-14'"` - Changes starting after specific date
- `"status:3 AND priority:1"` - High priority changes awaiting approval

*Tickets:*
- `"status:2"` - Open tickets
- `"status:6"` - Tickets in progress
- `"priority:4 AND status:2"` - Urgent open tickets
- `"group_id:18000169214"` - Tickets assigned to specific team

## Getting Started

### Installing via Smithery

To install freshservice_mcp automatically via Smithery:

```bash
npx -y @smithery/cli install @effytech/freshservice_mcp --client claude
```

### Prerequisites

- A Freshservice account (sign up at [freshservice.com](https://www.freshservice.com))
- Freshservice API key
- `uvx` installed (`pip install uv` or `brew install uv`)

### Configuration

1. Generate your Freshservice API key from the admin panel:
   - Navigate to Profile Settings → API Settings
   - Copy your API key for configuration

2. Set up your domain and authentication details as shown below

### Usage with Claude Desktop

1. Install Claude Desktop from the [official website](https://claude.ai/desktop)
2. Add the following configuration to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "freshservice-mcp": {
    "command": "uvx",
    "args": [
        "freshservice-mcp"
    ],
    "env": {
      "FRESHSERVICE_APIKEY": "<YOUR_FRESHSERVICE_APIKEY>",
      "FRESHSERVICE_DOMAIN": "<YOUR_FRESHSERVICE_DOMAIN>"
    }
  }
}
```
**Important**: Replace `<YOUR_FRESHSERVICE_APIKEY>` with your actual API key and `<YOUR_FRESHSERVICE_DOMAIN>` with your domain (e.g., `yourcompany.freshservice.com`)

## Example Operations

Once configured, you can ask Claude to perform operations like:

**Tickets:**
- "Create a new incident ticket with subject 'Network connectivity issue in Marketing department' and description 'Users unable to connect to Wi-Fi in Marketing area', set priority to high and assign to Security Team"
- "List all critical incidents reported in the last 24 hours"
- "Update ticket #12345 status to resolved"

**Changes:**
- "Create a change request for scheduled server maintenance next Tuesday at 2 AM"
- "Update the status of change request #45678 to 'Approved'"
- "Close change #5092 with result explanation 'Successfully deployed to production. All tests passed.'"
- "List all pending changes"

**Analytics & Reporting:**
- "Show me ticket statistics for the Security Team for the last 30 days"
- "What's the workload for agent Lee Mangold over the past 7 days?"
- "Compare the Security Team and IT Support Team performance for January 2024"
- "Search for all high-priority open tickets and return complete results"
- "Show me resolution time metrics for all agents in group 18000169214"

**Other Operations:**
- "Show asset details for laptop with asset tag 'LT-2023-087'"
- "Create a solution article about password reset procedures"

## Analytics Functions - Detailed Examples

The analytics functions provide comprehensive reporting capabilities with automatic pagination and human-readable output:

### 1. Get Agent/Group Lookup
```
"Get the agent and group lookup cache"
```
Returns all agent names, emails, and group names with 5-minute caching to improve performance.

### 2. Search All Tickets (Auto-Paginated)
```
"Search for all open tickets with high priority using search_tickets_all"
```
Automatically retrieves ALL matching tickets (not limited to 30 results), supports up to 1000 results with `max_results` parameter.

### 3. Get Ticket Statistics
```
"Get ticket statistics for group ID 18000169214 created after 2024-01-01"
```
Returns aggregated counts by:
- **Status**: Open, In Progress, Pending, Pending Return, Resolved, Closed
- **Priority**: Low, Medium, High, Urgent
- **Agent**: Ticket counts per agent (with names)
- **Type**: Incident, Service Request, etc.

### 4. Get Agent Workload
```
"Show workload for agent 18000806759 for the last 30 days"
OR
"Show workload for all agents in group 18000169214 for the period '7d'"
```
Returns per-agent metrics:
- Tickets assigned (total count)
- Tickets resolved (count)
- Average resolution time (hours)
- Sorted by ticket count (descending)

Supports flexible date parameters:
- Period shorthand: `"7d"`, `"30d"`, `"90d"`
- ISO dates: `"2024-01-01"` to `"2024-01-31"`

### 5. Compare Multiple Teams
```
"Compare teams 18000169214 and 18000169215 for tickets created after 2024-01-01"
```
Returns side-by-side comparison with:
- Total tickets per team
- Tickets by status (Open, In Progress, Pending, Resolved, Closed)
- Closure rate percentage
- Average resolution time
- Top 5 agents per team with their ticket counts

**Summary statistics** show which team has:
- Highest total tickets
- Best closure rate
- Fastest average resolution time

## Testing

For testing purposes, you can start the server manually:

```bash
uvx freshservice-mcp --env FRESHSERVICE_APIKEY=<your_api_key> --env FRESHSERVICE_DOMAIN=<your_domain>
```

## Troubleshooting

- Verify your Freshservice API key and domain are correct
- Ensure proper network connectivity to Freshservice servers
- Check API rate limits and quotas (Freshservice typically limits to ~500 requests/hour)
- Verify the `uvx` command is available in your PATH
- For analytics functions, the 5-minute agent/group lookup cache significantly reduces API calls

### Recent Improvements

**Pagination Fix (2026-01-05)**: Analytics functions now correctly retrieve ALL results, not just the first page (30 results). The server uses dual pagination logic that checks both result counts and Link headers.

**Status Mappings (2026-01-05)**: All 7 ticket statuses are now supported:
- Open (2)
- Pending (3)
- Resolved (4)
- Closed (5)
- In Progress (6)
- Pending Return (7)

**Ticket Assignment (2026-01-05)**: `create_ticket` now supports `group_id` and `responder_id` parameters for immediate ticket assignment.


## License

This MCP server is licensed under the MIT License. See the LICENSE file in the project repository for full details.

## Additional Resources

- [Freshservice API Documentation](https://api.freshservice.com/)
- [Claude Desktop Integration Guide](https://docs.anthropic.com/claude/docs/claude-desktop)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

---

<p align="center">Built with ❤️ by effy</p>
