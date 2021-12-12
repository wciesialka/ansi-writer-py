'''Main module.'''

from ansiwriter.frame_writer import FrameWriter
from time import sleep

def main():
    writer = FrameWriter(3, 3) 
    frames = [] 
    frames.append( "   \n   \n   " )
    frames.append( "   \n   \n . " )
    frames.append( "   \n . \n   " )
    frames.append( " . \n   \n   " )
    frames.append( "   \n   \n   " )
    frames.append( " * \n   \n   " )
    for frame in frames:
        writer.write_frame(frame)
        sleep(0.33)
    

if __name__ == "__main__":
    main()