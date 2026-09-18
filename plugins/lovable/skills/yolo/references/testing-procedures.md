# Credit-Efficient Deployment Verification

When testing is enabled, verify without sending follow-up Lovable prompts.

1. **Hosted-state check:** Read deployment status, function logs, or database schema from Lovable
   **Cloud** in the authenticated browser. Check only the affected artifacts. Never expose secret
   values and never ask Lovable chat/MCP to show logs or schema.
2. **Direct check:** Exercise the affected endpoint or user flow with the smallest safe request.
   Treat destructive, paid, and irreversible actions as manual.
3. **Local/Preview check:** Run the smallest affected local test set or Preview plan (`--changed` or
   `--smoke` before `--all`) according to project configuration.
4. Record the evidence and distinguish **accepted**, **deployed**, and **functionally verified**.
   If Cloud/browser access is unavailable, report the verification as pending and provide the exact
   manual Cloud navigation; do not consume another Lovable prompt merely to change the label.

For migrations, compare the locally reviewed SQL with the affected table/schema shown in Cloud. For
Edge Functions, compare deployment timestamp/status, inspect only relevant log entries, and make a
safe direct call when possible. Use the original deployment response as supporting—not sole—evidence.
