#!/usr/bin/env python3
"""
Performance Monitoring Script for Mualleem AI Tutor
Adds detailed timing and resource monitoring to validate performance diagnosis
"""

import time
import psutil
import logging
import asyncio
from datetime import datetime
from functools import wraps
from typing import Dict, Any
import json

# Configure performance logging
performance_logger = logging.getLogger("performance")
performance_logger.setLevel(logging.INFO)

# Create file handler for performance logs
handler = logging.FileHandler("performance.log", encoding='utf-8')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
performance_logger.addHandler(handler)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "requesty_calls": [],
            "qdrant_queries": [],
            "image_processing": [],
            "pdf_processing": [],
            "endpoint_response_times": {},
            "system_resources": []
        }
    
    def log_system_resources(self):
        """Log current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resource_data = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_mb": memory.used / 1024 / 1024,
                "memory_available_mb": memory.available / 1024 / 1024,
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / 1024 / 1024 / 1024
            }
            
            self.metrics["system_resources"].append(resource_data)
            performance_logger.info(f"SYSTEM_RESOURCES: {json.dumps(resource_data)}")
            
        except Exception as e:
            performance_logger.error(f"Error collecting system resources: {e}")
    
    def time_operation(self, operation_type: str, operation_name: str):
        """Decorator to time operations and log them"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.virtual_memory().used / 1024 / 1024
                
                try:
                    result = await func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                    raise
                finally:
                    end_time = time.time()
                    end_memory = psutil.virtual_memory().used / 1024 / 1024
                    duration = end_time - start_time
                    memory_change = end_memory - start_memory
                    
                    timing_data = {
                        "timestamp": datetime.now().isoformat(),
                        "operation_type": operation_type,
                        "operation_name": operation_name,
                        "duration_seconds": round(duration, 3),
                        "memory_change_mb": round(memory_change, 2),
                        "success": success,
                        "error": error
                    }
                    
                    # Add to specific metrics category
                    if operation_type not in self.metrics:
                        self.metrics[operation_type] = []
                    self.metrics[operation_type].append(timing_data)
                    
                    performance_logger.info(f"{operation_type.upper()}: {json.dumps(timing_data)}")
                
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.virtual_memory().used / 1024 / 1024
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                    raise
                finally:
                    end_time = time.time()
                    end_memory = psutil.virtual_memory().used / 1024 / 1024
                    duration = end_time - start_time
                    memory_change = end_memory - start_memory
                    
                    timing_data = {
                        "timestamp": datetime.now().isoformat(),
                        "operation_type": operation_type,
                        "operation_name": operation_name,
                        "duration_seconds": round(duration, 3),
                        "memory_change_mb": round(memory_change, 2),
                        "success": success,
                        "error": error
                    }
                    
                    # Add to specific metrics category
                    if operation_type not in self.metrics:
                        self.metrics[operation_type] = []
                    self.metrics[operation_type].append(timing_data)
                    
                    performance_logger.info(f"{operation_type.upper()}: {json.dumps(timing_data)}")
                
                return result
            
            # Return the appropriate wrapper based on whether function is async
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def log_endpoint_timing(self, endpoint: str, method: str, duration: float, status_code: int):
        """Log endpoint response timing"""
        endpoint_key = f"{method} {endpoint}"
        
        if endpoint_key not in self.metrics["endpoint_response_times"]:
            self.metrics["endpoint_response_times"][endpoint_key] = []
        
        timing_data = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 3),
            "status_code": status_code
        }
        
        self.metrics["endpoint_response_times"][endpoint_key].append(timing_data)
        performance_logger.info(f"ENDPOINT_TIMING: {endpoint_key} - {json.dumps(timing_data)}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate performance analysis report"""
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {},
            "detailed_metrics": self.metrics
        }
        
        # Calculate averages and statistics
        for operation_type, operations in self.metrics.items():
            if operation_type == "system_resources":
                continue
                
            if isinstance(operations, list) and operations:
                durations = [op.get("duration_seconds", 0) for op in operations if op.get("success", False)]
                if durations:
                    report["summary"][operation_type] = {
                        "total_calls": len(operations),
                        "successful_calls": len(durations),
                        "average_duration": round(sum(durations) / len(durations), 3),
                        "min_duration": round(min(durations), 3),
                        "max_duration": round(max(durations), 3),
                        "total_duration": round(sum(durations), 3)
                    }
        
        # Endpoint timing summary
        endpoint_summary = {}
        for endpoint, timings in self.metrics["endpoint_response_times"].items():
            if timings:
                durations = [t["duration_seconds"] for t in timings]
                endpoint_summary[endpoint] = {
                    "total_requests": len(timings),
                    "average_response_time": round(sum(durations) / len(durations), 3),
                    "min_response_time": round(min(durations), 3),
                    "max_response_time": round(max(durations), 3)
                }
        report["summary"]["endpoints"] = endpoint_summary
        
        return report
    
    def save_report(self, filename: str = "performance_report.json"):
        """Save performance report to file"""
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        performance_logger.info(f"Performance report saved to {filename}")

# Global performance monitor instance
perf_monitor = PerformanceMonitor()

def monitor_endpoint(endpoint: str):
    """Middleware decorator for monitoring endpoint performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            perf_monitor.log_system_resources()
            
            try:
                result = await func(*args, **kwargs)
                status_code = getattr(result, 'status_code', 200)
            except Exception as e:
                status_code = 500
                raise
            finally:
                duration = time.time() - start_time
                perf_monitor.log_endpoint_timing(endpoint, "POST", duration, status_code)
            
            return result
        return wrapper
    return decorator