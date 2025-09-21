#!/usr/bin/env python3
"""
Test script for JACAI application
"""

import requests
import json

def test_jacai():
    base_url = "http://localhost:8081"
    
    print("🧪 Testing JACAI API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test content generation
    try:
        data = {
            "topic": "AI and productivity",
            "platforms": ["instagram", "twitter"],
            "style": "professional"
        }
        response = requests.post(f"{base_url}/api/generate", json=data)
        print(f"✅ Content generation: {response.status_code}")
        result = response.json()
        if result.get("success"):
            print(f"   Generated {len(result['results'])} posts")
            for post in result['results']:
                print(f"   - {post['platform']}: {post['content']['caption'][:50]}...")
        else:
            print(f"   Error: {result.get('error')}")
    except Exception as e:
        print(f"❌ Content generation failed: {e}")
    
    # Test login
    try:
        data = {"username": "demo", "password": "demo"}
        response = requests.post(f"{base_url}/api/login", json=data)
        print(f"✅ Login test: {response.status_code}")
        result = response.json()
        if result.get("success"):
            print(f"   Token: {result['token'][:20]}...")
        else:
            print(f"   Error: {result.get('error')}")
    except Exception as e:
        print(f"❌ Login test failed: {e}")

if __name__ == "__main__":
    test_jacai()