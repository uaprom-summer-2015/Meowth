from unittest import TestCase
from project.lib.orm.types import GUID
from sqlalchemy.types import CHAR
from sqlalchemy.dialects import postgresql
import sqlalchemy.dialects as dialects
import uuid


class TestGUIDConversion(TestCase):

    def setUp(self):
        self.testing_guid = GUID()

    def tearDown(self):
        del self.testing_guid

    def test_load_postgres_impl(self):
        guid = self.testing_guid
        impl = guid.load_dialect_impl(
            dialect=dialects.postgresql.dialect()
        )
        self.assertIsInstance(impl, postgresql.UUID)

    def test_load_other_impl(self):
        guid = self.testing_guid
        impl = guid.load_dialect_impl(
            dialect=dialects.oracle.dialect()
        )
        self.assertIsInstance(impl, CHAR)

    def test_bind_none_param(self):
        guid = self.testing_guid
        processed = guid.process_bind_param(
            value=None,
            dialect=None,
        )
        self.assertIsNone(processed)

    def test_bind_uuid_postgres(self):
        guid = self.testing_guid
        postgres_dialect = dialects.postgresql.dialect()
        param = uuid.uuid4()
        processed = guid.process_bind_param(
            value=param,
            dialect=postgres_dialect,
        )
        self.assertEqual(uuid.UUID(processed), param)

    def test_bind_uuid_other(self):
        guid = self.testing_guid
        other_dialect = dialects.sqlite.dialect()
        param = uuid.uuid4()
        processed = guid.process_bind_param(
            value=param,
            dialect=other_dialect,
        )
        self.assertEqual(processed, param.hex)

    def test_bind_string_other(self):
        guid = self.testing_guid
        other_dialect = dialects.oracle.dialect()
        param = uuid.uuid4()
        processed = guid.process_bind_param(
            value=param.hex,
            dialect=other_dialect,
        )
        self.assertEqual(processed, param.hex)
        processed = guid.process_bind_param(
            value=str(param),
            dialect=other_dialect,
        )
        self.assertEqual(processed, param.hex)

    def test_result_none(self):
        guid = self.testing_guid
        processed = guid.process_result_value(
            value=None,
            dialect=None,
        )
        self.assertIsNone(processed)

    def test_result_string(self):
        guid = self.testing_guid
        param = uuid.uuid4()
        processed = guid.process_result_value(
            value=param.hex,
            dialect=None,
        )
        self.assertEqual(processed, param)
        processed = guid.process_result_value(
            value=str(param),
            dialect=None,
        )
        self.assertEqual(processed, param)
