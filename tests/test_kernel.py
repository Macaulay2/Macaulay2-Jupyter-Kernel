import unittest
import jupyter_kernel_test as jkt


class M2KernelTests(jkt.KernelTests):
    kernel_name = "m2"
    language_name = "Macaulay2"
    file_extension = ".m2"
    code_hello_world = 'print "hello, world"'

    # Two statements in one cell: first result → display_data, second → execute_result
    code_display_data = [{"code": "1\n2", "mime": "text/plain"}]

    code_execute_result = [{"code": "1 + 1"}]

    completion_samples = [{"text": "ring"}]

    complete_code_samples = ["1 + 1\n"]
    incomplete_code_samples = ["1 + 1"]

    def setUp(self):
        self.flush_channels()
        self.execute_helper(code="%mode standard")

if __name__ == "__main__":
    unittest.main()
