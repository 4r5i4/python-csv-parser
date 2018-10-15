import unittest
import arsia_parser


class TestParser(unittest.TestCase):
    """
    Test functions in parser.py
    """

    def test_order_of_columns(self):
        """testing placement of columns, should return sorted"""
        data = [
            {'make': 'Boeing', 'year': '2016', 'model': 'XF-1', 'stat': 'KIA'},
            {'make': 'Boeing', 'year': '1979', 'model': '747', 'stat': 'MIA'},
            {'make': 'Boeing', 'year': '1983', 'model': '747-AFA', 'stat': 'KIA'}
        ]
        expected = [
            {'make': 'Boeing', 'year': '1979', 'model': '747', 'stat': 'MIA'},
            {'make': 'Boeing', 'year': '1983', 'model': '747-AFA', 'stat': 'KIA'},
            {'make': 'Boeing', 'year': '2016', 'model': 'XF-1', 'stat': 'KIA'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['make', 'year', 'model'])

        self.assertCountEqual(result, expected)

    def test_sortability_based_on_number_of_columns(self):
        """testing number of columns, should return unsorted"""
        data = [
            {'make': 'Boeing', 'year': '2016'},
            {'make': 'Boeing', 'year': '1979'},
            {'make': 'Boeing', 'year': '1983'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['make', 'year'])

        self.assertCountEqual(result, data)

    def test_sortability_if_have_correct_columns(self):
        """testing if columns are sortable based on names [year, make, model], should be returned unsorted"""
        data = [
            {'name': 'Mike Tyson', 'year': '1987', 'studentid': '133313'},
            {'name': 'Habib Johnson ', 'year': '2017', 'studentid': '0901182713'},
            {'name': 'Arsia Ardalan', 'year': '1819', 'studentid': '313123'},
            {'name': 'John Marston', 'year': '1811', 'studentid': '99'},
            {'name': 'Mitch', 'year': '2012', 'studentid': '129929'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['name', 'year', 'studentid'])

        self.assertCountEqual(result, data)

    def test_sorting_one(self):
        """testing if sorting works, should be returned sorted"""
        data = [
            {'make': 'BMW', 'year': '2006', 'model': '335i'},
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': 'BMW', 'year': '2006', 'model': 'M3'},
            {'make': 'BMW', 'year': '2006', 'model': 'M5'}
        ]
        expected = [
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': 'BMW', 'year': '2006', 'model': '335i'},
            {'make': 'BMW', 'year': '2006', 'model': 'M3'},
            {'make': 'BMW', 'year': '2006', 'model': 'M5'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['make', 'year', 'model'])

        self.assertCountEqual(result, expected)

    def test_sorting_two(self):
        """testing if sorting works, should be returned sorted"""
        data = [
            {'make': 'BMW', 'year': '2013', 'model': '335i'},
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': 'BMW', 'year': '2001', 'model': 'M3'},
            {'make': 'Audi', 'year': '2008', 'model': 'S5'},
            {'make': 'Audi', 'year': '2008', 'model': 'SR5'},
            {'make': 'Audi', 'year': '2008', 'model': 'R8'},
            {'make': 'Porche', 'year': '1998', 'model': 'Carrera 4s'}
        ]
        expected = [
            {'make': 'Porche', 'year': '1998', 'model': 'Carrera 4s'},
            {'make': 'BMW', 'year': '2001', 'model': 'M3'},
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': 'Audi', 'year': '2008', 'model': 'R8'},
            {'make': 'Audi', 'year': '2008', 'model': 'S5'},
            {'make': 'Audi', 'year': '2008', 'model': 'SR5'},
            {'make': 'BMW', 'year': '2013', 'model': '335i'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['make', 'year', 'model'])

        self.assertCountEqual(result, expected)

    def test_for_missing_values(self):
        """testing if sorting works for missing values, should be returned sorted"""
        data = [
            {'make': 'BMW', 'year': '', 'model': '335i'},
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': 'BMW', 'year': '2001', 'model': 'M3'},
            {'make': '', 'year': '2008', 'model': ''},
            {'make': 'Audi', 'year': '2008', 'model': 'SR5'},
            {'make': 'Audi', 'year': '', 'model': 'R8'},
            {'make': 'Porche', 'year': '1998', 'model': ''}
        ]

        expected = [
            {'make': 'Audi', 'year': '', 'model': 'R8'},
            {'make': 'BMW', 'year': '', 'model': '335i'},
            {'make': 'Porche', 'year': '1998', 'model': ''},
            {'make': 'BMW', 'year': '2001', 'model': 'M3'},
            {'make': 'BMW', 'year': '2006', 'model': '325i'},
            {'make': '', 'year': '2008', 'model': ''},
            {'make': 'Audi', 'year': '2008', 'model': 'SR5'}
        ]

        result = arsia_parser._sort_date_make_model(
            './dir/path', data, ['make', 'year', 'model'])

        self.assertCountEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
