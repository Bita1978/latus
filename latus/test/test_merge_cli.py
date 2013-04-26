
import os
import unittest
from .. import merge, util
from . import test_latus


class test_merge_cli(unittest.TestCase):
    def setUp(self):
        root = os.path.join(test_latus.get_root(), "simple")
        md = util.Metadata(root, self.__module__)
        self.lm_cli = merge.merge(os.path.join(root, "src"), os.path.join(root,"domerge.bat"),
                                  os.path.join(root, "dest_temp"), verbose=True, metadata_root_override=md)

    def tearDown(self):
        del self.lm_cli

    def test_copy(self):
        self.lm_cli.mode = merge.str_to_mode("copy")
        self.lm_cli.run()
        self.lm_cli.close()
        data = open(self.lm_cli.out_file_path).read()
        found_it = False
        if "copy" in data:
            found_it = True
        assert(found_it)

    def test_move(self):
        self.lm_cli.mode = merge.str_to_mode("move")
        self.lm_cli.run()
        self.lm_cli.close()
        data = open(self.lm_cli.out_file_path).read()
        found_it = False
        if "move" in data:
            found_it = True
        assert(found_it)

if __name__ == "__main__":
    unittest.main()