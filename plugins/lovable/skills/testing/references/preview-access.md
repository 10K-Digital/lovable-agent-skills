# Preview Access: URLs, Tokens, and Sessions

How to obtain and maintain access to a Lovable project's Preview app for automated testing.

## What is the Preview?

Lovable Preview is the live, running build of the app - the same thing the user sees in the right panel of the Lovable editor. It reflects the latest synced code (including unpublished changes), which makes it the right target for testing after each implementation: you test what was just built, before/independent of publishing to production.

Preview URL format:

```
https://preview--[app-name].lovable.app/
```

## Access Methods

### Method 1: Tokenized Preview URL (preferred for automation)

Lovable generates a shareable preview URL containing a JWT access token:

```
https://preview--[app-name].lovable.app/?__lovable_token=eyJhbGciOiJSUzI1NiIs...
```

**How the user captures it:**
1. Open the Lovable project at lovable.dev
2. Make sure the right panel is in **Preview mode** (not code view)
3. Click the **arrow icon at the top of the preview, next to the preview address bar** ("open in new tab")
4. A new browser tab opens - the full URL in that tab contains `?__lovable_token=...`
5. Copy the entire URL

**Token properties:**
- It's a JWT (three base64url segments separated by dots)
- Payload contains `user_id`, `project_id`, `iat` (issued at), `exp` (expiry)
- **Valid for 7 days** from issuance
- Grants access to the preview app for that project - treat it as a credential

### Method 2: Logged-in Browser Session

If the user is logged in to Lovable in Chrome (with the Claude in Chrome extension connected), navigate to the bare preview URL (`https://preview--[app-name].lovable.app/`) or open the preview from within the Lovable editor. The session cookie provides access - no token needed.

**Trade-offs:** No token maintenance, but breaks if the user logs out, and requires the Chrome extension with an active session.

## Access Priority (decision order)

```
1. preview-token.local exists AND token not expired
   → Navigate to: [preview_url]?__lovable_token=[token]

2. Token missing/expired, Access Method is browser-login OR user likely logged in
   → Navigate to bare preview URL
   → If app loads (not a login/denied page) → proceed
   → If login wall appears → fall through to 3

3. Ask the user:
   "I need access to your Lovable Preview to run tests. Either:
    A) Log in to Lovable in Chrome, or
    B) Paste a fresh preview URL with token:
       (Lovable project → preview mode → click the arrow icon next to
        the address bar → copy the URL from the new tab)"

4. If browser automation itself is unavailable
   → Output manual test checklist (never block)
```

## Storing Access Safely

**The token is a credential. NEVER:**
- Commit it to git
- Write it into AGENTS.md or CLAUDE.md
- Write the base URL and dates into `.lovable-agent/config.json` under `testing`
- Echo the full token back in chat output (refer to it as "stored token")

**Storage layout:**

| What | Where | Committed? |
|------|-------|-----------|
| Base preview URL (no token) | `.lovable-agent/config.json` → `testing.preview_url` | ✅ Yes |
| Token | `.lovable-agent/preview-token.local` | ❌ Gitignored |
| Capture date + expiry date | `.lovable-agent/config.json` → `testing.token_captured`, `testing.token_expires` | ✅ Yes (dates only) |

**`preview-token.local` format** (token string only, single line):
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoi...
```

**Gitignore enforcement:** when scaffolding the workspace, ensure the project's `.gitignore` contains:
```
.lovable-agent/preview-token.local
```
If `.gitignore` is missing the entry, add it BEFORE writing the token file.

## Parsing a Pasted Preview URL

When the user pastes a full tokenized URL:

1. **Split** at `?__lovable_token=`:
   - Left part → `preview_url` (strip trailing `/` and `?`)
   - Right part → token (strip any additional query params after `&`)
2. **Validate the token shape**: three dot-separated base64url segments
3. **Decode the payload** (second segment, base64url → JSON) to extract:
   - `exp` → expiry as unix timestamp → store as ISO date in `token_expires`
   - `iat` → captured date → store in `token_captured`
   - `project_id` → sanity check against `lovable_url` in CLAUDE.md if available
4. **Write**:
   - Token → `preview-token.local`
   - URL + dates → `.lovable-agent/config.json` under `testing`
5. **Confirm** to the user (without echoing the token):
   ```
   ✅ Preview access configured
   - Preview URL: https://preview--my-app.lovable.app
   - Token valid until: 2026-06-17 (7 days)
   - Token stored in preview-token.local (gitignored)
   ```

Decoding `exp` example (shell):
```bash
echo "[middle-segment]" | tr '_-' '/+' | base64 -d 2>/dev/null | head -c 1000
# → {"user_id":"...","project_id":"...","exp":1781707140,...}
```

## Expiry Handling

**Before every test run:**
1. Read `testing.token_expires` from `.lovable-agent/config.json`
2. If today ≥ expiry date (or within 12 hours of it) → treat as expired
3. If expired:
   - Try Method 2 (logged-in session) silently first
   - If that fails, prompt for a fresh URL:

```
🔑 Your preview token expired on [date] (tokens last 7 days).

To capture a fresh one:
1. Open your Lovable project, switch to preview mode
2. Click the arrow icon at the top, next to the address bar
3. Copy the URL from the new tab and paste it here

Or just log in to Lovable in Chrome and I'll use your session.
```

4. On receiving a new URL, re-run the parsing procedure above

**Detecting a rejected token at runtime:** if navigation with a token lands on an error page, access-denied message, or Lovable login screen, treat it the same as expiry (the token may have been revoked) and re-prompt.

## Verifying Access Works

After configuring access (and at the start of each test session), do a quick access check:

1. Navigate to the preview URL (with token if using Method 1)
2. Wait for page load (up to 30s - preview cold starts can be slow)
3. Success: app content renders (root element populated, no Lovable login/error page)
4. Read console for fatal errors
5. Report:
   ```
   ✅ Preview access verified - app loaded at [preview_url]
   ```
   or the appropriate error + fallback from SKILL.md.
