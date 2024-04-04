import pandas as pd

from socceranalyzer.utils.logger import Logger
from socceranalyzer.common.enums.hl_kid import HLKid


class FilterSelfLocalizationCovariance():
    def __init__(self, df: pd.DataFrame, category, localization_prefix: str, x_sdev_threshold=0.5, y_sdev_threshold=0.5, theta_sdev_threshold=0.6):
        self.df = df
        self.category = category
        self.localization_prefix = localization_prefix
        print(self.localization_prefix)
        self.x_sdev_threshold = x_sdev_threshold
        self.y_sdev_threshold = y_sdev_threshold
        self.theta_sdev_threshold = theta_sdev_threshold

        if self.category is not HLKid:
            raise NotImplementedError


    def filter(self):
        """Filter the dataframe to only contain the player of interest"""
        # Return dataframe with all columns prefixed with the player
        if self.category is HLKid:
            # Filter out all rows where the standard deviation of the x, y and theta is too high
            x_sdev = self.df[f"{self.localization_prefix}.covariance.0"]
            y_sdev = self.df[f"{self.localization_prefix}.covariance.4"]
            theta_sdev = self.df[f"{self.localization_prefix}.covariance.8"]

            # Set self localization x, y, z to not a number if the standard deviation is too high for any dimension
            localization_covariance_is_too_bad = (x_sdev > self.x_sdev_threshold) | (y_sdev > self.y_sdev_threshold) | (theta_sdev > self.theta_sdev_threshold)
            self.df.loc[localization_covariance_is_too_bad, f"{self.localization_prefix}.position.x"] = float('nan')
            self.df.loc[localization_covariance_is_too_bad, f"{self.localization_prefix}.position.y"] = float('nan')
            self.df.loc[localization_covariance_is_too_bad, f"{self.localization_prefix}.position.z"] = float('nan')

            return self.df
        else:
            raise NotImplementedError


class FilterBallCovariance():
    def __init__(self, df: pd.DataFrame, category, localization_prefix: str, x_sdev_threshold=0.5, y_sdev_threshold=0.5):
        self.df = df
        self.category = category
        self.localization_prefix = localization_prefix
        self.x_sdev_threshold = x_sdev_threshold
        self.y_sdev_threshold = y_sdev_threshold

        if self.category is not HLKid:
            raise NotImplementedError


    def filter(self):
        """Filter the dataframe to only contain the player of interest"""
        # Return dataframe with all columns prefixed with the player
        if self.category is HLKid:
            # Filter out all rows where the standard deviation of the x, y and theta is too high
            x_sdev = self.df[f"{self.localization_prefix}.covariance.0"]
            y_sdev = self.df[f"{self.localization_prefix}.covariance.4"]

            # Set ball detection x, y, z to not a number if the standard deviation is too high for any dimension
            ball_covariance_is_too_bad = (x_sdev > self.x_sdev_threshold) | (y_sdev > self.y_sdev_threshold)
            self.df.loc[ball_covariance_is_too_bad, f"{self.localization_prefix}.position.x"] = float('nan')
            self.df.loc[ball_covariance_is_too_bad, f"{self.localization_prefix}.position.y"] = float('nan')
            self.df.loc[ball_covariance_is_too_bad, f"{self.localization_prefix}.position.z"] = float('nan')

            return self.df
        else:
            raise NotImplementedError
