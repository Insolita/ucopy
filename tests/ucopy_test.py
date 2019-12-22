import mock
import os
import unittest
from ucopy import ucopy


class UcopyTest(unittest.TestCase):
    def test__split_ext(self):
        self.assertEqual(ucopy._split_ext('image.jpg'), ('image', '.jpg'))
        self.assertEqual(ucopy._split_ext('archive.tar.gz'), ('archive', '.tar.gz'))
        self.assertEqual(ucopy._split_ext('archive..gz'), ('archive', '..gz'))
        self.assertEqual(ucopy._split_ext('config'), ('config', ''))
        self.assertEqual(ucopy._split_ext('.bashrc'), ('', '.bashrc'))
        self.assertEqual(ucopy._split_ext('..bashrc'), ('', '..bashrc'))

    def test__rand_suffix(self):
        a1 = ucopy._rand_suffix()
        a2 = ucopy._rand_suffix()
        self.assertEqual(len(a1), 5)
        self.assertEqual(len(a2), 5)
        self.assertNotEqual(a1, a2)

    @mock.patch('ucopy.ucopy._rand_suffix', return_value='xyzyz')
    @mock.patch('os.path.exists')
    def test__ensure_unique_filename(self, exists_mock, rand_mock):
        exists_mock.return_value = False
        filename = ucopy._ensure_unique_filename('abc', '.png', '/')
        self.assertEqual(filename, 'abc')

        exists_mock.side_effect = [True, False]
        filename = ucopy._ensure_unique_filename('abc', '.png', '/')
        self.assertEqual(filename, 'abc_[xyzyz]')

        exists_mock.side_effect = [True, True, False]
        filename = ucopy._ensure_unique_filename('abc', '.png', '/')
        self.assertEqual(filename, 'abc_[xyzyz]_[xyzyz]')

    @mock.patch('ucopy.ucopy.copier', return_value=None)
    def test__run(self, copier_mock):
        is_success = ucopy.run(['./stub_dirs/unexisted'], './stub_dirs/target', 'png,.gif')
        self.assertFalse(is_success)
        self.assertEqual(copier_mock.call_count, 0)

        is_success = ucopy.run(['./stub_dirs/dest'], './stub_dirs/unexisted', 'png,.gif')
        self.assertFalse(is_success)
        self.assertEqual(copier_mock.call_count, 0)

        is_success = ucopy.run(['./stub_dirs/*/unexisted'], './stub_dirs/target', 'png,.gif')
        self.assertFalse(is_success)
        self.assertEqual(copier_mock.call_count, 0)

        is_success = ucopy.run(['./stub_dirs/dest'], './stub_dirs/target', 'png,.gif')
        self.assertTrue(is_success)
        self.assertTrue(copier_mock.called)
        self.assertEqual(copier_mock.call_count, 1)
        args = copier_mock.call_args[0]
        self.assertEqual(
            (os.path.abspath('./stub_dirs/dest'), os.path.abspath('./stub_dirs/target'), ['.png', '.gif'], []),
            args
        )
        is_success = ucopy.run(['./stub_dirs/dest'], './stub_dirs/target', '*')
        self.assertTrue(is_success)
        self.assertTrue(copier_mock.called)
        args = copier_mock.call_args[0]
        assert args == (os.path.abspath('./stub_dirs/dest'), os.path.abspath('./stub_dirs/target'), [], [])

        copier_mock.reset_mock()
        is_success = ucopy.run(['./stub_dirs/dest/?/'], './stub_dirs/target', '*')
        self.assertTrue(is_success)
        self.assertTrue(copier_mock.called)
        self.assertEqual(copier_mock.call_count, 2)
        args1 = copier_mock.call_args_list[0][0]
        assert args1 == (os.path.abspath('./stub_dirs/dest/a'), os.path.abspath('./stub_dirs/target'), [], [])
        args2 = copier_mock.call_args_list[1][0]
        assert args2 == (os.path.abspath('./stub_dirs/dest/b'), os.path.abspath('./stub_dirs/target'), [], [])

        copier_mock.reset_mock()
        is_success = ucopy.run(['./stub_dirs/dest/a/', './stub_dirs/dest/b/'], './stub_dirs/target', '*', 'zip, txt')
        self.assertTrue(is_success)
        self.assertTrue(copier_mock.called)
        self.assertEqual(copier_mock.call_count, 2)
        args1 = copier_mock.call_args_list[0][0]
        assert args1 == (os.path.abspath('./stub_dirs/dest/a'), os.path.abspath('./stub_dirs/target'), [], ['.zip', '.txt'])
        args2 = copier_mock.call_args_list[1][0]
        assert args2 == (os.path.abspath('./stub_dirs/dest/b'), os.path.abspath('./stub_dirs/target'), [], ['.zip', '.txt'])

        copier_mock.reset_mock()
        is_success = ucopy.run(['./stub_dirs/dest/*/foo'], './stub_dirs/target', '*')
        self.assertTrue(is_success)
        self.assertTrue(copier_mock.called)
        self.assertEqual(copier_mock.call_count, 2)
        args1 = copier_mock.call_args_list[0][0]
        assert args1 == (os.path.abspath('./stub_dirs/dest/a/foo'), os.path.abspath('./stub_dirs/target'), [], [])
        args2 = copier_mock.call_args_list[1][0]
        assert args2 == (os.path.abspath('./stub_dirs/dest/b/foo'), os.path.abspath('./stub_dirs/target'), [], [])

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.path.islink', return_value=False)
    @mock.patch('ucopy.ucopy._ensure_unique_filename')
    @mock.patch('ucopy.ucopy._copy')
    @mock.patch('os.listdir')
    def test_copier(self, listdir_mock, copy_mock, name_mock, islink_mock, isfile_mock):
        listdir_mock.return_value = ['a.png', 'b.txt']
        name_mock.side_effect = ['a', 'b', 'b', 'b', 'b', 'b', 'b']
        ucopy.copier('/src', '/dst', ['.png', '.jpg'], [])
        self.assertTrue(copy_mock.called)
        self.assertEqual(copy_mock.call_count, 1)
        self.assertEqual(copy_mock.call_args[0], ('/src/a.png', '/dst/a.png'))

        copy_mock.reset_mock()
        ucopy.copier('/src', '/dst', [], ['.png'])
        self.assertTrue(copy_mock.called)
        self.assertEqual(copy_mock.call_count, 1)
        self.assertEqual(copy_mock.call_args[0], ('/src/b.txt', '/dst/b.txt'))

        copy_mock.reset_mock()
        ucopy.copier('/src', '/dst', ['.png'], ['.png'])
        self.assertTrue(copy_mock.called)
        self.assertEqual(copy_mock.call_count, 1)
        self.assertEqual(copy_mock.call_args[0], ('/src/b.txt', '/dst/b.txt'))

        copy_mock.reset_mock()
        ucopy.copier('/src', '/dst', ['.txt'], [])
        self.assertTrue(copy_mock.called)
        self.assertEqual(copy_mock.call_count, 1)
        self.assertEqual(copy_mock.call_args[0], ('/src/b.txt', '/dst/b.txt'))

        copy_mock.reset_mock()
        name_mock.side_effect = ['a', 'b']
        ucopy.copier('/src', '/dst', [], [])
        self.assertTrue(copy_mock.called)
        self.assertEqual(copy_mock.call_count, 2)

        copy_mock.reset_mock()
        islink_mock.return_value = True
        ucopy.copier('/src', '/dst', [], [])
        self.assertFalse(copy_mock.called)

        copy_mock.reset_mock()
        isfile_mock.return_value = False
        ucopy.copier('/src', '/dst', [], [])
        self.assertFalse(copy_mock.called)


if __name__ == '__main__':
    unittest.main()
