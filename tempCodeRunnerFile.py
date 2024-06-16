import os

stage_file = os.path.join(os.path.dirname(__file__), "assets/stage.txt")
with open(stage_file) as f:
    s = f.readline(-10).rstrip().split()
    print(s)
