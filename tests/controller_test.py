from collections import OrderedDict
import os.path
import tempfile
import unittest

from tcm import Controller


class ControllerTestCase (unittest.TestCase):

    def setUp(self):
        self._data_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'data'))

    def test_generate_catalogues(self):
        controller = Controller()
        controller.load_control(os.path.join(
            self._data_dir, 'control1.txt'))
        with tempfile.TemporaryDirectory() as temp_dir:
            save_dir = os.path.join(temp_dir, 'output')
            controller.generate_catalogues(save_dir)
            with open(os.path.join(save_dir, 'catalogue1.txt')) as fh:
                actual_content1 = fh.readlines()
            with open(os.path.join(save_dir, 'catalogue2.txt')) as fh:
                actual_content2 = fh.readlines()
        expected_content1 = [
            'T3 label1\n',
            'T6 label1\n',
            'T1 label3\n',
            'T2 label3\n',
            'T5 label3\n',
        ]
        expected_content2 = [
            'T1 label2\n',
            'T2 label2\n',
            'T5 label2\n',
            'T3 \n',
            'T6 \n',
        ]
        self.assertEqual(actual_content1, expected_content1)
        self.assertEqual(actual_content2, expected_content2)

    def test_generate_catalogues_report(self):
        controller = Controller()
        controller.load_control(os.path.join(
            self._data_dir, 'control1.txt'))
        with tempfile.TemporaryDirectory() as temp_dir:
            actual_report = controller.generate_catalogues(temp_dir)
        expected_report = [
            'T1 removed from group2.txt',
            'T1 removed from group3.txt',
            'T3 removed from group3.txt',
            'T5 removed from group3.txt',
            'T6 removed from group3.txt'
        ]
        self.assertEqual(actual_report, expected_report)

    def test_load_control_base_path(self):
        controller = Controller()
        controller.load_control(os.path.join(
            self._data_dir, 'control1.txt'))
        expected_base_path = self._data_dir
        self.assertEqual(controller.base_path, expected_base_path)

    def test_load_control_groups(self):
        controller = Controller()
        controller.load_control(os.path.join(
            self._data_dir, 'control1.txt'))
        expected_groups_path = 'groups1.txt'
        self.assertEqual(controller.groups_path, expected_groups_path)

    def test_load_control_mappings(self):
        controller = Controller()
        controller.load_control(os.path.join(
            self._data_dir, 'control1.txt'))
        expected_mappings = [('mapping1.txt', 'catalogue1.txt'),
                             ('mapping2.txt', 'catalogue2.txt')]
        self.assertEqual(controller.mappings, expected_mappings)

    def test_load_mapping(self):
        controller = Controller()
        actual_mapping = controller.load_mapping(os.path.join(
            self._data_dir, 'mapping1.txt'))
        expected_mapping = OrderedDict([
            ('group2.txt', 'label1'),
            ('group3.txt', 'label2'),
            ('group1.txt', 'label3')
        ])
        self.assertEqual(actual_mapping, expected_mapping)

    def test_load_mapping_blank(self):
        controller = Controller()
        actual_mapping = controller.load_mapping(os.path.join(
            self._data_dir, 'mapping2.txt'))
        expected_mapping = OrderedDict([
            ('group3.txt', 'label1'),
            ('group1.txt', 'label2'),
            ('group2.txt', ''),
        ])
        self.assertEqual(actual_mapping, expected_mapping)

    def test_load_groups(self):
        controller = Controller()
        actual_groups = controller.load_groups(os.path.join(
            self._data_dir, 'groups1.txt'))
        expected_groups = ['group1.txt', 'group2.txt', 'group3.txt']
        self.assertEqual(actual_groups, expected_groups)
