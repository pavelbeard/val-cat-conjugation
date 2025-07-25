import sys
import os

# Add apps/backend to sys.path so that top-level 'src' package can be imported || OK
current_dir = os.path.dirname(__file__)
# Go up two levels: tests/.. => src, then src/.. => backend || OK
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# IT'S IMPORTANT TO NOTE THAT MODIFYING sys.path IS A HACKY SOLUTION FOR MONOREPO STRUCTURE