#!/usr/bin/env python3
"""
Performance and Stability Testing Suite for Mualleem AI Tutor (Section 5)
Comprehensive load testing, performance monitoring, and long-term stability testing
"""

import asyncio
import time
import json
import subprocess
import concurrent.futures
import requests
import psutil
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import logging
import sys

# Test Configuration
BACKEND_URL = "http://216.81.248.146:8000"
TIMEOUT = 30
TEST_DURATION_HOURS = 2  # Long-term stability test duration

# Performance Thresholds (from test plan)
THRESHOLDS = {
    "chat_text_avg": 5.0,      # < 5 seconds average
    "chat_image_avg": 8.0,     # < 8 seconds average  
    "health_avg": 1.0,         # < 1 second
    "success_rate": 95.0,      # > 95% success rate
    "memory_increase_limit": 10.0  # < 10% memory increase over 2 hours
}

class PerformanceStabilityTester:
    def __init__(self):
        self.results = {
            "test_start": datetime.now().isoformat(),
            "load_tests": {},
            "performance_monitoring": {},
            "stability_tests": {},
            "resource_usage": [],
            "summary": {},
            "recommendations": []
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('performance_test.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_system_resources(self):
        """Log current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            resource_data = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_mb": memory.used / 1024 / 1024,
                "memory_available_mb": memory.available / 1024 / 1024
            }
            
            self.results["resource_usage"].append(resource_data)
            return resource_data
            
        except Exception as e:
            self.logger.error(f"Error collecting system resources: {e}")
            return None
    
    async def single_request(self, endpoint: str, method: str = "GET", data: Dict = None, files: Dict = None):
        """Make a single HTTP request and measure response time"""
        url = f"{BACKEND_URL}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "POST":
                if files:
                    response = requests.post(url, data=data, files=files, timeout=TIMEOUT)
                else:
                    response = requests.post(url, data=data, timeout=TIMEOUT)
            else:
                response = requests.get(url, timeout=TIMEOUT)
            
            duration = time.time() - start_time
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "duration": duration,
                "response_size": len(response.content) if response.content else 0
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "status_code": 0,
                "duration": duration,
                "error": str(e)
            }
    
    async def load_test_chat_endpoint(self, concurrent_users: int = 10, duration_minutes: int = 5):
        """Section 5.1.a: Load test /chat endpoint"""
        self.logger.info(f"🚀 Starting load test: {concurrent_users} concurrent users for {duration_minutes} minutes")
        
        test_questions = [
            "ما هي مشتقة x^2؟",
            "اشرح نظرية فيثاغورس",
            "ما هو التكامل بالأجزاء؟",
            "حل المعادلة: 2x + 5 = 15",
            "ما هي قواعد الاشتقاق الأساسية؟"
        ]
        
        results = []
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        # Monitor resources during test
        resource_monitoring = []
        
        while time.time() < end_time:
            # Log system resources
            resource_data = self.log_system_resources()
            if resource_data:
                resource_monitoring.append(resource_data)
            
            # Create concurrent requests
            tasks = []
            for i in range(concurrent_users):
                question = test_questions[i % len(test_questions)]
                data = {"question": f"{question} - طلب رقم {len(results) + i + 1}"}
                task = self.single_request("/chat", "POST", data)
                tasks.append(task)
            
            # Execute requests concurrently
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if not isinstance(result, Exception):
                    results.append(result)
            
            self.logger.info(f"Completed batch of {concurrent_users} requests. Total: {len(results)}")
            
            # Brief pause to avoid overwhelming
            await asyncio.sleep(2)
        
        # Analyze results
        successful_requests = [r for r in results if r.get("success", False)]
        failed_requests = [r for r in results if not r.get("success", False)]
        
        if successful_requests:
            response_times = [r["duration"] for r in successful_requests]
            success_rate = (len(successful_requests) / len(results)) * 100
            
            analysis = {
                "total_requests": len(results),
                "successful_requests": len(successful_requests),
                "failed_requests": len(failed_requests),
                "success_rate": round(success_rate, 2),
                "average_response_time": round(statistics.mean(response_times), 3),
                "min_response_time": round(min(response_times), 3),
                "max_response_time": round(max(response_times), 3),
                "p95_response_time": round(statistics.quantiles(response_times, n=20)[18], 3) if len(response_times) > 10 else round(max(response_times), 3),
                "resource_monitoring": resource_monitoring
            }
        else:
            analysis = {
                "total_requests": len(results),
                "successful_requests": 0,
                "failed_requests": len(failed_requests),
                "success_rate": 0,
                "error": "No successful requests"
            }
        
        self.results["load_tests"]["chat_endpoint"] = analysis
        self.logger.info(f"✅ Chat endpoint load test completed: {analysis.get('success_rate', 0)}% success rate")
        
        return analysis
    
    async def load_test_upload_curriculum(self):
        """Section 5.1.b: Load test /upload-curriculum endpoint"""
        self.logger.info("📚 Starting upload curriculum load test")
        
        # Check if sample PDF exists
        sample_pdf = Path("data/sample_math.pdf")
        if not sample_pdf.exists():
            self.logger.warning("Sample PDF not found, skipping upload load test")
            self.results["load_tests"]["upload_curriculum"] = {"skipped": "Sample PDF not available"}
            return
        
        results = []
        concurrent_uploads = 2  # Reduced to avoid overwhelming
        
        # Monitor resources during upload test
        resource_start = self.log_system_resources()
        
        for i in range(concurrent_uploads):
            with open(sample_pdf, 'rb') as f:
                files = {"file": (f"test_upload_{i}.pdf", f, "application/pdf")}
                result = await self.single_request("/upload-curriculum", "POST", files=files)
                results.append(result)
                self.logger.info(f"Upload {i+1}/{concurrent_uploads} completed: {result.get('status_code', 'ERROR')}")
        
        resource_end = self.log_system_resources()
        
        # Analyze upload results
        successful_uploads = [r for r in results if r.get("success", False)]
        
        analysis = {
            "total_uploads": len(results),
            "successful_uploads": len(successful_uploads),
            "success_rate": (len(successful_uploads) / len(results)) * 100 if results else 0,
            "average_upload_time": round(statistics.mean([r["duration"] for r in successful_uploads]), 3) if successful_uploads else 0,
            "resource_change": {
                "memory_change_mb": (resource_end["memory_used_mb"] - resource_start["memory_used_mb"]) if resource_end and resource_start else 0
            }
        }
        
        self.results["load_tests"]["upload_curriculum"] = analysis
        self.logger.info(f"✅ Upload load test completed: {analysis['success_rate']}% success rate")
    
    async def detailed_response_time_analysis(self):
        """Section 5.1.c: Detailed response time analysis for different endpoints"""
        self.logger.info("⏱️ Starting detailed response time analysis")
        
        endpoints = {
            "/health": {"method": "GET", "expected_time": THRESHOLDS["health_avg"]},
            "/stats": {"method": "GET", "expected_time": 2.0},
            "/chat": {"method": "POST", "data": {"question": "اختبار سرعة الاستجابة"}, "expected_time": THRESHOLDS["chat_text_avg"]}
        }
        
        detailed_results = {}
        
        for endpoint, config in endpoints.items():
            self.logger.info(f"Testing {endpoint}...")
            endpoint_results = []
            
            for i in range(10):  # 10 requests per endpoint
                if config["method"] == "POST":
                    result = await self.single_request(endpoint, "POST", config.get("data"))
                else:
                    result = await self.single_request(endpoint, "GET")
                
                endpoint_results.append(result)
                await asyncio.sleep(0.5)  # Brief pause between requests
            
            # Analyze endpoint results
            successful_results = [r for r in endpoint_results if r.get("success", False)]
            
            if successful_results:
                response_times = [r["duration"] for r in successful_results]
                
                analysis = {
                    "total_requests": len(endpoint_results),
                    "successful_requests": len(successful_results),
                    "success_rate": (len(successful_results) / len(endpoint_results)) * 100,
                    "average_response_time": round(statistics.mean(response_times), 3),
                    "min_response_time": round(min(response_times), 3),
                    "max_response_time": round(max(response_times), 3),
                    "expected_time": config["expected_time"],
                    "meets_threshold": statistics.mean(response_times) <= config["expected_time"]
                }
            else:
                analysis = {
                    "total_requests": len(endpoint_results),
                    "successful_requests": 0,
                    "success_rate": 0,
                    "error": "No successful requests"
                }
            
            detailed_results[endpoint] = analysis
            self.logger.info(f"{endpoint} - Average: {analysis.get('average_response_time', 'N/A')}s")
        
        self.results["performance_monitoring"]["detailed_response_times"] = detailed_results
        self.logger.info("✅ Detailed response time analysis completed")
    
    async def long_term_stability_test(self, hours: int = 2):
        """Section 5.2: Long-term stability testing"""
        self.logger.info(f"🔄 Starting {hours}-hour stability test")
        
        start_time = time.time()
        end_time = start_time + (hours * 3600)
        
        # Track metrics over time
        stability_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "error_count": 0,
            "start_memory": self.log_system_resources(),
            "memory_samples": [],
            "error_log": []
        }
        
        request_types = [
            {"endpoint": "/chat", "method": "POST", "data": {"question": "سؤال استقرار رقم {}"}},
            {"endpoint": "/health", "method": "GET"},
            {"endpoint": "/stats", "method": "GET"}
        ]
        
        while time.time() < end_time:
            # Select request type cyclically
            request_config = request_types[stability_metrics["total_requests"] % len(request_types)]
            
            # Prepare request data
            if request_config["method"] == "POST":
                data = request_config["data"].copy()
                if "question" in data and "{}" in data["question"]:
                    data["question"] = data["question"].format(stability_metrics["total_requests"] + 1)
                result = await self.single_request(request_config["endpoint"], "POST", data)
            else:
                result = await self.single_request(request_config["endpoint"], "GET")
            
            stability_metrics["total_requests"] += 1
            
            # Track results
            if result.get("success", False):
                stability_metrics["successful_requests"] += 1
            else:
                stability_metrics["error_count"] += 1
                stability_metrics["error_log"].append({
                    "request_number": stability_metrics["total_requests"],
                    "endpoint": request_config["endpoint"],
                    "error": result.get("error", f"HTTP {result.get('status_code', 'Unknown')}")
                })
            
            # Log progress every 100 requests
            if stability_metrics["total_requests"] % 100 == 0:
                current_time = datetime.now().strftime('%H:%M:%S')
                success_rate = (stability_metrics["successful_requests"] / stability_metrics["total_requests"]) * 100
                current_memory = self.log_system_resources()
                stability_metrics["memory_samples"].append(current_memory)
                
                self.logger.info(f"[{current_time}] Requests: {stability_metrics['total_requests']}, Success: {success_rate:.1f}%")
            
            # Wait between requests to simulate realistic usage
            await asyncio.sleep(2)
        
        # Final analysis
        end_memory = self.log_system_resources()
        
        if stability_metrics["start_memory"] and end_memory:
            memory_change = ((end_memory["memory_used_mb"] - stability_metrics["start_memory"]["memory_used_mb"]) 
                           / stability_metrics["start_memory"]["memory_used_mb"]) * 100
        else:
            memory_change = 0
        
        final_success_rate = (stability_metrics["successful_requests"] / stability_metrics["total_requests"]) * 100 if stability_metrics["total_requests"] > 0 else 0
        
        stability_analysis = {
            "test_duration_hours": hours,
            "total_requests": stability_metrics["total_requests"],
            "successful_requests": stability_metrics["successful_requests"],
            "error_count": stability_metrics["error_count"],
            "final_success_rate": round(final_success_rate, 2),
            "memory_change_percent": round(memory_change, 2),
            "memory_leak_detected": abs(memory_change) > THRESHOLDS["memory_increase_limit"],
            "stability_passed": final_success_rate >= THRESHOLDS["success_rate"] and abs(memory_change) <= THRESHOLDS["memory_increase_limit"],
            "error_summary": stability_metrics["error_log"][:10]  # First 10 errors
        }
        
        self.results["stability_tests"]["long_term"] = stability_analysis
        self.logger.info(f"✅ Stability test completed: {final_success_rate:.1f}% success, {memory_change:.1f}% memory change")
        
        return stability_analysis
    
    def generate_final_report(self):
        """Generate comprehensive performance and stability report"""
        self.logger.info("📊 Generating final performance report...")
        
        # Calculate overall metrics
        overall_metrics = {
            "test_completion_time": datetime.now().isoformat(),
            "tests_passed": 0,
            "tests_failed": 0,
            "critical_issues": [],
            "performance_bottlenecks": []
        }
        
        # Analyze load test results
        if "chat_endpoint" in self.results["load_tests"]:
            chat_results = self.results["load_tests"]["chat_endpoint"]
            if chat_results.get("success_rate", 0) >= THRESHOLDS["success_rate"]:
                overall_metrics["tests_passed"] += 1
            else:
                overall_metrics["tests_failed"] += 1
                overall_metrics["critical_issues"].append(f"Chat endpoint success rate: {chat_results.get('success_rate', 0)}% < {THRESHOLDS['success_rate']}%")
            
            if chat_results.get("average_response_time", 0) > THRESHOLDS["chat_text_avg"]:
                overall_metrics["performance_bottlenecks"].append(f"Chat response time: {chat_results.get('average_response_time', 0)}s > {THRESHOLDS['chat_text_avg']}s")
        
        # Analyze stability test results
        if "long_term" in self.results["stability_tests"]:
            stability_results = self.results["stability_tests"]["long_term"]
            if stability_results.get("stability_passed", False):
                overall_metrics["tests_passed"] += 1
            else:
                overall_metrics["tests_failed"] += 1
                if stability_results.get("memory_leak_detected", False):
                    overall_metrics["critical_issues"].append(f"Memory leak detected: {stability_results.get('memory_change_percent', 0)}% increase")
        
        # Generate recommendations
        recommendations = []
        
        if overall_metrics["performance_bottlenecks"]:
            recommendations.extend([
                "تحسين أوقات الاستجابة عبر تحسين اتصالات Requesty.ai",
                "إضافة connection pooling لـ Qdrant",
                "تحسين معالجة الصور باستخدام async I/O"
            ])
        
        if overall_metrics["critical_issues"]:
            recommendations.extend([
                "مراجعة إدارة الذاكرة وإصلاح memory leaks",
                "تحسين error handling و retry mechanisms",
                "إضافة monitoring وalerts للإنتاج"
            ])
        
        recommendations.extend([
            "تنفيذ automated performance tests في CI/CD",
            "إضافة rate limiting محسن للإنتاج",
            "مراقبة مستمرة لاستخدام الموارد"
        ])
        
        self.results["summary"] = overall_metrics
        self.results["recommendations"] = recommendations
        
        # Production readiness assessment
        production_ready = (
            overall_metrics["tests_passed"] >= overall_metrics["tests_failed"] and
            len(overall_metrics["critical_issues"]) == 0
        )
        
        self.results["production_readiness"] = {
            "ready": production_ready,
            "confidence_level": "High" if production_ready else "Medium" if overall_metrics["tests_passed"] > 0 else "Low"
        }
        
        return self.results
    
    def save_report(self, filename: str = "performance_stability_report.json"):
        """Save comprehensive report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📁 Full report saved to: {filename}")
    
    async def run_all_tests(self):
        """Run complete performance and stability test suite"""
        self.logger.info("=" * 80)
        self.logger.info("🧪 COMPREHENSIVE PERFORMANCE & STABILITY TEST SUITE")
        self.logger.info("=" * 80)
        
        try:
            # Section 5.1: Load Testing
            self.logger.info("\n📈 SECTION 5.1: LOAD TESTING")
            await self.load_test_chat_endpoint(concurrent_users=10, duration_minutes=5)
            await self.load_test_upload_curriculum()
            await self.detailed_response_time_analysis()
            
            # Section 5.2: Long-term Stability
            self.logger.info("\n⏳ SECTION 5.2: LONG-TERM STABILITY")
            await self.long_term_stability_test(hours=TEST_DURATION_HOURS)
            
            # Generate final report
            self.logger.info("\n📊 GENERATING FINAL REPORT")
            report = self.generate_final_report()
            self.save_report()
            
            # Print summary
            self.logger.info("=" * 80)
            self.logger.info("📋 TEST SUMMARY")
            self.logger.info("=" * 80)
            
            summary = report["summary"]
            self.logger.info(f"✅ Tests Passed: {summary['tests_passed']}")
            self.logger.info(f"❌ Tests Failed: {summary['tests_failed']}")
            self.logger.info(f"🚨 Critical Issues: {len(summary['critical_issues'])}")
            self.logger.info(f"⚠️  Performance Bottlenecks: {len(summary['performance_bottlenecks'])}")
            
            production_ready = report["production_readiness"]
            self.logger.info(f"🎯 Production Ready: {production_ready['ready']} ({production_ready['confidence_level']} confidence)")
            
            if summary['critical_issues']:
                self.logger.info("\n🚨 CRITICAL ISSUES:")
                for issue in summary['critical_issues']:
                    self.logger.info(f"   • {issue}")
            
            if summary['performance_bottlenecks']:
                self.logger.info("\n⚠️  PERFORMANCE BOTTLENECKS:")
                for bottleneck in summary['performance_bottlenecks']:
                    self.logger.info(f"   • {bottleneck}")
            
            self.logger.info("\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                self.logger.info(f"   • {rec}")
            
            self.logger.info("=" * 80)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Test suite failed with error: {e}")
            raise

async def main():
    """Main function to run performance and stability tests"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick test mode for faster debugging
        global TEST_DURATION_HOURS
        TEST_DURATION_HOURS = 0.1  # 6 minutes instead of 2 hours
        print("⚡ Running in QUICK TEST mode (6 minutes stability test)")
    
    tester = PerformanceStabilityTester()
    results = await tester.run_all_tests()
    return results

if __name__ == "__main__":
    asyncio.run(main())