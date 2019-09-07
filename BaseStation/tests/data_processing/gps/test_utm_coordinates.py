from unittest import TestCase

from src.data_processing.gps.utm_coordinates import UTMCoordinates


class UTMCoordinatesTest(TestCase):

    def setUp(self):
        self.utm_coordinates = UTMCoordinates(3, 4)
        self.utm_coordinates_operand = UTMCoordinates(1, 2)
        self.operand_of_other_type = (3, 4)

    def test_add_should_add_coordinates_component_wise_given_utm_coordinates_operand(self):
        resulting_coordinates = self.utm_coordinates + self.utm_coordinates_operand

        self.assertEqual(resulting_coordinates, UTMCoordinates(4, 6))

    def test_add_should_raise_type_error_given_operand_of_a_different_type(self):
        with self.assertRaises(TypeError):
            self.utm_coordinates + self.operand_of_other_type

    def test_subtract_should_subtract_coordinates_component_wise_given_utm_coordinates_operand(self):
        resulting_coordinates = self.utm_coordinates - self.utm_coordinates_operand

        self.assertEqual(resulting_coordinates, UTMCoordinates(2, 2))

    def test_subtract_should_raise_type_error_given_operand_of_a_different_type(self):
        with self.assertRaises(TypeError):
            self.utm_coordinates - self.operand_of_other_type

    def test_divide_should_divide_coordinates_component_wise_given_numerical_operand(self):
        resulting_coordinates = self.utm_coordinates / 2

        self.assertEqual(resulting_coordinates, UTMCoordinates(1.5, 2))

    def test_divide_should_raise_type_error_given_non_numerical_operand(self):
        with self.assertRaises(TypeError):
            self.utm_coordinates / self.utm_coordinates_operand
