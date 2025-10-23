#!/usr/bin/env python3
"""
Test a deployed Databricks agent via its API endpoint.

This script helps validate agent deployments by testing both
streaming and non-streaming invocations.
"""

import sys
import json
import requests
import argparse
from typing import Optional


def test_invoke(
    url: str,
    token: str,
    message: str,
    stream: bool = False
) -> None:
    """Test agent invocation"""
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": message}],
        "stream": stream
    }
    
    print(f"🔍 Testing {'streaming' if stream else 'non-streaming'} invocation")
    print(f"📤 Message: {message}")
    print()
    
    try:
        response = requests.post(
            f"{url}/invocations",
            headers=headers,
            json=payload,
            stream=stream,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            return
        
        if stream:
            print("📥 Streaming response:")
            print("-" * 50)
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    print(chunk, end='', flush=True)
            print()
            print("-" * 50)
        else:
            result = response.json()
            print("📥 Response:")
            print("-" * 50)
            print(json.dumps(result, indent=2))
            print("-" * 50)
        
        print("✅ Test passed!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def test_health(url: str, token: str) -> bool:
    """Test health endpoint"""
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("🏥 Testing health endpoint")
    
    try:
        response = requests.get(
            f"{url}/health",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check passed!")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def run_tests(
    url: str,
    token: str,
    messages: Optional[list[str]] = None
) -> None:
    """Run comprehensive tests"""
    
    print("=" * 60)
    print(f"🧪 Testing Agent at {url}")
    print("=" * 60)
    print()
    
    # Test health
    if not test_health(url, token):
        print("\n⚠️  Health check failed, skipping other tests")
        return
    
    print()
    
    # Default test messages if none provided
    if not messages:
        messages = [
            "Hello, how are you?",
            "What can you help me with?",
        ]
    
    # Test non-streaming
    for msg in messages:
        print()
        test_invoke(url, token, msg, stream=False)
    
    # Test streaming
    print()
    test_invoke(url, token, messages[0], stream=True)
    
    print()
    print("=" * 60)
    print("🎉 All tests completed!")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Test a deployed Databricks agent"
    )
    parser.add_argument(
        "url",
        help="Agent URL (e.g., https://workspace.cloud.databricks.com/apps/my-agent)"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="Databricks personal access token"
    )
    parser.add_argument(
        "--message",
        action="append",
        help="Test message (can be specified multiple times)"
    )
    parser.add_argument(
        "--health-only",
        action="store_true",
        help="Only test health endpoint"
    )
    parser.add_argument(
        "--stream-only",
        action="store_true",
        help="Only test streaming invocation"
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Skip streaming tests"
    )
    
    args = parser.parse_args()
    
    # Remove trailing slash from URL
    url = args.url.rstrip('/')
    
    if args.health_only:
        test_health(url, args.token)
    elif args.stream_only:
        message = args.message[0] if args.message else "Hello!"
        test_invoke(url, args.token, message, stream=True)
    elif args.no_stream:
        messages = args.message if args.message else ["Hello!"]
        for msg in messages:
            test_invoke(url, args.token, msg, stream=False)
    else:
        run_tests(url, args.token, args.message)


if __name__ == "__main__":
    main()
