from doconv.plugin import base
from doconv.util import check_bin_dependency, shell


class AsciiDoctor(base.PluginBase):

    def get_supported_conversions(self):
        return [("asciidoc", "docbook", {"priority": 50})]

    def check_dependencies(self):
        check_bin_dependency("asciidoctor")

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        self.logger.debug("asciidoctor plugin converting...")
        shell(
            "asciidoctor -b docbook -o {0} {1}".format(output_file,
                                                       input_file))
        self.logger.debug("Generated temporary file: {0}".format(output_file))

        return output_file
