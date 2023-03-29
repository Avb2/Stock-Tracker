import threading
from functions.buildPage import build_page

lock = threading.Lock()

build_page(lock)
