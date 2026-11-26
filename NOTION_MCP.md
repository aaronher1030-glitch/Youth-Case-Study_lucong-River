# Connecting Notion to this workspace

**Status:** configured, waiting for you to sign in once.

---

## What was set up

[`opencode.jsonc`](opencode.jsonc) in this folder registers Notion's **hosted MCP server**:

```jsonc
"notion": {
  "type": "remote",
  "url": "https://mcp.notion.com/mcp"
}
```

That is the whole implementation. No install, no daemon, no API token, no page sharing, no local server to keep running.

The endpoint was probed and is live:

```
POST https://mcp.notion.com/mcp  →  401
WWW-Authenticate: Bearer realm="OAuth",
  resource_metadata="https://mcp.notion.com/.well-known/oauth-protected-resource/mcp"
```

A 401 with OAuth metadata is the correct answer — it is how the client learns to start the sign-in flow.

## What you do, once

1. In OpenCode, run **`/mcps`**
2. Select **notion**
3. Complete the browser sign-in with your Notion account

OpenCode discovers the authorization server, signs in with PKCE, stores the tokens outside this project, and refreshes them. Nothing else needs configuring, and the tokens never pass through this folder.

Config changes reload automatically, so no restart is needed. If `notion` does not appear in `/mcps`, run `/reload`.

**Until you sign in, everything reads `needs authentication`.** That is the expected state, not a failure.

## What becomes possible after sign-in

The hosted server exposes Notion-native tools — search, read pages as Markdown, create and edit pages, create databases. It respects your existing Notion permissions, so it can only touch what you can touch.

Once connected, I can build the schedule directly in your workspace: create the `RF2027 — Gantt Schedule` database under your page, add the 42 tasks with owner, phase, dates and status, and set the Timeline view. That is the same outcome as `schedule/notion_setup.py`, without a token.

## Why this replaces the old approach

| | Integration token (old plan) | Hosted MCP (now configured) |
|---|---|---|
| Token to create | Yes | None |
| Page shared with integration | Yes, manually | No |
| Local process to maintain | Yes | No |
| Fails if you forget the Connections step | Yes, silently, with 404 | Not applicable |
| Respects existing Notion permissions | No, integration has its own | Yes |

Keep [`schedule/notion_setup.py`](schedule/notion_setup.py) as plan C — it still works if you ever want a fully scripted build with no OAuth.

## If the OAuth flow fails

**Enterprise policy blocks it.** A workspace admin may have restricted MCP servers. The error names the policy; only an admin can lift it.

**The browser lands on a page that will not load.** Normal when OpenCode runs somewhere the browser cannot reach. Copy the URL from the address bar — it looks like `http://127.0.0.1:52817/callback?code=...&state=...` — and paste it into the sign-in prompt.

**The server never connects.** Some clients need the newer protocol revision. Add one line:

```jsonc
"notion": {
  "type": "remote",
  "url": "https://mcp.notion.com/mcp",
  "protocol": "auto"
}
```

**You want the local server instead.** Notion no longer actively maintains it, but it exists. It needs an integration token and manual page sharing:

```jsonc
"notion-local": {
  "type": "local",
  "command": ["npx", "-y", "@notionhq/notion-mcp-server"],
  "environment": {
    "NOTION_TOKEN": "{env:NOTION_TOKEN}"
  }
}
```

Then set `NOTION_TOKEN` in your environment. Use a different server name so the two do not collide.

**You want to sign in as a different account.** `opencode mcp logout notion`, then `/mcps` again.

---

*Configured 14 November 2026. Endpoint and OAuth behaviour verified against `mcp.notion.com`; setup steps follow the OpenCode V2 MCP documentation at `opencode.ai/v2/docs/mcp-servers`.*
