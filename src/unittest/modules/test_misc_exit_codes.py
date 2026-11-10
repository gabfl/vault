import os
import tempfile
import unittest

from src.modules import misc


class TestExitCodes(unittest.TestCase):
    def test_create_directory_failure_exits_nonzero(self):
        # makedirs fails when a path component is a file, not a directory
        with tempfile.TemporaryDirectory() as dir_:
            blocker = os.path.join(dir_, 'blocker')
            with open(blocker, 'w') as fh:
                fh.write('x')
            with self.assertRaises(SystemExit) as ctx:
                misc.create_directory_if_missing(
                    os.path.join(blocker, 'sub'))
            self.assertEqual(ctx.exception.code, 1)

    def test_create_directory_success_paths_unchanged(self):
        with tempfile.TemporaryDirectory() as dir_:
            self.assertFalse(misc.create_directory_if_missing(dir_))
            self.assertTrue(misc.create_directory_if_missing(
                os.path.join(dir_, 'some', 'dir')))


if __name__ == '__main__':
    unittest.main()
