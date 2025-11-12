# RunPod Usage Tracking Limitation

## Issue

After extensive investigation, we discovered that **RunPod does not expose audit logs or historical pod usage via their GraphQL API**.

### What We Tried

1. **Audit Logs Query** - RunPod's GraphQL schema mentions `auditLogs` but:
   - It requires an `input` parameter of type `AuditLogInput!`
   - The input type structure is not documented
   - Introspection is disabled on the API
   - No public examples exist

2. **GraphQL Errors Encountered:**
   ```
   - "Cannot query field auditLogs on type User"
   - "Unknown argument 'first' on field Query.auditLogs"
   - "Field auditLogs argument input of type AuditLogInput! is required"
   - "GraphQL introspection is not allowed"
   ```

### What IS Available

RunPod's GraphQL API provides:
- ✅ **Current pods** - `myself.pods` - Active pods only
- ✅ **Pod details** - GPU type, cost per hour, current uptime
- ✅ **Spending summary** - Account balance, spend limit, current spend/hr
- ❌ **Historical data** - Not available via GraphQL
- ❌ **Past pod sessions** - Not available via GraphQL
- ❌ **User activity logs** - Not available via GraphQL

## Alternative Solutions

### Option 1: Manual Tracking from Web Dashboard

RunPod's web dashboard shows audit logs with full history. You can manually export this data.

### Option 2: Track Only Current Usage

We can track CURRENT pod usage (running pods) but not historical data:

```python
# What we CAN track:
- Currently running pods
- Current GPU usage
- Current hourly spend
- Active users

# What we CANNOT track:
- Past pod sessions
- Historical costs per user
- Who created/deleted which pods
- Total monthly spending per user
```

### Option 3: Internal Tracking (Recommended)

Since the control panel already tracks sessions locally in `/workspace/user_data/usage_log.json`, we could:

1. **Sync local usage logs to Google Sheets**
2. **Track sessions in the control panel** (already implemented)
3. **Export usage data periodically**

This requires pods to be running, but gives us the historical data we need.

## Recommendation

**Stop trying to use RunPod's audit logs API** - it's either not publicly accessible or requires undocumented access.

Instead:
1. Use the **control panel's local tracking** (`/workspace/user_data/usage_log.json`)
2. Add a **manual export to Google Sheets** from the local logs
3. Accept that we can only track usage for pods that have our control panel running

This matches how most cloud platforms work - if you want usage tracking, you implement it yourself.

## Updated Implementation Plan

1. ✅ Keep existing local usage tracking in control panel
2. ✅ Add endpoint to export local logs to Google Sheets
3. ❌ Remove RunPod GraphQL audit log queries (not accessible)
4. ✅ Document limitation clearly

The good news: Your control panel ALREADY tracks all this data locally! We just need to sync it to sheets.
