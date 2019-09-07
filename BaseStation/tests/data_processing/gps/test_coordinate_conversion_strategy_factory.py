from unittest import TestCase

from src.data_processing.gps.coordinate_conversion_strategy_factory import CoordinateConversionStrategyFactory
from src.data_processing.gps.decimal_degrees_coordinate_conversion_strategy import \
    DecimalDegreesCoordinateConversionStrategy
from src.data_processing.gps.degree_decimal_minutes_coordinate_conversion_strategy import \
    DegreeDecimalMinutesCoordinateConversionStrategy


class CoordinateConversionStrategyFactoryTest(TestCase):
    INVALID_PACKET_VERSION = -1

    def setUp(self):
        self.strategy_factory = CoordinateConversionStrategyFactory()

    def test_create_should_return_decimal_degrees_conversion_strategy_given_2017_version(self):
        strategy = self.strategy_factory.create(2017)

        self.assertIsInstance(strategy, DecimalDegreesCoordinateConversionStrategy)

    def test_create_should_return_decimal_degrees_conversion_strategy_given_2018_version(self):
        strategy = self.strategy_factory.create(2018)

        self.assertIsInstance(strategy, DecimalDegreesCoordinateConversionStrategy)

    def test_create_should_return_degree_decimal_minutes_conversion_strategy_given_2019_version(self):
        strategy = self.strategy_factory.create(2019)

        self.assertIsInstance(strategy, DegreeDecimalMinutesCoordinateConversionStrategy)
