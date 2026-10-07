import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("JWT_SECRET", "test-jwt-secret-32chars-minimum!!")
os.environ.setdefault("SUBJECT_PEPPER", "week9-capstone-pepper-for-fixtures-only")
