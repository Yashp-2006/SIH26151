import sys
from pathlib import Path

# Ensure backend root is in sys.path so 'pramana' package is discoverable
sys.path.insert(0, str(Path(__file__).parent))
