import unittest
from functions.file_info import get_files_info
from functions.file_info import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

class TestFunctions(unittest.TestCase):
    def test_get_files_info(self):
        print(get_files_info("calculator", "."))
        print(get_files_info("calculator", "pkg"))
        print(get_files_info("calculator", "bin"))
        print(get_files_info("calculator", "../"))
        self.assertTrue(
            all(
                substring in get_files_info(
                    "calculator",
                    "."
                    ) for substring in ["current", "main.py", "tests.py", "pkg", "file_size", "is_dir"]
            )
        )

        self.assertTrue(
            all(
                substring in get_files_info(
                    "calculator",
                    "pkg"
                    ) for substring in ["pkg", "calculator.py", "render.py", "__pycache__", "file_size", "is_dir"]
            )
        )

        self.assertTrue(
            all(
                substring in get_files_info(
                    "calculator",
                    "bin"
                    ) for substring in ["Error"]
            )
        )

        self.assertTrue(
            all(
                substring in get_files_info(
                    "calculator",
                    "../"
                    ) for substring in ["Error"]
            )
        )

        #print(get_file_content("calculator", "lorem.txt"))
        self.assertTrue(
            all(
                substring in get_file_content(
                    "calculator",
                    "lorems.txt"
                    ) for substring in ["truncated", "10000"]
            )
        )

        print(get_file_content("calculator", "main.py"))
        print(get_file_content("calculator", "pkg/calculator.py"))
        print(get_file_content("calculator", "/bin/cat"))
        print(get_file_content("calculator", "pkg/does_not_exist.py"))

        print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
        print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
        print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

        print(run_python_file("calculator", "main.py"))
        print(run_python_file("calculator", "main.py", ["3 + 5"]))
        print(run_python_file("calculator", "tests.py"))
        print(run_python_file("calculator", "../main.py"))
        print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    unittest.main()