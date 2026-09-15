import os
import subprocess
import sys
from pathlib import Path

environment = {**os.environ, 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1', 'PYTHONIOENCODING': 'utf-8'}
with Path('tmp/test-results-verified.txt').open('w', encoding='utf-8') as log:
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'], env=environment, stdout=log, stderr=subprocess.STDOUT)
print('Python test process exit code:', result.returncode)
for line in Path('tmp/test-results-verified.txt').read_text(encoding='utf-8').splitlines():
    if line.startswith(('Ran ', 'OK', 'FAILED')):
        print(line)
sys.exit(result.returncode)
