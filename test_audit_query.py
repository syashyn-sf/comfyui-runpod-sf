#!/usr/bin/env python3
"""
Test different approaches to query audit logs from RunPod GraphQL API
"""

import os
import requests
import json

# Use the API key from environment
API_KEY = (
    os.environ.get('COMFYUI_RUNPOD_API_KEY') or
    os.environ.get('API_KEY_RUNPOD') or
    os.environ.get('RUNPOD_API_KEY')
)

if not API_KEY:
    print("❌ No API key found! Set COMFYUI_RUNPOD_API_KEY environment variable")
    exit(1)

ENDPOINT = 'https://api.runpod.io/graphql'

def test_query(query_name, query, variables=None):
    """Test a GraphQL query and print results"""
    print(f"\n{'='*60}")
    print(f"Testing: {query_name}")
    print(f"{'='*60}")

    url = f"{ENDPOINT}?api_key={API_KEY}"
    payload = {'query': query}
    if variables:
        payload['variables'] = variables

    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})

    print(f"Status: {response.status_code}")

    try:
        result = response.json()
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))
        return result
    except:
        print(f"Raw response: {response.text}")
        return None

# Test 1: Try auditLogs with empty input
print("\n🔍 Attempt 1: auditLogs with empty input object")
query1 = """
query {
    auditLogs(input: {}) {
        edges {
            actorId
            email
            resourceType
            resourceId
            action
            timestamp
        }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
"""
test_query("auditLogs with empty input", query1)

# Test 2: Try auditLogs without any arguments
print("\n🔍 Attempt 2: auditLogs without arguments")
query2 = """
query {
    auditLogs {
        edges {
            actorId
            email
            resourceType
            resourceId
            action
            timestamp
        }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
"""
test_query("auditLogs without arguments", query2)

# Test 3: Try with pagination parameters
print("\n🔍 Attempt 3: auditLogs with first/after")
query3 = """
query {
    auditLogs(first: 10) {
        edges {
            actorId
            email
            resourceType
            resourceId
            action
            timestamp
        }
        pageInfo {
            hasNextPage
            endCursor
        }
    }
}
"""
test_query("auditLogs with first: 10", query3)

# Test 4: Try checking if myself has auditLogs
print("\n🔍 Attempt 4: Check myself for auditLogs")
query4 = """
query {
    myself {
        id
        email
    }
}
"""
result = test_query("Check myself fields", query4)

# Test 5: Try to use impersonations (probably won't work but worth trying)
print("\n🔍 Attempt 5: Try impersonations.auditLogs")
query5 = """
query {
    impersonations {
        auditLogs(input: {}) {
            edges {
                actorId
                email
            }
        }
    }
}
"""
test_query("impersonations.auditLogs", query5)

print("\n" + "="*60)
print("Test complete!")
print("="*60)
