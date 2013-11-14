# doconv imports
from doconv.plugin import base
from doconv.util import shell, check_bin_dependency, which


class AsciiDoc(base.PluginBase):

    def get_supported_conversions(self):
        return [("asciidoc", "docbook", {"priority": 60})]

    def check_dependencies(self):
        check_bin_dependency("python2")
        check_bin_dependency("asciidoc")

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        self.logger.debug("asciidoc plugin converting...")
        asciidoc_bin = which("asciidoc")
        shell("python2 {0} -b docbook -o {1} {2}".format(asciidoc_bin,
              output_file, input_file))
        self.logger.debug("Generated temporary file: {0}".format(output_file))

        return output_file
