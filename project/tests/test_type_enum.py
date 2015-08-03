from unittest import TestCase
from project.lib.orm.types import TypeEnum
from random import randint
from enum import IntEnum

MAXINT = 2**4
MININT = -MAXINT - 1


class TestTypeEnumConversion(TestCase):

    def setUp(self):
        self.testing_intenum = IntEnum(
            'Custom IntEnum',
            {
                'val_1': -1,
                'val_2': 10,
                'val_3': 11,
                'val_4': -3,
            },
        )

    def positive_bind_test(self, *, typeenum):
        te = typeenum
        for val in te._enum:
            processed_type = te.process_bind_param(
                val,
                dialect=None,
            )
            processed_int = te.process_bind_param(
                val.value,
                dialect=None,
            )
            self.assertEqual(processed_type, val.value)
            self.assertEqual(processed_int, val.value)

    def negative_bind_test(self, *, typeenum):
        te = typeenum  # alias
        while True:
            v = randint(MININT, MAXINT)
            if v not in te._enum.__members__.values():
                break
        with self.assertRaises(TypeError):
            te.process_bind_param(
                v,
                dialect=None,
            )

    def test_positive_custom(self):
        ie = self.testing_intenum
        te = TypeEnum(ie)
        self.positive_bind_test(
            typeenum=te,
        )

    def test_negative_custom(self):
        ie = self.testing_intenum
        te = TypeEnum(ie)
        self.negative_bind_test(
            typeenum=te,
        )

    def test_none_param(self):
        ie = self.testing_intenum
        te = TypeEnum(ie)
        processed = te.process_bind_param(
            None,
            dialect=None,
        )
        self.assertIsNone(processed)
