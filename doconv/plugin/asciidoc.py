# doconv imports
from doconv.plugin import base
from doconv.util import shell, check_bin_dependency


class AsciiDoc(base.PluginBase):

    def get_supported_conversions(self):
        return [("asciidoc", "docbook")]

    def check_dependencies(self):
        check_bin_dependency("asciidoc")

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        self.logger.debug("asciidoc plugin converting...")
        shell("asciidoc -b docbook -o {0} {1}".format(output_file, input_file))
        self.logger.debug("Generated temporary file: {0}".format(output_file))

        return output_file
