#!/usr/bin/python3

import cgi
import cgitb
from freshdesk.api import API

# IMPORTANT: Change mm_token to match the value Mattermost gave you when creating the command!
mm_token = "deadbeefcafedada"
fd_site = "acme-inc.freshdesk.com"

cgitb.enable(format="plain")
form = cgi.FieldStorage()

if "key" not in form or "token" not in form or form.getvalue('token') != mm_token:
    print("Content-type: text/plain\r\n\r\nGoodbye")
    exit()

subcommand = form.getvalue("text", "summary")

fd_api_key = form.getvalue('key')
fdapi = API(fd_site, fd_api_key)

tix_data = fdapi.tickets.filter_tickets(query='status:2 OR status:3')

cust_data = fdapi.companies.list_companies()
cust_lookup = {}
for cust in cust_data:
    cust_lookup[cust.id] = cust.name

contacts_data = fdapi.contacts.list_contacts()
contacts_lookup = {}
for contact in contacts_data:
    contacts_lookup[contact.id] = contact.name

agents_data = fdapi.agents.list_agents()
agents_lookup = {}
for agent in agents_data:
    agents_lookup[agent.id] = agent.contact["name"]

status_lookup = { 2: "Open", 3: "Pending", 4: "Resolved", 5: "Closed"}

header = []
ruler = []
rows = []
title = "Report"

if subcommand == "summary":
    title = "Freshdesk: Unresolved Tickets Summary"
    header = [ "**ID**", "**Subject**", "**Company**", "**Contact**", "**Agent**", "**Status**" ]
    for t in tix_data["results"]:
        rows.append( [ str(t["id"]), "[{0}](https://acme-inc.freshdesk.com/a/tickets/{1})".format(t["subject"], t["id"]), cust_lookup.get(t["company_id"], "Unknown"), contacts_lookup.get(t["requester_id"], "Unknown"), agents_lookup.get(t["responder_id"], "Unknown"), status_lookup.get(t["status"], "Other") ] )
elif subcommand == "companies":
    cust_tix = {}
    title = "Freshdesk: Unresolved Tickets by Company"
    header = [ "**Company**", "**Unresolved**" ]
    for cust in cust_data:
        cust_tix[cust_lookup[cust["id"]]] = 0
        for t in tix_data["results"]:
            if t["company_id"] == cust["id"]:
                cust_tix[cust_lookup[cust["id"]]] += 1
    ct_sorted = dict(sorted(cust_tix.items(), key=lambda item: item[0]))
    for cust_name in ct_sorted.keys():
        rows.append( [ cust_name, str(cust_tix[cust_name]) ] )
elif subcommand == "agents":
    agent_tix = {}
    title = "Freshdesk: Unresolved Tickets by Agent"
    header = [ "**Agent**", "**Unresolved**" ]
    for agent in agents_data:
        agent_tix[agents_lookup[agent["id"]]] = 0
        for t in tix_data["results"]:
            if t["responder_id"] == agent["id"]:
                agent_tix[agents_lookup[agent["id"]]] += 1
    at_sorted = dict(sorted(agent_tix.items(), key=lambda item: item[0]))
    for agent_name in at_sorted.keys():
        rows.append( [ agent_name, str(agent_tix[agent_name]) ] )

for hi in header:
    ruler.append(":----")

slash_resp = {}
slash_resp["response_type"] = "in_channel"
slash_resp["text"] = """
---
#### """ + title + """

| """ + " | ".join(header) + """ |
|""" + "|".join(ruler) + """|
"""
for r in rows:
    slash_resp["text"] += "| " + " | ".join(r) + " |\n"
slash_resp["text"] += "---"

print("Content-type: application/json\r\n\r\n")
print(json.dumps(slash_resp))
