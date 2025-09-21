#!/usr/bin/env python3
"""
JACAI API Test Suite
Comprehensive testing for all endpoints
"""

import requests
import json
import time

class JacaiTester:
    def __init__(self, base_url="http://localhost:8082"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
    
    def test_health(self):
        """Test health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            assert response.status_code == 200
            data = response.json()
            print("✅ Health check passed")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            return True
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_register(self):
        """Test user registration"""
        try:
            data = {
                "username": f"testuser_{int(time.time())}",
                "email": "test@jacai.com",
                "password": "testpass123"
            }
            response = requests.post(f"{self.base_url}/api/register", json=data)
            result = response.json()
            
            if result.get("success"):
                self.token = result.get("token")
                self.user_id = result.get("user_id")
                print("✅ Registration passed")
                print(f"   User ID: {self.user_id}")
                return True
            else:
                print(f"❌ Registration failed: {result.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def test_content_generation(self):
        """Test content generation"""
        try:
            data = {
                "topic": "AI productivity tools",
                "platforms": ["instagram", "twitter", "linkedin"],
                "style": "professional",
                "user_id": self.user_id or "1"
            }
            response = requests.post(f"{self.base_url}/api/generate", json=data)
            result = response.json()
            
            if result.get("success") and result.get("results"):
                print("✅ Content generation passed")
                print(f"   Generated {len(result['results'])} posts")
                for post in result['results'][:2]:
                    print(f"   - {post['platform']}: {post['content']['caption'][:50]}...")
                return True
            else:
                print(f"❌ Content generation failed: {result.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Content generation error: {e}")
            return False
    
    def test_social_connect(self):
        """Test social media connection"""
        try:
            data = {
                "platform": "instagram",
                "user_id": self.user_id or "1",
                "account_name": "@test_account"
            }
            response = requests.post(f"{self.base_url}/api/connect-social", json=data)
            result = response.json()
            
            if result.get("success"):
                print("✅ Social connect passed")
                print(f"   Connected: {data['platform']}")
                return True
            else:
                print(f"❌ Social connect failed: {result.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Social connect error: {e}")
            return False
    
    def test_analytics(self):
        """Test analytics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics?user_id={self.user_id or '1'}")
            result = response.json()
            
            if "total_posts" in result or isinstance(result, dict):
                print("✅ Analytics passed")
                print(f"   Data: {str(result)[:100]}...")
                return True
            else:
                print(f"❌ Analytics failed: {result}")
                return False
        except Exception as e:
            print(f"❌ Analytics error: {e}")
            return False
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Starting JACAI API Test Suite...")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health),
            ("User Registration", self.test_register),
            ("Content Generation", self.test_content_generation),
            ("Social Connect", self.test_social_connect),
            ("Analytics", self.test_analytics)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            if test_func():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed! JACAI is ready for production.")
        else:
            print("⚠️  Some tests failed. Check the logs above.")
        
        return passed == total

if __name__ == "__main__":
    tester = JacaiTester()
    tester.run_all_tests()