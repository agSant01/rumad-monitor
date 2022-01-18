import sys
from pathlib import Path

path = Path(Path.cwd()).parent.absolute()

sys.path.insert(0, str(path))
