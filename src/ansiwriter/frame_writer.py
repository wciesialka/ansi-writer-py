'''Module containing the FrameWriter'''

from typing import TextIO, List
from sys import stdout
from copy import deepcopy
from os import linesep

class FrameWriter:

    '''A class with the primary function of writing frames to a stream.'''

    def __init__(self, width: int, height: int, stream: TextIO = stdout):
        self.__stream = stream
        self.__width = width
        self.__height = height
        self.__last_frame = None
        self.__current_frame = None

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @staticmethod
    def prepare_frame(source: str) -> List[List[str]]:
        '''Prepare a string into a frame.

        :param source: String to convert.
        :type source: str
        :returns: Prepared frame.
        :rtype: list(list(str))'''
        lines = source.split(linesep)
        frame = [list(line) for line in lines]
        return frame

    def __check_frame_size(self, frame: List[List[str]]) -> bool:
        '''Check the size of the frame, width * height.

        :param frame: Incoming frame to check.
        :type frame: list(list(str))

        :returns: True if size fits writer, false otherwise.
        :rtype: bool'''
        if len(frame) == self.__height:
            for line in frame:
                if len(line) != self.__width:
                    return False
            return True
        return False

    def __find_differences(self):
        differences = [-1 for _ in range(self.__height)]
        for y, row in enumerate(self.__current_frame):
            for x, char in enumerate(self.__current_frame):
                    if char != self.__last_frame[y][x]:
                        differences[y] = x
        return differences


    def write_frame(self, frame: List[List[str]]):
        '''Write a frame to the writer's stream.

        :param frame: Frame to write.
        :type frame: list(list(str))'''

        # Check if frame is a plain string. If it is, prepare it.
        if(isinstance(frame,str)):
            frame = FrameWriter.prepare_frame(frame)

        # Check size of frame.
        if not self.__check_frame_size(frame):
            raise ValueError("Frame does not match size of FrameWriter.")

        self.__last_frame = None if self.__current_frame is None else deepcopy(self.__current_frame)
        self.__current_frame = deepcopy(frame)

        # Handle initial frame
        if self.__last_frame is None:
            for line in self.__current_frame:
                # Set horizontal position to 1.
                self.__stream.write('\033[G')
                for char in line:
                    self.__stream.write(char)
                # Move cursor down
                self.__stream.write('\033[B')

        else:
            # Move up
            for _ in range(self.height):
                self.__stream.write('\033[A')
            changes = self.__find_differences()
            for y, row in enumerate(self.__current_frame):
                # Set horizontal position to 1.
                self.__stream.write('\033[G')
                change = changes[y]
                if change > -1:
                    for i in range(change):
                        self.__stream.write(row[i])
                # Move cursor down.
                self.__stream.write('\033[B')
        self.__stream.flush()
                    


    