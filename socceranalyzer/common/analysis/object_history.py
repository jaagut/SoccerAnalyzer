from typing import List, Tuple

from enum import Enum

import pandas as pd

from socceranalyzer.common.analysis.abstract_analysis import AbstractAnalysis
from socceranalyzer.utils.logger import Logger


class ObjectHistory(AbstractAnalysis):
    """
        Contains the pose (position and rotation) of the given object
    """
    def __init__(self, dataframe, category: Enum, debug, frame: str, mirror: bool = False, filter=None):
        self.__dataframe = dataframe
        self.__category = category
        self.__frame = frame
        self.__mirror = mirror
        self.__object_pose: Tuple[pd.DataFrame, pd.DataFrame]
        self.__filter = filter

        # Apply filter
        if self.__filter is not None:
            filter_object = self.__filter(dataframe, category, frame)
            self.__dataframe = filter_object.filter()

        try:
            self._analyze()
        except Exception as err:
            Logger.error(f"ObjectHistory failed: {err.args[0]}")
            if debug:
                raise
        else:
            Logger.success(f"ObjectHistory for {frame} has results.")
            
    @property
    def dataframe(self):
        return self.__dataframe

    @property
    def category(self):
        return self.__category

    def _analyze(self):
        mirror_factor = -1 if self.__mirror else 1

        object_positions = pd.DataFrame()
        object_positions["x"] = self.__dataframe[f"{self.__frame}.position.x"] * mirror_factor
        object_positions["y"] = self.__dataframe[f"{self.__frame}.position.y"] * mirror_factor
        object_positions["z"] = self.__dataframe[f"{self.__frame}.position.z"]

        object_rotations = pd.DataFrame()
        if hasattr(self.__dataframe, f"{self.__frame}.rotation.x"):
            object_rotations["x"] = self.__dataframe[f"{self.__frame}.rotation.x"]
            object_rotations["y"] = self.__dataframe[f"{self.__frame}.rotation.y"]
            object_rotations["z"] = self.__dataframe[f"{self.__frame}.rotation.z"]
            object_rotations["w"] = self.__dataframe[f"{self.__frame}.rotation.w"]

        self.__object_pose = (object_positions, object_rotations)

    def describe(self):
        Logger.data("No description available")

    def results(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Pose of the object (position and rotation)

        :return: First element is the position, second is the rotation
        :rtype: Tuple[pd.DataFrame, pd.DataFrame]
        """
        return self.__object_pose

    def serialize(self):
        raise NotImplementedError
