import abc


class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_supported_conversions_graph(self):
        """Method documentation"""
        return

    @abc.abstractmethod
    def convert(self, input_file, output_file, input_format, output_format):
        """Method docs"""
        return

    @abc.abstractmethod
    def check_dependencies(self):
        """Method docs"""
        return
