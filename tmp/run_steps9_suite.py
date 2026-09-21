import os
import subprocess
import sys
from pathlib import Path

environment = {**os.environ, 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1', 'PYTHONIOENCODING': 'utf-8'}
log = Path('tmp/steps9-verified-tests.txt')
with log.open('w', encoding='utf-8') as output:
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_*.py'], env=environment, stdout=output, stderr=subprocess.STDOUT)
for line in log.read_text(encoding='utf-8').splitlines():
    if line.startswith(('Ran ', 'OK', 'FAILED', 'ERROR:', 'FAIL:')):
        print(line)
print('Test process exit code:', result.returncode)
sys.exit(result.returncode)
