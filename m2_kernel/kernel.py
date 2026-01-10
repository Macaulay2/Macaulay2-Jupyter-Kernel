import os
import re
import sys
from metakernel.process_metakernel import ProcessMetaKernel, TextOutput
from metakernel.replwrap import REPLWrapper
from IPython.display import HTML
from .symbols import completion_symbols

class M2Kernel(ProcessMetaKernel):
    implementation = "macaulay2_jupyter_kernel"
    implementation_version = "0.8.0" # TODO: __version__
    banner = f"Jupyter Kernel for Macaulay2 (v{implementation_version})"
    language_info = {
        "name": "Macaulay2",
        "mimetype": "text/x-macaulay2",
        "file_extension": ".m2",
    }

    @property
    def kernel_json(self):
        return {
            "argv": [
                sys.executable,
                "-m", "m2_kernel",
                "-f", "{connection_file}"],
            "display_name": "Macaulay2",
            "name": "M2",
            "mimetype": "text/x-macaulay2",
            "file_extension": ".m2",
        }

    def __init__(self, *args, **kwargs):
        ProcessMetaKernel.__init__(self, *args, **kwargs)
        self.mode = "webapp"

    def makeWrapper(self):
        init_file = f"{os.path.dirname(__file__)}/assets/m2-code/JupyterKernel.m2"
        return REPLWrapper(
            f"M2 --no-readline -e 'load \"{init_file}\"'",
            r"i+\d+ :\s*$",
            None,
            continuation_prompt_regex=r"\.\.\. : $")

    # regexes to recognize control tags in webapp mode
    webapp_with_prompt = re.compile(
        r"\x0e([^\x12]*)\x12([^\x11]*)\x11([^\x12]*)\x12",
        re.DOTALL)
    webapp_without_prompt = re.compile(
        r"\x11([^\x12]*)\x12",
        re.DOTALL)

    def do_execute_direct(self, code, silent=False):
        if not self.wrapper:
            self.wrapper = self.makeWrapper()

        output = self.wrapper.run_command(code.rstrip())
        if self.mode == "standard":
            return TextOutput(output)
        elif self.mode == "webapp":
            output = self.webapp_with_prompt.sub(
                lambda m: f"<p>{m[1]}{m[2]}{m[3]}</p>", output)
            output = self.webapp_without_prompt.sub(
                lambda m: f"<p>{m[1]}</p>", output)
            return HTML(output)
        elif self.mode == "texmacs":
            return HTML(
                output.replace("\x02html:", "<p>").replace("\x05", "</p>"))
        else:
            return ""

    def get_completions(self, info):
        return [s for s in completion_symbols if s.startswith(info["obj"])]


# TODO:
# * add support for mode, timeout magics (+ any others we currently support?)
# * did we break anything by overriding do_execute_direct?  (almost certainly!)
