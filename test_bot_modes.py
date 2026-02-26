import unittest
from unittest.mock import MagicMock, patch
from main_bot import (
    cover_letter_mode,
    resume_mode,
    ai_interviewer_mode,
    parser_mode,
    main_menu_handler,
    restart_handler
)
from bots_functions import (
    cover_letter_start,
    resume_bot_start,
    ai_interviewer_start,
    parser_start,
    return_to_main_menu,
    current_mode,
    create_main_menu,
    create_restart_menu,
    create_main_menu_button
)

class TestBotModes(unittest.TestCase):
    def setUp(self):
        self.message = MagicMock()
        self.message.from_user.id = 123
        self.message.chat.id = 123
        self.message.text = "Test message"
        
        # Мокаем все необходимые функции
        self.patchers = [
            patch('bots_functions.bot.send_message'),
            patch('bots_functions.bot.register_next_step_handler'),
            patch('bots_functions.create_main_menu'),
            patch('bots_functions.create_restart_menu'),
            patch('bots_functions.create_main_menu_button')
        ]
        
        for patcher in self.patchers:
            patcher.start()
            
        # Настраиваем возвращаемые значения для моков
        self.mock_send_message = self.patchers[0].start()
        self.mock_register_next_step = self.patchers[1].start()
        self.mock_create_main_menu = self.patchers[2].start()
        self.mock_create_restart_menu = self.patchers[3].start()
        self.mock_create_main_menu_button = self.patchers[4].start()
        
        # Настраиваем возвращаемые значения для моков
        self.mock_create_main_menu.return_value = MagicMock()
        self.mock_create_restart_menu.return_value = MagicMock()
        self.mock_create_main_menu_button.return_value = MagicMock()

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()
        current_mode.clear()

    def reset_mocks(self):
        self.mock_send_message.reset_mock()
        self.mock_register_next_step.reset_mock()
        self.mock_create_main_menu.reset_mock()
        self.mock_create_restart_menu.reset_mock()
        self.mock_create_main_menu_button.reset_mock()

    def test_cover_letter_mode(self):
        cover_letter_mode(self.message)
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_create_restart_menu.assert_not_called()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()
        self.assertEqual(current_mode[123], "cover_letter")

    def test_resume_mode(self):
        resume_mode(self.message)
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_create_restart_menu.assert_not_called()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()
        self.assertEqual(current_mode[123], "resume")

    def test_ai_interviewer_mode(self):
        ai_interviewer_mode(self.message)
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_create_restart_menu.assert_not_called()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()
        self.assertEqual(current_mode[123], "interviewer")

    def test_parser_mode(self):
        parser_mode(self.message)
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_create_restart_menu.assert_not_called()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()
        self.assertEqual(current_mode[123], "parser")

    def test_main_menu_handler(self):
        main_menu_handler(self.message)
        self.mock_create_main_menu.assert_called_once()
        self.mock_send_message.assert_called_once()
        self.assertNotIn(123, current_mode)

    def test_restart_handler(self):
        # Тест для режима сопроводительного письма
        self.reset_mocks()
        current_mode[123] = "cover_letter"
        restart_handler(self.message)
        self.mock_create_restart_menu.assert_not_called()
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()

        # Тест для режима резюме
        self.reset_mocks()
        current_mode[123] = "resume"
        restart_handler(self.message)
        self.mock_create_restart_menu.assert_not_called()
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()

        # Тест для режима AI интервьюера
        self.reset_mocks()
        current_mode[123] = "interviewer"
        restart_handler(self.message)
        self.mock_create_restart_menu.assert_not_called()
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()

        # Тест для режима парсера
        self.reset_mocks()
        current_mode[123] = "parser"
        restart_handler(self.message)
        self.mock_create_restart_menu.assert_not_called()
        self.mock_create_main_menu_button.assert_called_once()
        self.mock_send_message.assert_called_once()
        self.mock_register_next_step.assert_called_once()

        # Тест для неопределенного режима
        self.reset_mocks()
        current_mode[123] = "unknown"
        restart_handler(self.message)
        self.mock_create_main_menu.assert_called_once()
        self.mock_create_restart_menu.assert_not_called()
        self.mock_create_main_menu_button.assert_not_called()
        self.mock_send_message.assert_called_once()

if __name__ == '__main__':
    unittest.main() 