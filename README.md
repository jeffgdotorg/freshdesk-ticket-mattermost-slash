# freshdesk-ticket-mm-slash-command

A very dirty Python CGI script that implements a Mattermost slash-command which returns a number of different summary reports about tickets in Freshdesk

## KNOWN BUGS

* The script assumes that there are no more than 30 unresolved tickets and no more than 100 companies, requesters, or agents. The script is aware of when this bug bites, and will warn you by appending an OUTPUT INVALID blurb onto the report title. It's not a lot of work to address this, but I don't have time at the moment.

## Installation:

1. Build an HTTPS-enabled Linux / Apache-HTTPD host. Set the web server to start at boot. Be sure that the cron job to renew the certbot stuff is in place, if you used certbot.
1. Configure SELinux to allow the web server to make network connections (and make it persist across reboots):
`setsebool -P httpd_can_network_connect=true`
1. Copy fdtix.py to /var/lib/cgi-bin and make sure its mode is `0755` or similar.
1. In Mattermost's Integrations / Slash Commands interface, add a new slash command:

| Setting | Value |
| ---   | --- |
| Title | `Freshdesk: Ticket queries` |
| Description | `Shows information about Freshdesk tickets, companies, and agents` |
| Command Trigger Word | `fdtix` |
| Request URL | `https://mm-slash-cmds.acme-inc.com/cgi-bin/fdtix.py?key=<a-valid-freshdesk-api-key>` (alter hostname to match the host you installed on) |
| Request Method | `POST` |
| Response Username | `SupportBot` (or your choice) |
| Response Icon | (Blank, or your choice) |
| Autocomplete | `[x]` |
| Autocomplete Hint | `[ summary \| companies \| agents ]` |
| Autocomplete Description | (Blank or make up something useful) |

1. **IMPORTANT**: Mattermost generates a token, which you must copy and paste into the installed `fdtix.py` script as the value of the `mm_token` variable just after the `import` lines at the top. If you don't do this, the slash command will fail to work.
1. Have fun!

## How to find your Freshdesk API key

1. Log in to https://acme-inc.freshdesk.com (substitute your own Freshdesk URL)
1. Click on your profile picture on the top right corner of your portal
1. Go to Profile settings Page
1. Your API key will be available below the change password section to your right

