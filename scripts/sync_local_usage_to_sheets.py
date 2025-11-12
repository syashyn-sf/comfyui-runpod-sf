#!/usr/bin/env python3
"""
Sync Local Usage Tracking to Google Sheets

Reads usage data from control panel's local tracking files:
- /workspace/user_data/usage_log.json
- /workspace/user_data/user_statistics.json

And syncs them to Google Sheets for easy viewing and billing.

This is the ALTERNATIVE to RunPod's audit logs API (which is not accessible).
"""

import os
import sys
import json
from datetime import datetime

# Add ui directory to path so we can import sheets_sync
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ui'))

try:
    from sheets_sync import SheetsSync
except ImportError:
    print("❌ Error: sheets_sync module not found")
    print("   Make sure gspread and oauth2client are installed")
    sys.exit(1)

# Local tracking files on RunPod pod
USAGE_LOG_FILE = "/workspace/user_data/usage_log.json"
USER_STATS_FILE = "/workspace/user_data/user_statistics.json"

def load_local_usage_data():
    """Load usage data from control panel's local tracking files"""
    usage_data = {}

    # Try to load user statistics file first (has complete session data)
    if os.path.exists(USER_STATS_FILE):
        print(f"📂 Loading user statistics from {USER_STATS_FILE}")
        try:
            with open(USER_STATS_FILE, 'r') as f:
                usage_data = json.load(f)

            print(f"✅ Loaded statistics for {len(usage_data)} users")

            # Convert to format expected by sheets_sync
            for username, stats in usage_data.items():
                # Ensure required fields exist
                if 'total_hours' not in stats:
                    stats['total_hours'] = 0
                if 'total_cost' not in stats:
                    stats['total_cost'] = 0
                if 'sessions' not in stats:
                    stats['sessions'] = []

                print(f"  • {username}: {stats['total_hours']:.2f} hours, ${stats['total_cost']:.2f}")

        except Exception as e:
            print(f"⚠️  Error loading user statistics: {e}")
    else:
        print(f"⚠️  User statistics file not found: {USER_STATS_FILE}")
        print(f"   This means no usage has been tracked yet")

    # Also check usage log for additional context
    if os.path.exists(USAGE_LOG_FILE):
        print(f"\n📂 Found usage log at {USAGE_LOG_FILE}")
        try:
            with open(USAGE_LOG_FILE, 'r') as f:
                usage_log = json.load(f)
            print(f"✅ Usage log has {len(usage_log)} entries")
        except Exception as e:
            print(f"⚠️  Error loading usage log: {e}")
    else:
        print(f"⚠️  Usage log file not found: {USAGE_LOG_FILE}")

    return usage_data

def main():
    """Main function to sync local usage data to Google Sheets"""
    print("=" * 60)
    print("📊 Local Usage Tracker → Google Sheets Sync")
    print("=" * 60)
    print()
    print("📝 This script syncs LOCAL usage tracking data to Google Sheets")
    print("   (Alternative to RunPod API which is not accessible)")
    print()

    # Check for Google Service Account credentials
    if not os.environ.get('GOOGLE_SERVICE_ACCOUNT'):
        print("❌ Error: GOOGLE_SERVICE_ACCOUNT environment variable not set")
        print("   Set it in GitHub Secrets or export it locally:")
        print("   export GOOGLE_SERVICE_ACCOUNT='{ ... json contents ... }'")
        return 1

    # Load local usage data
    print("1️⃣ Loading local usage data...")
    print()
    usage_stats = load_local_usage_data()

    if not usage_stats:
        print()
        print("⚠️  No usage data found")
        print()
        print("💡 This is normal if:")
        print("   • No one has used ComfyUI yet")
        print("   • The control panel hasn't tracked any sessions")
        print("   • The tracking files don't exist yet")
        print()
        print("📌 Usage tracking happens automatically when:")
        print("   1. User launches ComfyUI from control panel")
        print("   2. User stops ComfyUI")
        print("   3. Data is saved to /workspace/user_data/")
        return 0

    # Calculate totals
    print()
    print("2️⃣ Usage Summary:")
    print("-" * 60)
    total_hours = 0
    total_cost = 0

    for username, stats in sorted(usage_stats.items()):
        hours = stats.get('total_hours', 0)
        cost = stats.get('total_cost', 0)
        sessions = len(stats.get('sessions', []))

        total_hours += hours
        total_cost += cost

        print(f"  {username:15} {hours:8.2f} hrs  ${cost:8.2f}  ({sessions} sessions)")

    print("-" * 60)
    print(f"  {'TOTAL':15} {total_hours:8.2f} hrs  ${total_cost:8.2f}")
    print()

    # Sync to Google Sheets
    print("3️⃣ Syncing to Google Sheets...")
    try:
        sheets = SheetsSync()

        if sheets.update_usage_data(usage_stats):
            sheet_url = sheets.get_sheet_url()
            print(f"✅ Successfully synced to Google Sheets!")
            print(f"📊 View at: {sheet_url}")
            print()

            # Also generate monthly report for current month
            now = datetime.now()
            print(f"4️⃣ Generating monthly report for {now.strftime('%B %Y')}...")

            if sheets.create_monthly_report(usage_stats, now.year, now.month):
                print(f"✅ Monthly report created!")

            return 0
        else:
            print("❌ Failed to sync to Google Sheets")
            return 1

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
