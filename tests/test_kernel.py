import unittest
import jupyter_kernel_test as jkt


class M2KernelTests(jkt.KernelTests):
    kernel_name = "m2"
    language_name = "Macaulay2"
    file_extension = ".m2"
    code_hello_world = "\"hello, world\""

    def setUp(self):
        self.flush_channels()
        self.execute_helper(code="%mode standard")

if __name__ == "__main__":
    unittest.main()
