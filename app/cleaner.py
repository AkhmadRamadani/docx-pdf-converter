import os
import time

def auto_cleanup(upload_dir, output_dir, max_age_seconds):
    while True:
        now = time.time()

        for directory in [upload_dir, output_dir]:
            for filename in os.listdir(directory):
                path = os.path.join(directory, filename)
                if os.path.isfile(path):
                    age = now - os.path.getmtime(path)
                    if age > max_age_seconds:
                        try:
                            os.remove(path)
                        except Exception:
                            pass

        time.sleep(60)
