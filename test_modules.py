#!/usr/bin/env python3
"""Quick test of enterprise modules"""

from lib_compliance import ComplianceManager, OWASPMapper
from lib_logging import StructuredLogger, PerformanceMetrics

# Test ComplianceManager
comp = ComplianceManager()
print('ComplianceManager initialized')

# Test StructuredLogger
logger = StructuredLogger('test')
print('StructuredLogger initialized')

# Test OWASPMapper
owasp_info = OWASPMapper.get_owasp_info('xss')
print(f'OWASP Info: {owasp_info["owasp"]}')

# Test CVSS
cvss = OWASPMapper.get_cvss_string('xss')
print(f'CVSS Generated: {cvss[:30]}...')

# Test PerformanceMetrics
metrics = PerformanceMetrics()
metrics.record_payload_test()
metrics.record_vulnerability()
summary = metrics.get_summary()
print(f' Metrics: {summary["payloads_tested"]} payload, {summary["vulnerabilities_found"]} vulnerability')

print('\n !All enterprise modules working correctly! ')
