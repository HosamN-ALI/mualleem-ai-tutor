#!/usr/bin/env python3
"""
Stability Test Monitor - Monitor the ongoing 2-hour stability test
"""

import time
import json
import psutil
import os
from datetime import datetime, timedelta

def monitor_test_progress():
    """Monitor the stability test progress"""
    print("🔍 Monitoring ongoing stability test...")
    
    # Check if the test process is running
    test_running = False
    test_pid = None
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python3' and 'performance_stability_test.py' in ' '.join(proc.info['cmdline']):
                test_running = True
                test_pid = proc.info['pid']
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if not test_running:
        print("❌ Stability test is not running")
        return
    
    print(f"✅ Stability test is running (PID: {test_pid})")
    
    # Check log file for latest updates
    log_file = "performance_test.log"
    if os.path.exists(log_file):
        print(f"\n📋 Latest log entries:")
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Show last 5 lines
            for line in lines[-5:]:
                print(f"   {line.strip()}")
    
    # Estimate completion time
    # Test started around 07:25, should complete around 09:25
    start_time = datetime.fromisoformat("2025-11-20T07:25:00")
    expected_end = start_time + timedelta(hours=2)
    now = datetime.now()
    
    if now < expected_end:
        remaining = expected_end - now
        print(f"\n⏱️  Estimated completion: {expected_end.strftime('%H:%M:%S')}")
        print(f"⏳ Time remaining: {str(remaining).split('.')[0]}")
    else:
        print(f"\n✅ Test should be completed or nearly completed")
    
    # Check if results file exists
    if os.path.exists("performance_stability_report.json"):
        print(f"\n📊 Results file found - test may be complete!")
        try:
            with open("performance_stability_report.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "production_readiness" in data:
                    readiness = data["production_readiness"]
                    print(f"🎯 Production Ready: {readiness.get('ready', 'Unknown')}")
                    print(f"📈 Confidence: {readiness.get('confidence_level', 'Unknown')}")
        except Exception as e:
            print(f"⚠️  Error reading results: {e}")

if __name__ == "__main__":
    monitor_test_progress()