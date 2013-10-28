from os import path
# doconv imports
from doconv.plugin import base
from doconv.util import xslt_process


class DocBookToDita(base.PluginBase):

    def get_supported_conversions(self):
        return [("docbook", "dita")]

    def check_dependencies(self):
        pass

    def convert(self, input_file, input_format, output_format,
                output_file=None):
        self.logger.debug("docbooktodita plugin converting...")
        current_dir = path.dirname(__file__)
        xsl_file = path.join(
            current_dir, "docbooktodita/db2dita/docbook2dita.xsl")
        xslt_process(input_file, output_file, xsl_file)
        self.logger.debug("Generated temporary file: {0}".format(output_file))
        return output_file
