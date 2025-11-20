#!/usr/bin/env python3
"""
Comprehensive Integration Testing Suite for Mualleem AI Tutor
Tests all integration points: Frontend↔Backend, Backend↔Requesty, Backend↔Qdrant
"""

import os
import json
import time
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI

load_dotenv()

# Test Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://216.81.248.146:3002"
TIMEOUT = 30

class IntegrationTester:
    def __init__(self):
        self.results = {
            "frontend_backend": {},
            "backend_requesty": {},
            "backend_qdrant": {},
            "end_to_end": {},
            "issues_found": [],
            "recommendations": []
        }
    
    def log_result(self, section, test_name, status, details="", error=None):
        """Log test result"""
        result = {
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if error:
            result["error"] = str(error)
        
        self.results[section][test_name] = result
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_symbol} [{section.upper()}] {test_name}: {status}")
        if details:
            print(f"   └─ {details}")
        if error:
            print(f"   └─ Error: {error}")

    def test_frontend_backend_integration(self):
        """Test Section 3.1: Frontend ↔ Backend Integration"""
        print("\n🔄 Testing Frontend ↔ Backend Integration...")
        
        # Test 1: Basic chat endpoint with Arabic text
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                data={"question": "ما هي مشتقة x^2؟"},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                if "answer" in data and data["answer"]:
                    self.log_result("frontend_backend", "arabic_text_chat", "PASS", 
                                  f"Response: {data.get('model_used', 'unknown model')}")
                else:
                    self.log_result("frontend_backend", "arabic_text_chat", "FAIL", 
                                  "No answer in response")
            else:
                self.log_result("frontend_backend", "arabic_text_chat", "FAIL", 
                              f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("frontend_backend", "arabic_text_chat", "FAIL", error=e)

        # Test 2: Image upload validation  
        try:
            # Test with invalid file type
            response = requests.post(
                f"{BACKEND_URL}/chat",
                data={"question": "تحليل الصورة"},
                files={"image": ("test.txt", "hello world", "text/plain")},
                timeout=TIMEOUT
            )
            
            if response.status_code == 400:
                self.log_result("frontend_backend", "image_validation", "PASS", 
                              "Correctly rejected invalid file type")
            else:
                self.log_result("frontend_backend", "image_validation", "FAIL", 
                              f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_result("frontend_backend", "image_validation", "FAIL", error=e)

        # Test 3: Request/Response format documentation
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                data={"question": "اختبار تنسيق الطلب والاستجابة"},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["answer", "question", "has_image", "context_used", "model_used", "provider"]
                missing_fields = [f for f in required_fields if f not in data]
                
                if not missing_fields:
                    self.log_result("frontend_backend", "response_format", "PASS", 
                                  f"All required fields present: {list(data.keys())}")
                else:
                    self.log_result("frontend_backend", "response_format", "FAIL", 
                                  f"Missing fields: {missing_fields}")
            else:
                self.log_result("frontend_backend", "response_format", "FAIL", 
                              f"HTTP {response.status_code}")
        except Exception as e:
            self.log_result("frontend_backend", "response_format", "FAIL", error=e)

    def test_backend_requesty_integration(self):
        """Test Section 3.2: Backend ↔ Requesty.ai Integration"""
        print("\n🤖 Testing Backend ↔ Requesty.ai Integration...")
        
        # Test 1: GPT-4o-mini model
        try:
            client = OpenAI(
                api_key=os.getenv("REQUESTY_API_KEY"),
                base_url=os.getenv("REQUESTY_BASE_URL"),
                default_headers={
                    "HTTP-Referer": os.getenv("SITE_URL"),
                    "X-Title": os.getenv("SITE_NAME")
                }
            )
            
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "اختبار قصير"}],
                max_tokens=50
            )
            
            if response.choices and response.choices[0].message.content:
                self.log_result("backend_requesty", "gpt4o_mini_model", "PASS", 
                              "Successfully generated response")
            else:
                self.log_result("backend_requesty", "gpt4o_mini_model", "FAIL", 
                              "No response content")
        except Exception as e:
            self.log_result("backend_requesty", "gpt4o_mini_model", "FAIL", error=e)

        # Test 2: text-embedding-3-large model
        try:
            embedding_response = client.embeddings.create(
                model="openai/text-embedding-3-large",
                input=["مرحباً بك في منصة معلّم"]
            )
            
            if embedding_response.data:
                embedding_dim = len(embedding_response.data[0].embedding)
                expected_dim = 3072  # text-embedding-3-large dimension
                
                if embedding_dim == expected_dim:
                    self.log_result("backend_requesty", "embedding_model", "PASS", 
                                  f"Generated {embedding_dim}D embeddings")
                else:
                    self.log_result("backend_requesty", "embedding_model", "WARN", 
                                  f"Unexpected dimensions: {embedding_dim} vs {expected_dim}")
            else:
                self.log_result("backend_requesty", "embedding_model", "FAIL", 
                              "No embedding data")
        except Exception as e:
            self.log_result("backend_requesty", "embedding_model", "FAIL", error=e)

        # Test 3: Error handling simulation
        try:
            # Test with invalid model
            response = client.chat.completions.create(
                model="invalid/model-name",
                messages=[{"role": "user", "content": "اختبار"}],
                max_tokens=10
            )
            
            self.log_result("backend_requesty", "error_handling", "FAIL",
                          "Should have failed with invalid model")
        except Exception as e:
            error_str = str(e).lower()
            if ("not found" in error_str or "invalid" in error_str or
                "404" in error_str or "not supported" in error_str or
                "provider and/or model not supported" in error_str):
                self.log_result("backend_requesty", "error_handling", "PASS",
                              "Correctly handled invalid model error")
            else:
                self.log_result("backend_requesty", "error_handling", "WARN",
                              f"Unexpected error type: {e}")

    def test_backend_qdrant_integration(self):
        """Test Section 3.3: Backend ↔ Qdrant Cloud Integration"""
        print("\n💾 Testing Backend ↔ Qdrant Cloud Integration...")
        
        try:
            client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY")
            )
            
            # Test 1: Connection and collection existence
            collections = client.get_collections()
            collection_names = [col.name for col in collections.collections]
            target_collection = os.getenv("QDRANT_COLLECTION_NAME", "mualleem_curriculum")
            
            if target_collection in collection_names:
                self.log_result("backend_qdrant", "connection_and_collection", "PASS", 
                              f"Collection '{target_collection}' exists")
            else:
                self.log_result("backend_qdrant", "connection_and_collection", "FAIL", 
                              f"Collection '{target_collection}' not found")
                return

            # Test 2: Collection configuration
            collection_info = client.get_collection(target_collection)
            vector_size = collection_info.config.params.vectors.size
            distance = collection_info.config.params.vectors.distance
            points_count = collection_info.points_count
            
            self.log_result("backend_qdrant", "collection_config", "PASS", 
                          f"Vectors: {vector_size}D, Distance: {distance}, Points: {points_count}")

            # Test 3: Vector search functionality
            if points_count > 0:
                try:
                    # Use the correct query_points method (modern Qdrant API)
                    search_results = client.query_points(
                        collection_name=target_collection,
                        query=[0.1] * vector_size,
                        limit=1,
                        with_payload=True
                    )
                    if search_results.points:
                        self.log_result("backend_qdrant", "vector_search", "PASS",
                                      f"Query returned {len(search_results.points)} results")
                    else:
                        self.log_result("backend_qdrant", "vector_search", "PASS",
                                      "Query executed but no similar points found")
                except Exception as e:
                    self.log_result("backend_qdrant", "vector_search", "FAIL", error=e)
                    self.results["issues_found"].append(f"Qdrant search error: {e}")
            else:
                self.log_result("backend_qdrant", "vector_search", "SKIP",
                              "No points in collection to search")
                
        except Exception as e:
            self.log_result("backend_qdrant", "connection_and_collection", "FAIL", error=e)

    def test_end_to_end_scenarios(self):
        """Test Section 3.4: End-to-End Integration Scenarios"""
        print("\n🔄 Testing End-to-End Integration Scenarios...")
        
        # Test 1: Complete RAG workflow
        try:
            # First check if we have curriculum data
            response = requests.get(f"{BACKEND_URL}/stats", timeout=TIMEOUT)
            
            if response.status_code == 200:
                stats = response.json()
                if stats.get("total_chunks", 0) > 0:
                    # Test RAG query
                    rag_response = requests.post(
                        f"{BACKEND_URL}/chat",
                        data={"question": "اشرح لي مفهوم من المنهج المرفوع"},
                        timeout=TIMEOUT
                    )
                    
                    if rag_response.status_code == 200:
                        data = rag_response.json()
                        context_used = data.get("context_used", False)
                        
                        if context_used:
                            self.log_result("end_to_end", "rag_workflow", "PASS", 
                                          "RAG context was used in response")
                        else:
                            self.log_result("end_to_end", "rag_workflow", "FAIL", 
                                          "RAG context was not used despite having curriculum data")
                            self.results["issues_found"].append("RAG context retrieval not working")
                    else:
                        self.log_result("end_to_end", "rag_workflow", "FAIL", 
                                      f"Chat request failed: HTTP {rag_response.status_code}")
                else:
                    self.log_result("end_to_end", "rag_workflow", "SKIP", 
                                  "No curriculum data uploaded yet")
            else:
                self.log_result("end_to_end", "rag_workflow", "FAIL", 
                              f"Stats endpoint failed: HTTP {response.status_code}")
        except Exception as e:
            self.log_result("end_to_end", "rag_workflow", "FAIL", error=e)

        # Test 2: Data consistency check
        try:
            backend_stats = requests.get(f"{BACKEND_URL}/stats", timeout=TIMEOUT).json()
            
            # Connect to Qdrant directly to verify consistency
            client = QdrantClient(
                url=os.getenv("QDRANT_URL"),
                api_key=os.getenv("QDRANT_API_KEY")
            )
            
            collection_info = client.get_collection(os.getenv("QDRANT_COLLECTION_NAME", "mualleem_curriculum"))
            
            backend_chunks = backend_stats.get("total_chunks", 0)
            qdrant_points = collection_info.points_count
            
            if backend_chunks == qdrant_points:
                self.log_result("end_to_end", "data_consistency", "PASS", 
                              f"Consistent: {backend_chunks} chunks = {qdrant_points} points")
            else:
                self.log_result("end_to_end", "data_consistency", "WARN", 
                              f"Mismatch: {backend_chunks} chunks vs {qdrant_points} points")
                
        except Exception as e:
            self.log_result("end_to_end", "data_consistency", "FAIL", error=e)

    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        print("\n📋 Generating Recommendations...")
        
        # Count results by status
        total_tests = 0
        passed = 0
        failed = 0
        warnings = 0
        
        for section in self.results:
            if section in ["issues_found", "recommendations"]:
                continue
            for test_name, result in self.results[section].items():
                total_tests += 1
                status = result["status"]
                if status == "PASS":
                    passed += 1
                elif status == "FAIL":
                    failed += 1
                elif status == "WARN":
                    warnings += 1

        # Generate specific recommendations
        recommendations = []
        
        if "RAG context retrieval not working" in self.results["issues_found"]:
            recommendations.append("CRITICAL: Fix RAG search functionality - QdrantClient API method issue needs resolution")
        
        if failed > 0:
            recommendations.append(f"Address {failed} failed test(s) before production deployment")
        
        if warnings > 0:
            recommendations.append(f"Investigate {warnings} warning(s) for potential improvements")
        
        # Add general recommendations
        recommendations.extend([
            "Implement automated integration tests as part of CI/CD pipeline",
            "Add monitoring and alerting for all integration endpoints",
            "Consider implementing retry mechanisms with exponential backoff",
            "Add rate limiting and request throttling for production deployment",
            "Implement comprehensive logging for debugging integration issues"
        ])
        
        self.results["recommendations"] = recommendations
        
        print(f"\n📊 Test Summary: {passed} PASSED, {failed} FAILED, {warnings} WARNINGS out of {total_tests} tests")
        
        for rec in recommendations:
            print(f"💡 {rec}")

    def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 80)
        print("🧪 COMPREHENSIVE INTEGRATION TEST SUITE FOR MUALLEEM AI TUTOR")
        print("=" * 80)
        
        self.test_frontend_backend_integration()
        self.test_backend_requesty_integration() 
        self.test_backend_qdrant_integration()
        self.test_end_to_end_scenarios()
        self.generate_recommendations()
        
        # Save results to file
        with open("integration_test_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full results saved to: integration_test_results.json")
        print("=" * 80)
        
        return self.results

if __name__ == "__main__":
    tester = IntegrationTester()
    results = tester.run_all_tests()