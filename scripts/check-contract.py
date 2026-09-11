"""Run official GenLayer tools with a project-local SDK cache on Windows."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'work' / 'genvm-cache'
CACHE.mkdir(parents=True, exist_ok=True)
import genvm_linter.validate.artifacts as artifacts
artifacts.CACHE_DIR = CACHE
if sys.argv[1] == 'lint':
    from genvm_linter.cli import main
    main(args=['check',str(ROOT/'contracts/fairdrop.py'),'--json'])
elif sys.argv[1] == 'test':
    import subprocess
    raise SystemExit(subprocess.call([sys.executable, '-X', 'utf8', str(ROOT/'scripts/test-contract-isolated.py')]))
elif sys.argv[1] in ['single', 'collect']:
    import gltest.direct.sdk_loader as loader
    loader.CACHE_DIR = CACHE
    # Upstream unlinks the temporary stdin file while fd 0 still holds it.
    # Unix permits this; Windows does not. Defer only that cleanup, leaving
    # the official message encoding, fd injection and execution unchanged.
    import os
    import atexit
    if os.name == 'nt':
        import gltest.direct.loader as contract_loader
        original_inject = contract_loader._inject_message_to_fd0
        deferred = []
        def inject_windows(vm):
            try:
                original_inject(vm)
            except PermissionError as error:
                if error.winerror != 32 or not error.filename:
                    raise
                deferred.append(error.filename)
        def cleanup():
            for filename in deferred:
                try:
                    os.unlink(filename)
                except (FileNotFoundError, PermissionError):
                    pass
        contract_loader._inject_message_to_fd0 = inject_windows
        atexit.register(cleanup)
    import pytest
    args = ['tests/test_fairdrop.py','--collect-only','-q'] if sys.argv[1]=='collect' else [sys.argv[2],'-q','--tb=short',*sys.argv[3:]]
    raise SystemExit(pytest.main(args))
