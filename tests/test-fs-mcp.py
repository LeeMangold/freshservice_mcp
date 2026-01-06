import asyncio
from freshservice_mcp.server import (
    add_requester_to_group, create_ticket, filter_agents, filter_requesters,
    filter_tickets, publish_solution_article, update_ticket, delete_ticket,
    get_ticket_by_id, list_service_items, get_requested_items, create_service_request,
    create_ticket_note, send_ticket_reply, list_all_ticket_conversation,
    update_ticket_conversation, get_all_products, get_products_by_id, create_product,
    update_product, create_requester, get_requester_id, update_requester,
    list_all_requester_fields, create_agent, get_agent, get_all_agents, update_agent,
    get_agent_fields, get_all_agent_groups, getAgentGroupById, create_group,
    update_requester_group, update_group, get_requester_groups_by_id,
    list_requester_group_members, create_requester_group, list_all_workspaces,
    get_workspace, get_all_canned_response, get_canned_response,
    list_all_canned_response_folder, get_all_solution_category, get_solution_category,
    create_solution_category, update_solution_category, get_list_of_solution_folder,
    create_solution_folder, update_solution_folder, create_solution_article,
    update_solution_article, get_list_of_solution_article, get_solution_article,
    # New analytics functions
    get_agent_lookup, search_tickets_all, get_ticket_stats, get_agent_workload,
    get_team_comparison
)

async def test_create_ticket():
    payload = {
  "email": "marketing.lead@company.com",
  "source": 2,
  "status": 2,
  "subject": "Network Connectivity Issues in Marketing Department",
  "priority": 3,
  "description": "Several employees in the Marketing department are experiencing intermittent network connectivity issues. The problem started this morning around 9:30 AM. Users report that their internet connection drops every 15-20 minutes and reconnects after about 30 seconds. This is disrupting their workflow, especially for those working on time-sensitive campaign materials."
}
    result = await create_ticket(payload["subject"],payload["description"],payload["source"],payload["priority"],payload["status"],payload["email"])
    print(result)

async def test_create_ticket_with_group_and_responder():
    """Test creating a ticket with group_id and responder_id"""
    result = await create_ticket(
        subject="Test ticket with group and responder assignment",
        description="This ticket tests the new group_id and responder_id parameters",
        source=2,  # Portal
        priority=2,  # Medium
        status=2,  # Open
        email="test@example.com",
        group_id=18000169214,  # Security Team
        responder_id=18000806759  # Lee Mangold
    )
    print(result)

async def test_update_ticket():
    ticket_id = 862
    ticket_fields = {
        "source": 3,
        "status": 2,
        "subject": "UPDATED",
        "priority": 4,
    }
    result = await update_ticket(ticket_id,ticket_fields)
    print(result)

async def test_delete_ticket():
    ticket_id = 862
    result = await delete_ticket(ticket_id)
    print(result)

async def test_get_ticket_by_id():
    ticket_id = 861
    result = await get_ticket_by_id(ticket_id)
    print(result)

async def test_list_service_items():
    result = await list_service_items()
    print(result)

async def test_get_requested_items():
    ticket_id = 848
    result = await get_requested_items(ticket_id)
    print(result)

async def test_create_service_request():
    display_id = 10
    email = "maanaesh.s@effy.co.in"
    requested_for = "gopi@effy.co.in"
    quantity= 2
    result = await create_service_request(display_id,email,requested_for,quantity)
    print(result)

async def test_create_ticket_note():
    ticket_id = 848
    body="<h1>TEST NOTE</h1>"
    result = await create_ticket_note(ticket_id,body)
    print(result)


async def test_send_ticket_reply():
    ticket_id = 848
    body = "Thank you for reaching out. We are reviewing your ticket and will get back to you shortly."
    result = await send_ticket_reply(
        ticket_id=ticket_id,
        body=body,    
    )
    print(result)

async def test_list_all_ticket_conversation():
    ticket_id = 848
    result = await list_all_ticket_conversation(ticket_id)
    print(result)

async def test_update_ticket_conversation():
  
    id = 27094915080
    body = "<h1>Hiiii</h1>"
    result = await update_ticket_conversation(id,body)
    print(result)

async def test_get_all_products():
    result = await get_all_products()
    print(result)

async def test_get_products_by_id():
    id = 27000094367
    result = await get_products_by_id(id)
    print(result)

async def test_create_product():
    result = await create_product(
        name="Laptop X100",
        asset_type_id=27000798668,
        manufacturer="TechCorp",
        status="In Pipeline",
        mode_of_procurement="Buy",
        description="High-performance business laptop",
    )
    print(result)
async def test_update_product():
    updated_product = await update_product(
        id=27000331519,
        name="Laptop X100 - Updated",
        asset_type_id=27000798668,
        manufacturer="TechCorp International",
        status=1,
        mode_of_procurement="Lease",
        description="<div>Updated: Now with better specs</div>",
    )
    print(updated_product)

async def test_create_requester():
    first_name="Havertz",
    primary_email="havertz@arsenal.com"
    result = await create_requester(first_name=str(first_name),primary_email=primary_email)
    print(result)

async def test_get_requester_id():
    id = 27005859432
    result = await get_requester_id(id)
    print(result)

async def test_update_requester():
    id = 27005859432
    result = await update_requester(requester_id=id,first_name="Kai")
    print(result)

async def test_list_all_requester_fields():
    result = await list_all_requester_fields()
    print(result)
async def test_create_agent():
    name = "Raya"
    email = "davidraya@arsenal.com"
    result = await create_agent(first_name=name,email=email)
    print(result)
async def test_get_agent():
    id = 27005859458
    result = await get_agent(id)
    print(result)

async def test_get_all_agents():
    result = await get_all_agents()
    print(result)

async def test_update_agent():
    id=27005859458
    email="leno@afc.co.in"
    result = await update_agent(agent_id=id,email=email)
    print(result)

async def test_get_agent_fields():
    result = await get_agent_fields()
    print(result)

async def test_get_all_agent_groups():
    result = await get_all_agent_groups()
    print(result)

async def test_getAgentGroupById():
    id = 27000298443
    result = await getAgentGroupById(id)
    print(result)

async def test_create_group():
    payload = {
  "name": "Support Team effy x TEST",
  "description": "Handles general support inquiries",
  "agent_ids": [27000465570],
  "auto_ticket_assign": True,
  "escalate_to": 201,
  "unassigned_for": "THIRTY_MIN"
}
    result = await create_group(group_fields= payload)
    print(result)

async def test_update_group():
    id = 27000298443
    payload = {
        
  "name": "Support Team effy x TEST",
  "description": "Handles general support inquiries",
    }
    result = await update_group(group_id=id , group_fields= payload)
    print(result)

async def test_update_requester_group():
    id = 27000229326
    name = "Capacity Ops"
    result = await update_requester_group(id=id,name=name)
    print(result)

async def test_get_requester_groups_by_id():
    id = 27000229326
    result = await get_requester_groups_by_id(id)
    print(result)

async def test_list_requester_group_members():
    id = 27000229326
    result = await list_requester_group_members(id)
    print(result)

async def test_create_requester_group():
    name="Group A"
    description="List Of teams that belong to Group A"
    result = await create_requester_group(name=name,description=description)
    print(result)

async def test_list_all_workspaces():
    result = await list_all_workspaces()
    print(result)

async def test_get_workspace():
    id=2
    result = await get_workspace(id=id)
    print(result)

async def test_get_all_canned_response():
    result = await get_all_canned_response()
    print(result)

async def test_get_canned_response():
    id = 27000031007
    result = await get_canned_response(id=id)
    print(result)

async def test_list_all_canned_response_folder():
    result = await list_all_canned_response_folder()
    print(result)

async def test_get_all_solution_category():
    result = await get_all_solution_category()
    print(result)

async def test_get_solution_category():
    id = 27000124576
    result = await get_solution_category(id)
    print(result)

async def test_create_solution_category():
    name="Tactical Solutions"
    description="List of tactics to follow"
    result = await create_solution_category(name=name,description=description)
    print(result)

async def test_update_solution_category ():
    id =27000124578
    name = "Football Tactic"
    result = await update_solution_category(category_id=id,name=name)
    print(result)
async def test_get_list_of_solution_folder():
    id = 27000124578
    result = await get_list_of_solution_folder(id=id)
    print(result)

async def test_create_solution_folder():
    name="433 Tactics"
    category_id = 27000124578
    department_ids = [27001017280]
    result = await create_solution_folder(name=name,category_id=category_id,department_ids=department_ids)
    print(result)
    #27000183948

async def test_update_solution_folder():
    id = 27000183948
    name = "GengenPress Tactics"
    result = await update_solution_folder(id=id,name=name)
    print(result)

async def test_create_solution_article():
    title = "GengenPress Football Tactics"
    description = """
        <p>The GengenPress is a high-intensity football tactic where a team immediately presses the ball after losing possession, aiming to win it back quickly.</p>
        <p>This article covers the key principles, advantages, and how to train your squad to master this approach.</p>
    """
    folder_id = 27000183948 
    article_type = 1         # Permanent
    status = 2               # Published
    tags = ["football", "tactics", "pressing", "gengenpress"]
    keywords = ["gengenpress", "football tactics", "high press"]
    review_date = "2025-12-01"

    result = await create_solution_article(
        title=title,
        description=description,
        folder_id=folder_id,
        article_type=article_type,
        status=status,
        tags=tags,
        keywords=keywords,
        review_date=review_date
    )
    # id 27000093242
    print(result)

async def test_update_solution_article():
    id = 27000093242
    title = "GengenPress Football Tactics - A complete guide"
    result = await update_solution_article(article_id=id,title=title)
    print (result)

async def test_get_list_of_solution_article():
    id= 27000183948
    result = await get_list_of_solution_article(id=id)
    print(result)

async def test_get_solution_article():
    id = 27000093242
    result = await get_solution_article(id=id)
    print(result)

async def test_filter_tickets():
    # Quotes are now automatically added by the function
    query = "priority:3"
    result = await filter_tickets(query)
    print(result)

async def test_filter_requesters():
    query = "primary_email:'vijay.r@effy.co.in'"  
    include_agents = True  

    result = await filter_requesters(query, include_agents)
    print(result)
        
async def test_filter_agents():
    # Quotes are now automatically added by the function
    # Note: use valid filter fields like first_name, email, etc.
    query = "first_name:John"
    agents = await filter_agents(query)
    print(agents)

async def test_add_requester_to_group():
    group_id = 27000229326  
    requester_id = 27005854063  

    result = await add_requester_to_group(group_id, requester_id)
    print(result)

async def test_publish_solution_article():
    article_id = 27000093217
    result = await publish_solution_article(article_id)
    print(result)

# ANALYTICS FUNCTION TESTS

async def test_get_agent_lookup():
    """Test agent and group lookup cache"""
    result = await get_agent_lookup()
    print("\n=== Agent Lookup Test ===")
    print(f"Success: {result.get('success')}")
    print(f"Cached at: {result.get('cached_at')}")
    print(f"Number of agents: {len(result.get('agents', {}))}")
    print(f"Number of groups: {len(result.get('groups', {}))}")
    print(f"Cache age: {result.get('cache_age_seconds')} seconds")

async def test_search_tickets_all():
    """Test paginated ticket search"""
    result = await search_tickets_all(
        query="status:2",  # Open tickets
        max_results=100
    )
    print("\n=== Search Tickets All Test ===")
    print(f"Success: {result.get('success')}")
    print(f"Total fetched: {result['total_fetched']}")
    print(f"Pages fetched: {result['pages_fetched']}")
    print(f"Truncated: {result['truncated']}")
    if result.get('tickets'):
        print(f"First ticket ID: {result['tickets'][0].get('id')}")

async def test_get_ticket_stats():
    """Test aggregated ticket statistics"""
    result = await get_ticket_stats(
        group_id=18000169214,  # Security Team
        created_after="2024-01-01"
    )
    print("\n=== Ticket Stats Test ===")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        stats = result.get('stats', {})
        print(f"Total tickets: {stats.get('total_tickets')}")
        print(f"By status: {stats.get('by_status')}")
        print(f"By priority: {stats.get('by_priority')}")
        print(f"Top 3 agents: {list(stats.get('by_agent', {}).items())[:3]}")

async def test_get_agent_workload():
    """Test agent workload metrics"""
    result = await get_agent_workload(
        agent_id=18000806759,  # Lee Mangold
        period="30d"
    )
    print("\n=== Agent Workload Test ===")
    print(f"Success: {result.get('success')}")
    if result.get('success') and result.get('agents'):
        agent = result['agents'][0]
        print(f"Agent: {agent.get('agent_name')}")
        print(f"Tickets assigned: {agent.get('tickets_assigned')}")
        print(f"Tickets resolved: {agent.get('tickets_resolved')}")
        print(f"Tickets open: {agent.get('tickets_open')}")
        print(f"Avg resolution hours: {agent.get('avg_resolution_hours')}")

async def test_get_agent_workload_by_group():
    """Test workload metrics for all agents in a group"""
    result = await get_agent_workload(
        group_id=18000169214,  # Security Team
        period="30d"
    )
    print("\n=== Group Workload Test ===")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"Group: {result.get('group_name')}")
        print(f"Number of agents: {len(result.get('agents', []))}")
        for agent in result.get('agents', [])[:3]:  # Show top 3
            print(f"  - {agent.get('agent_name')}: {agent.get('tickets_assigned')} tickets")

async def test_get_team_comparison():
    """Test multi-team comparison"""
    # Note: Update these group IDs to match your Freshservice instance
    result = await get_team_comparison(
        group_ids=[18000169214, 18000169215],  # Multiple teams
        created_after="2024-01-01"
    )
    print("\n=== Team Comparison Test ===")
    print(f"Success: {result.get('success')}")
    if result.get('success'):
        print(f"\nTotal tickets (all groups): {result['summary']['total_tickets_all_groups']}")
        print(f"Average closure rate: {result['summary']['average_closure_rate']:.1%}")

        for team in result.get('comparison', []):
            print(f"\n{team['group_name']}:")
            print(f"  Total tickets: {team['total_tickets']}")
            print(f"  Closure rate: {team['closure_rate']:.1%}")
            print(f"  Avg resolution hours: {team['avg_resolution_hours']}")
            print(f"  Top agents: {[a['agent_name'] for a in team['top_agents'][:3]]}")

if __name__ == "__main__":
    # asyncio.run(test_create_ticket())
    # asyncio.run(test_update_ticket())
    # asyncio.run(test_delete_ticket())
    # asyncio.run(test_get_ticket_by_id())
    # asyncio.run(test_list_service_items())
    # asyncio.run(test_get_requested_items())
    # asyncio.run(test_create_service_request())
    # asyncio.run(test_create_ticket_note())
    # asyncio.run(test_send_ticket_reply())
    # asyncio.run(test_list_all_ticket_conversation())
    # asyncio.run(test_update_ticket_conversation())
    # asyncio.run(test_get_all_products())
    # asyncio.run(test_get_products_by_id())
    # asyncio.run(test_create_product())
    # asyncio.run(test_update_product())
    # asyncio.run(test_create_requester())
    # asyncio.run(test_get_requester_id())
    # asyncio.run(test_update_requester())
    # asyncio.run(test_list_all_requester_fields())
    # asyncio.run(test_create_agent())
    # asyncio.run(test_get_agent())
    # asyncio.run(test_get_all_agents())
    # asyncio.run(test_update_agent())
    # asyncio.run(test_get_agent_fields())
    # asyncio.run(test_get_all_agent_groups())
    # asyncio.run(test_getAgentGroupById())
    # asyncio.run(test_create_group())
    # asyncio.run(test_update_group())
    # asyncio.run(test_update_requester_group())
    # asyncio.run(test_get_requester_groups_by_id())
    # asyncio.run(test_list_requester_group_members())
    # asyncio.run(test_create_requester_group())
    # asyncio.run(test_list_all_workspaces())
    # asyncio.run(test_get_workspace())
    # asyncio.run(test_get_all_canned_response())
    # asyncio.run(test_get_canned_response())
    # asyncio.run(test_list_all_canned_response_folder())
    # asyncio.run(test_get_all_solution_category())
    # asyncio.run(test_create_solution_category())
    # asyncio.run(test_update_solution_category())
    # asyncio.run(test_get_list_of_solution_folder())
    # asyncio.run(test_create_solution_folder())
    # asyncio.run(test_update_solution_folder())
    # asyncio.run(test_create_solution_article())
    # asyncio.run(test_update_solution_article()) 
    # asyncio.run(test_get_list_of_solution_article())
    # asyncio.run(test_get_solution_article())
    asyncio.run(test_filter_tickets())
    # asyncio.run(test_filter_requesters())
    # asyncio.run(test_filter_agents())
    # asyncio.run(test_publish_solution_article())
    # asyncio.run(test_add_requester_to_group())

    # Analytics function tests
    # asyncio.run(test_get_agent_lookup())
    # asyncio.run(test_search_tickets_all())
    # asyncio.run(test_get_ticket_stats())
    # asyncio.run(test_get_agent_workload())
    # asyncio.run(test_get_agent_workload_by_group())
    # asyncio.run(test_get_team_comparison())
