from unittest import TestCase
from project.lib.orm.types import TypeEnum
from enum import IntEnum


class TestTypeEnumConversion(TestCase):

    def setUp(self):
        testing_intenum = IntEnum(
            'Custom IntEnum',
            {
                'val_1': -1,
                'val_2': 10,
                'val_3': 11,
                'val_4': -3,
            },
        )
        self.testing_typeenum = TypeEnum(testing_intenum)

    def test_positive_bind(self):
        for good_value in self.testing_typeenum._enum:
            processed_type = self.testing_typeenum.process_bind_param(
                good_value,
                dialect=None,
            )
            processed_int = self.testing_typeenum.process_bind_param(
                good_value.value,
                dialect=None,
            )
            self.assertEqual(processed_type, good_value.value)
            self.assertEqual(processed_int, good_value.value)

    def test_negative_bind(self):
        bad_value = 0
        # selfcheck:
        self.assertNotIn(
            bad_value,
            self.testing_typeenum._enum.__members__.values(),
            msg="Test selfcheck failed. Please update the test",
        )
        with self.assertRaises(TypeError):
            self.testing_typeenum.process_bind_param(
                bad_value,
                dialect=None,
            )

    def test_none_param(self):
        processed = self.testing_typeenum.process_bind_param(
            None,
            dialect=None,
        )
        self.assertIsNone(processed)
