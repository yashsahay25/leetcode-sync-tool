import unittest
from archiver.config import LANGUAGE_EXTENSIONS


class LanguageExtensionMappingTest(unittest.TestCase):
    def test_known_languages_map_to_expected_extensions(self):
        cases = {
            "cpp": ".cpp",
            "c": ".c",
            "python": ".py",
            "python3": ".py",
            "java": ".java",
            "javascript": ".js",
            "typescript": ".ts",
            "go": ".go",
            "rust": ".rs",
            "mysql": ".sql",
        }
        for lang, expected in cases.items():
            with self.subTest(lang=lang):
                self.assertEqual(LANGUAGE_EXTENSIONS[lang], expected)

    def test_unknown_language_returns_empty_default(self):
        self.assertEqual(LANGUAGE_EXTENSIONS.get("brainfuck", ""), "")

    def test_missing_lang_key_returns_empty_default(self):
        self.assertEqual(LANGUAGE_EXTENSIONS.get(None, ""), "")
        self.assertEqual(LANGUAGE_EXTENSIONS.get("", ""), "")

    def test_languages_that_share_an_extension(self):
        self.assertEqual(LANGUAGE_EXTENSIONS["python"], LANGUAGE_EXTENSIONS["python3"])
        self.assertEqual(LANGUAGE_EXTENSIONS["mysql"], LANGUAGE_EXTENSIONS["mssql"])
        self.assertEqual(LANGUAGE_EXTENSIONS["pandas"], ".py")


if __name__ == "__main__":
    unittest.main()
