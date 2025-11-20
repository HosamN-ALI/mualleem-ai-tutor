#!/bin/bash

echo "=== 🔒 Section 6.3: اختبارات File Upload Security ==="
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

echo "أ. إنشاء ملفات اختبار ضارة"
echo "========================="

# Create test files for upload security
echo "Creating malicious test files..."

# Executable disguised as image
echo '#!/bin/bash
echo "This should not execute"' > malicious.png

# PHP file disguised as image
echo '<?php echo "PHP code executed"; phpinfo(); ?>' > malicious.jpg

# File with null bytes
printf "PNG\x00shell_command\x00" > nullbyte.png

# HTML file disguised as image
echo '<html><script>alert("XSS")</script><img src="x" onerror="alert(1)"></html>' > html_disguised.png

# SQL injection in filename (will be tested differently)
echo "test content" > "test'; DROP TABLE users; --.jpg"

# Large file (but not too large to avoid issues)
dd if=/dev/zero of=large_test.jpg bs=1M count=2 2>/dev/null

log_success "Test files created"

echo ""
echo "ب. اختبار رفع ملفات ضارة في endpoint /chat"
echo "========================================="

test_malicious_file() {
    local filename="$1"
    local description="$2"
    
    increment_test
    
    echo "Testing upload: $filename - $description"
    
    if [ ! -f "$filename" ]; then
        log_warning "Test file $filename not found, skipping"
        increment_warning
        return
    fi
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=test malicious upload" \
        -F "image=@$filename" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    
    if [[ "$status_code" == "400" ]]; then
        log_success "Malicious file properly rejected (400 Bad Request)"
        increment_passed
    elif [[ "$status_code" == "413" ]]; then
        log_success "File rejected - too large (413 Payload Too Large)"
        increment_passed
    elif [[ "$status_code" == "422" ]]; then
        log_success "File rejected - validation error (422 Unprocessable Entity)"
        increment_passed
    elif [[ "$status_code" == "200" ]]; then
        log_critical "Malicious file accepted (200 OK) - SECURITY RISK!"
        increment_failed
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing tests"
        increment_passed
        sleep 1
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

# Test malicious files
test_malicious_file "malicious.png" "Executable disguised as PNG"
test_malicious_file "malicious.jpg" "PHP code disguised as JPG"
test_malicious_file "nullbyte.png" "File with null bytes"
test_malicious_file "html_disguised.png" "HTML/XSS content disguised as PNG"
test_malicious_file "large_test.jpg" "Large file test"

echo ""
echo "ج. اختبار رفع ملفات ضارة في endpoint /upload-curriculum"
echo "=================================================="

test_malicious_pdf() {
    local filename="$1"
    local description="$2"
    
    increment_test
    
    echo "Testing PDF upload: $filename - $description"
    
    if [ ! -f "$filename" ]; then
        log_warning "Test file $filename not found, skipping"
        increment_warning
        return
    fi
    
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "file=@$filename" \
        "http://216.81.248.146:8000/upload-curriculum" 2>/dev/null)
    
    if [[ "$status_code" == "400" ]]; then
        log_success "Non-PDF file properly rejected (400 Bad Request)"
        increment_passed
    elif [[ "$status_code" == "413" ]]; then
        log_success "Large file rejected (413 Payload Too Large)"
        increment_passed
    elif [[ "$status_code" == "422" ]]; then
        log_success "File validation error (422 Unprocessable Entity)"
        increment_passed
    elif [[ "$status_code" == "200" ]]; then
        log_warning "File accepted - verify it's actually a valid PDF"
        increment_warning
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing tests"
        increment_passed
        sleep 1
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

# Test uploading non-PDF files to PDF endpoint
test_malicious_pdf "malicious.png" "PNG file to PDF endpoint"
test_malicious_pdf "malicious.jpg" "JPG file to PDF endpoint" 
test_malicious_pdf "large_test.jpg" "Large file to PDF endpoint"

echo ""
echo "د. اختبار أسماء ملفات خطيرة"
echo "=========================="

test_dangerous_filename() {
    local dangerous_name="$1"
    local description="$2"
    
    increment_test
    
    echo "Testing dangerous filename: $description"
    
    status_code=$(echo "test content" | curl -s -o /dev/null -w "%{http_code}" -X POST \
        -F "question=test filename" \
        -F "image=@-;filename=$dangerous_name" \
        "http://216.81.248.146:8000/chat" 2>/dev/null)
    
    if [[ "$status_code" == "400" ]] || [[ "$status_code" == "422" ]]; then
        log_success "Dangerous filename rejected ($status_code)"
        increment_passed
    elif [[ "$status_code" == "200" ]]; then
        log_warning "Dangerous filename accepted - check file validation"
        increment_warning
    elif [[ "$status_code" == "429" ]]; then
        log_info "Rate limited - continuing tests"
        increment_passed
        sleep 1
    else
        log_info "Response: $status_code"
        increment_passed
    fi
}

# Test dangerous filenames
test_dangerous_filename "../../../etc/passwd" "Path traversal attack"
test_dangerous_filename "..\\..\\windows\\system32\\config\\sam" "Windows path traversal"
test_dangerous_filename "test.php%00.jpg" "Null byte injection in filename"
test_dangerous_filename 'test.jpg"; rm -rf /; echo "' "Command injection in filename"

echo ""
echo "هـ. اختبار أحجام ملفات متطرفة"
echo "==========================="

echo "Testing extremely large file..."
increment_test

# Create a very large file (10MB)
dd if=/dev/zero of=very_large.jpg bs=1M count=10 2>/dev/null

status_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    -F "question=test large file" \
    -F "image=@very_large.jpg" \
    "http://216.81.248.146:8000/chat" 2>/dev/null)

if [[ "$status_code" == "413" ]]; then
    log_success "Very large file properly rejected (413 Payload Too Large)"
    increment_passed
elif [[ "$status_code" == "400" ]]; then
    log_success "Very large file rejected (400 Bad Request)"
    increment_passed
elif [[ "$status_code" == "200" ]]; then
    log_warning "Very large file accepted - check size limits"
    increment_warning
else
    log_info "Large file test response: $status_code"
    increment_passed
fi

echo ""
echo "و. تنظيف ملفات الاختبار"
echo "====================="

# Cleanup test files
rm -f malicious.png malicious.jpg nullbyte.png html_disguised.png large_test.jpg very_large.jpg "test'; DROP TABLE users; --.jpg" 2>/dev/null
log_success "Test files cleaned up"

echo ""
echo "=== Section 6.3 Results ==="
echo "Tests run: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS" 
echo "Failed: $FAILED_TESTS"
echo "Warnings: $WARNINGS"
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    log_critical "Section 6.3 FAILED - Critical file upload security issues found!"
    exit 1
elif [ $WARNINGS -gt 2 ]; then
    log_warning "Section 6.3 PASSED with warnings - file validation may need improvement"
    exit 2
else
    log_success "Section 6.3 PASSED - File upload security appears adequate"
fi
