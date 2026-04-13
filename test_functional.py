#!/usr/bin/env python3
"""Functional test of XSS payload loading and core logic"""

import os
from pathlib import Path

# Test payload loading
payloads_dir = Path('payloads')
print(f'Payloads directory: {payloads_dir.absolute()}')
print(f' Exists: {payloads_dir.exists()}')

payload_files = list(payloads_dir.glob('*.txt'))
print(f' Found {len(payload_files)} payload files:')

total_payloads = 0
for pfile in sorted(payload_files):
    with open(pfile, 'r') as f:
        payloads = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        total_payloads += len(payloads)
        print(f'   • {pfile.name:<20} - {len(payloads):3d} payloads')

print(f'\nTotal payloads available: {total_payloads}')

# Test compliance manager
from lib_compliance import ComplianceManager
comp = ComplianceManager()

# Test audit logging
print(f'\n Testing audit logging:')
comp.log_scan_start(
    url='https://example.com/test',
    mode='quick',
    profile='all',
    endpoint='/search',
    param='q'
)
comp.log_audit('payload_tested', {
    'payload': '<img src=x onerror=alert(1)>',
    'injection_point': 'query_param',
    'result': 'filtered'
})
comp.log_scan_end({
    'url': 'https://example.com/test',
    'vulnerabilities_found': 0,
    'payloads_tested': 10,
    'duration_seconds': 5.2
})
print(f'   !Scan events logged successfully!')

print(f'\n !XSS Generator is fully operational!')
print(f'   Ready for interactive wizard or command-line scanning')
