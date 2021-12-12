'''Main module.'''

from time import sleep
from ansiwriter.frame_writer import FrameWriter

def main():
    '''Displays a test animation.'''
    writer = FrameWriter(3, 3)
    frames = []
    frames.append("   \n   \n   ")
    frames.append("   \n   \n . ")
    frames.append("   \n . \n   ")
    frames.append(" . \n   \n   ")
    frames.append("   \n   \n   ")
    frames.append(" * \n   \n   ")
    for frame in frames:
        writer.write_frame(frame)
        sleep(0.33)

if __name__ == "__main__":
    main()
