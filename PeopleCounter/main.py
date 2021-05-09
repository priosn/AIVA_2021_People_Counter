import argparse
from PeopleCounterLib import *

parser = argparse.ArgumentParser()
parser.add_argument("--input_video", required=True, help="Ruta del video de entrada")
args = parser.parse_args()

in_path = args.input_video
video_bool = False

name = os.path.split(in_path)

counter = PeopleCounterLib()
counter.compute(path_video=in_path, showvideo=video_bool)

print(f"\n El resultado del video {name[1]} es:")
print(counter.lastReport())
