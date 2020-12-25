import unittest

from prime_numbers.viewmodel.prime_numbers_viewmodel import PrimeNumberViewModel


class TestPrimeNumbersViewModel(unittest.TestCase):
    def test_by_default_button_is_disable(self):
        model = PrimeNumberViewModel()
        self.assertEqual('disabled', model.is_button_enable())

    def test_when_enter_both_number_button_enabled(self):
        model = PrimeNumberViewModel(1, 10)
        self.assertTrue(model.is_button_enable())

    def test_when_clear_first_number_button_disabled(self):
        model = PrimeNumberViewModel(1, 10)
        model.set_start_value(None)

        self.assertEqual('disabled', model.is_button_enable())

    def test_when_clear_second_number_button_disabled(self):
        model = PrimeNumberViewModel(1, 10)
        model.set_end_value(None)

        self.assertEqual('disabled', model.is_button_enable())

    def test_when_enter_values_display_corrected_list(self):
        model = PrimeNumberViewModel(1, 10)
        model.perform()
        answer = [2, 3, 5, 7]

        self.assertEqual(answer, model.get_result())

    def test_when_enter_incorrect_values(self):
        model = PrimeNumberViewModel('asd', '11a')
        self.assertEqual('disabled', model.is_button_enable())

    def test_when_first_value_is_bigger_than_second(self):
        model = PrimeNumberViewModel(10, 1)
        model.perform()
        error_message = 'Что-то пошло не так.\nВозможно первое число оказалось больше второго'
        self.assertEqual(error_message, model.get_error_message())
        self.assertIsNone(model.get_result())

    def test_correct_set_value(self):
        model = PrimeNumberViewModel()
        model.set_start_value(1)
        model.set_end_value(10)

        self.assertEqual(1, model.get_start_value())
        self.assertEqual(10, model.get_end_value())

    def test_get_interval(self):
        model = PrimeNumberViewModel(1, 10)
        model.perform()

        self.assertEqual('range(1, 10)', model.get_interval_label())

    def test_get_interval_if_no_values(self):
        model = PrimeNumberViewModel()
        model.perform()

        self.assertEqual('', model.get_interval_label())


class TestViewModelLogger(unittest.TestCase):
    def test_init_logging(self):
        model = PrimeNumberViewModel(1, 10)
        self.assertEqual('Welcome!', model.logger.get_last_message())

    def test_set_start_value_logging(self):
        model = PrimeNumberViewModel()
        model.set_start_value(2)
        self.assertEqual('Setting start value - 2', model.logger.get_last_message())

    def test_set_end_value_logging(self):
        model = PrimeNumberViewModel()
        model.set_end_value(10)
        self.assertEqual('Setting end value - 10', model.logger.get_last_message())

    def test_model_perform_logging(self):
        model = PrimeNumberViewModel()
        model.set_start_value(2)
        model.set_end_value(10)
        model.perform()
        self.assertEqual('Result = [2, 3, 5, 7]', model.logger.get_last_message())

    def test_model_perform_all_message_logging(self):
        model = PrimeNumberViewModel()
        model.set_start_value(2)
        model.set_end_value(10)
        model.perform()

        log_message = ['Welcome!', 'Setting start value - 2',
                       'Setting end value - 10', 'Button clicked',
                       'Interval = range(2, 10)', 'Result = [2, 3, 5, 7]']
        self.assertEqual(log_message, model.logger.get_log_messages()[-6:])

    def test_input_wrong_data(self):
        model = PrimeNumberViewModel()
        model.set_start_value(10)
        model.set_end_value(2)
        model.perform()

        wrong_message = 'Что-то пошло не так.\nВозможно первое число оказалось больше второго'
        self.assertEqual(wrong_message, model.logger.get_last_message())
