import threading
from newFunctions.buildPage import build_page

lock = threading.Lock()

build_page(lock)
