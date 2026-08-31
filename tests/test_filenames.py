import unittest
from archiver.config import LANGUAGE_EXTENSIONS


class FilenameResolutionTest(unittest.TestCase):
    def build_filename(self, frontend_id, slug, submission_id, sub):
        extension = LANGUAGE_EXTENSIONS.get(sub.get("lang", ""), ".txt")
        return f"{int(frontend_id):05d}_{slug}_{submission_id}{extension}"

    def test_python_submission_gets_py_extension(self):
        name = self.build_filename(1, "two-sum", 999, {"lang": "python3"})
        self.assertEqual(name, "00001_two-sum_999.py")

    def test_cpp_submission_gets_cpp_extension(self):
        name = self.build_filename(42, "trapping-rain-water", 123, {"lang": "cpp"})
        self.assertEqual(name, "00042_trapping-rain-water_123.cpp")

    def test_unknown_lang_falls_back_to_txt(self):
        name = self.build_filename(7, "reverse-integer", 55, {"lang": "unknownlang"})
        self.assertEqual(name, "00007_reverse-integer_55.txt")

    def test_missing_lang_falls_back_to_txt(self):
        name = self.build_filename(7, "reverse-integer", 55, {})
        self.assertEqual(name, "00007_reverse-integer_55.txt")

    def test_frontend_id_is_zero_padded(self):
        name = self.build_filename(1234, "some-problem", 1, {"lang": "java"})
        self.assertEqual(name, "01234_some-problem_1.java")


if __name__ == "__main__":
    unittest.main()
