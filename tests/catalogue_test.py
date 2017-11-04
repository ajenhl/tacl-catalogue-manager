from collections import OrderedDict
import os.path
import tempfile
import unittest

from tcm import Catalogue


class CatalogueTestCase (unittest.TestCase):

    def setUp(self):
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self._label1 = os.path.join(self._data_dir, 'group1.txt')
        self._label2 = os.path.join(self._data_dir, 'group2.txt')
        self._label3 = os.path.join(self._data_dir, 'group3.txt')

    def test_add_group_file(self):
        catalogue = Catalogue()
        catalogue.add_group_file(self._label1)
        catalogue.add_group_file(self._label2)
        catalogue.add_group_file(self._label3)
        expected_catalogue = OrderedDict([
            ('T1', 'group1.txt'), ('T2', 'group1.txt'),
            ('T5', 'group1.txt'), ('T3', 'group2.txt'),
            ('T6', 'group2.txt')])
        self.assertEqual(catalogue.data, expected_catalogue)

    def test_add_group_file_report(self):
        catalogue = Catalogue()
        actual_report = catalogue.add_group_file(self._label1)
        expected_report = []
        self.assertEqual(actual_report, expected_report)
        actual_report = catalogue.add_group_file(self._label2)
        expected_report = ['T1 removed from group2.txt']
        self.assertEqual(actual_report, expected_report)
        actual_report = catalogue.add_group_file(self._label3)
        expected_report = [
            'T1 removed from group3.txt',
            'T3 removed from group3.txt',
            'T5 removed from group3.txt',
            'T6 removed from group3.txt'
        ]
        self.assertEqual(actual_report, expected_report)

    def test_save(self):
        catalogue = Catalogue()
        catalogue._data = OrderedDict([
            ('T1', 'group1.txt'), ('T2', 'group1.txt'),
            ('T5', 'group1.txt'), ('T3', 'group2.txt'),
            ('T6', 'group2.txt')
        ])
        mapping = OrderedDict([
            ('group2.txt', 'label1'),
            ('group3.txt', 'label2'),
            ('group1.txt', 'label3')
        ])
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = os.path.join(temp_dir, 'catalogue.txt')
            catalogue.save(save_path, mapping)
            with open(save_path) as fh:
                actual_content = fh.readlines()
        expected_content = [
            'T3 label1\n',
            'T6 label1\n',
            'T1 label3\n',
            'T2 label3\n',
            'T5 label3\n',
        ]
        self.assertEqual(actual_content, expected_content)
