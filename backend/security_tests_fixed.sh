#!/bin/bash

echo "=== اختبارات الأمان الشاملة لنظام معلّم ==="
echo "التاريخ: $(date)"
echo "الخادم: http://216.81.248.146:8000"
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

echo "=== 🔒 Section 6.1: اختبارات الصلاحيات والوصول ==="
echo ""

# Function to test HTTP response
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=$3
    local description=$4
    
    increment_test
    
    echo "Testing: $method $endpoint - $description"
    
    # Use separate curl command to get just the status code
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" \
        "http://216.81.248.146:8000$endpoint" 2>/dev/null)
    
    if [[ "$status_code" =~ ^[0-9]{3}$ ]]; then
        if [[ "$status_code" == "$expected_status" ]]; then
            log_success "$method $endpoint returns $status_code (expected)"
            increment_passed
        elif [[ "$status_code" == "200" && "$expected_status" != "200" ]]; then
            log_critical "$method $endpoint returns 200 - may be exposed!"
            increment_failed
        elif [[ "$status_code" =~ ^[45][0-9][0-9]$ ]]; then
            log_success "$method $endpoint properly blocked ($status_code)"
            increment_passed
        else
            log_info "$method $endpoint returns $status_code"
            increment_passed
        fi
    else
        log_warning "Failed to get response from $method $endpoint (got: $status_code)"
        increment_warning
    fi
}

echo "أ. فحص Endpoints إدارية محتملة"
echo "================================"

# Test for exposed admin endpoints
admin_endpoints=(
    "/admin"
    "/admin/"
    "/api/admin"
    "/admin/users"
    "/dashboard"
    "/management"
    "/config"
    "/settings"
    "/debug"
    "/logs"
    "/status"
    "/metrics"
    "/api/reset"
    "/api/delete"
    "/qdrant/reset"
    "/database/drop"
    "/system/restart"
    "/docs"
    "/redoc" 
    "/openapi.json"
)

for endpoint in "${admin_endpoints[@]}"; do
    test_endpoint "GET" "$endpoint" "404" "Admin endpoint check"
done

echo ""
echo "ب. فحص طرق HTTP مختلفة على Endpoints موجودة"
echo "============================================"

# Test HTTP methods on existing endpoints
existing_endpoints=("/health" "/stats" "/" "/chat" "/upload-curriculum")
http_methods=("GET" "POST" "PUT" "DELETE" "PATCH" "HEAD" "OPTIONS")

for endpoint in "${existing_endpoints[@]}"; do
    echo ""
    echo "Testing endpoint: $endpoint"
    echo "----------------------------"
    
    for method in "${http_methods[@]}"; do
        case "$endpoint:$method" in
            "/health:GET"|"/stats:GET"|"/:GET")
                test_endpoint "$method" "$endpoint" "200" "Expected method"
                ;;
            "/chat:POST"|"/upload-curriculum:POST")
                # These may return 400/422 due to missing data, but should not return 404/405
                increment_test
                status_code=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" \
                    "http://216.81.248.146:8000$endpoint" 2>/dev/null)
                
                if [[ "$status_code" =~ ^[0-9]{3}$ ]]; then
                    if [[ "$status_code" =~ ^(200|400|422|413|429)$ ]]; then
                        log_success "$method $endpoint accepted ($status_code)"
                        increment_passed
                    elif [[ "$status_code" =~ ^(404|405)$ ]]; then
                        log_warning "$method $endpoint blocked ($status_code) - method may not be properly configured"
                        increment_warning
                    else
                        log_info "$method $endpoint returns $status_code"
                        increment_passed
                    fi
                else
                    log_warning "Failed to get response from $method $endpoint (got: $status_code)"
                    increment_warning
                fi
                ;;
            *)
                test_endpoint "$method" "$endpoint" "405" "Unauthorized method"
                ;;
        esac
    done
done

echo ""
echo "=== Section 6.1 Results ==="
echo "Tests run: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS" 
echo "Failed: $FAILED_TESTS"
echo "Warnings: $WARNINGS"
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    log_critical "Section 6.1 FAILED - Critical security issues found!"
    exit 1
elif [ $WARNINGS -gt 3 ]; then
    log_warning "Section 6.1 PASSED with warnings - review needed"
    exit 2
else
    log_success "Section 6.1 PASSED - No critical security issues in access controls"
fi
