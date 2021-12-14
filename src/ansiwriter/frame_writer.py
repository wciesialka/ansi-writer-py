#!/usr/bin/env python3
'''Module containing the FrameWriter'''

from typing import TextIO, List
from sys import stdout
from copy import deepcopy
from os import linesep
import re

FRAME_SPLIT_REGEX = re.compile(r'(\033\[\d+;?\d*(?:[A-Z]|[a-z]).?|\033[NOP\[\\\]X\^\_].?|.)')

def contains_printable(string: str) -> bool:
    '''Returns true if the string contains at least one printable character.
    
    :param string: String to check.
    :type string: str'''

    return any([char.isprintable() for char in string])

def split_frame_line(line: str) -> List[str]:
    '''Split a line into a row for a frame.'''
    row = [str(group) for group in FRAME_SPLIT_REGEX.findall(line)]

    for i, _ in enumerate(row):
        while not contains_printable(row[i]):
            if i >= len(row)-1:
                break
            row[i] += row.pop(i+1)
            
    if len(row) > 1 and not contains_printable(row[-1]):
        tmp = row.pop(-1)
        row[-1] += tmp

    return row

class FrameWriter:

    '''A class with the primary function of writing frames to a stream.'''

    def __init__(self, width: int, height: int, stream: TextIO = stdout):
        self.__stream: TextIO = stream
        self.__width: int = width
        self.__height: int = height
        self.__last_frame: List[List[str]] = None
        self.__current_frame: List[List[str]] = None

    @property
    def width(self) -> int:
        '''Return the width of the writer.

        :returns: Width of writer.
        :rtype: int'''
        return self.__width

    @property
    def height(self) -> int:
        '''Return the height of the writer.

        :returns: height of writer.
        :rtype: int'''
        return self.__height

    @staticmethod
    def prepare_frame(source: str) -> List[List[str]]:
        '''Prepare a string into a frame.

        :param source: String to convert.
        :type source: str
        :returns: Prepared frame.
        :rtype: list(list(str))'''
        lines = source.split(linesep)
        frame = [split_frame_line(line) for line in lines]
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

    def __find_differences(self) -> List[int]:
        '''Find differences between the writer's current frame and last frame.

        :returns: A list containing the indices of the \
            rightmost change in each row of the current frame.
        :rtype: list(int)'''
        differences = [-1 for _ in range(self.__height)]
        for y, row in enumerate(self.__current_frame):
            for x, char in enumerate(row[::-1]):
                if char != self.__last_frame[y][x]:
                    differences[y] = len(row)-x
                    continue
        return differences


    def write_frame(self, frame: List[List[str]]):
        '''Write a frame to the writer's stream.

        :param frame: Frame to write.
        :type frame: list(list(str))'''

        # Check if frame is a plain string. If it is, prepare it.
        if isinstance(frame, str):
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
                # We newline instead of moving cursor down to ensure there's space for further writes.
                self.__stream.write(linesep)

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

                    for i in range(change+1):
                        str_length_difference = len(self.__last_frame[y][i]) - len(row[i])
                        for _ in range(str_length_difference):
                            # Write a zero-width character to clean out anything left behind.
                            self.__stream.write('\u200b')

                        self.__stream.write(row[i])
                    
                # Move cursor down.
                self.__stream.write('\033[B')
        self.__stream.flush()
