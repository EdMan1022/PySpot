from unittest import TestCase, mock


class BaseTestClass(TestCase):
    target_path = None

    def create_patch(self, module_name: str, path: str = None):
        """
        Sets up a new mock for a given module in the target path

        :type path: str Optional path to mock at, defaults to target
        :param module_name: (str) Name of the module to mock
        :return: (mock.Patch) The patch of the defined module
        """

        if not path:
            path = self.target_path

        new_mock = mock.patch(target="{}.{}".format(path, module_name))
        self.addCleanup(new_mock.stop)
        return new_mock.start()
