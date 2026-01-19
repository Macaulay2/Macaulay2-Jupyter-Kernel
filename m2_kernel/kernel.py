import os
import re
import sys
import configparser
import html2text
import subprocess
from metakernel.process_metakernel import ProcessMetaKernel, TextOutput
from metakernel.replwrap import REPLWrapper
from IPython.display import HTML
from .symbols import completion_symbols
from .mode_magic import ModeMagic
from ._version import __version__

class HTMLWithTextFallback(HTML):
    "Provide text fallback for html output outside of web browsers."
    def __repr__(self):
        return html2text.html2text(self._repr_html_())

class M2Kernel(ProcessMetaKernel):
    implementation = "macaulay2_jupyter_kernel"
    implementation_version = __version__
    banner = f"Jupyter Kernel for Macaulay2 (v{implementation_version})"

    @property
    def language_info(self):
        return {
            "name": "Macaulay2",
            "mimetype": "text/x-macaulay2",
            "file_extension": ".m2",
            "version": self.version
        }

    kernel_json = {
        "argv": [
            sys.executable,
            "-m", "m2_kernel",
            "-f", "{connection_file}"],
        "display_name": "Macaulay2",
        "name": "M2",
    }

    def __init__(self, *args, **kwargs):
        ProcessMetaKernel.__init__(self, *args, **kwargs)
        self.execpath = "M2"
        self.mode = "webapp"
        init_file = f"{os.path.dirname(__file__)}/assets/m2-code/JupyterKernel.m2"
        self.init_cmd = f'load \"{init_file}\"'

        config = configparser.ConfigParser()
        configpath = os.getenv("M2JK_CONFIG")
        if configpath:
            config.read(configpath)
            if "magic" in config:
                if "execpath" in config["magic"]:
                    self.execpath = config["magic"]["execpath"]
                if "mode" in config["magic"]:
                    mode = config["magic"]["mode"]
                    if mode in ModeMagic.modes:
                        self.mode = mode
                        self.init_cmd += f"; changeJupyterMode {ModeMagic.modes[mode]}"
                    else:
                        raise ValueError(f"expected one of {list(ModeMagic.modes.keys())}")

        self.version = subprocess.check_output(
            [self.execpath, "--version"], text=True).strip()
        self.register_magics(ModeMagic)

    def makeWrapper(self):
        return REPLWrapper(
            f"{self.execpath} --no-readline -e '{self.init_cmd}'",
            r"i+\d+ :\s*$",
            None,
            continuation_prompt_regex=r"\.\.\. : $")

    webapp_regex = re.compile(
        r"""
        \x0e([^\x12]*)\x12([^\x11]*)\x11([^\x12]*)\x12 # with prompt
        | \x11([^\x12]*)\x12                           # without prompt
        """,
        re.DOTALL | re.VERBOSE
    )
    texmacs_regex = re.compile(r"\x02html:([^\x05]*)\x05", re.DOTALL)

    def do_execute_direct(self, code, silent=False):
        # run parent do_execute_direct silently so we can modify the output
        output = super().do_execute_direct(code, True)

        if self.mode == "webapp":
            output = repr(output)
            html = []
            pos = 0

            for m in self.webapp_regex.finditer(output):
                pre = output[pos:m.start()].strip()
                if pre:
                    html.append(f"<pre>{pre}</pre>\n")
                p = re.sub(r"[\x0e\x11\x12]", "",  m.group(0))
                html.append(f"<p>{p}</p>\n")
                pos = m.end()

            pre = output[pos:].strip()
            if pre:
                html.append(f"<pre>{pre}</pre>\n")

            return HTMLWithTextFallback("".join(html))

        elif self.mode == "texmacs":
            output = repr(output)
            html = []
            pos = 0

            for m in self.texmacs_regex.finditer(output):
                pre = output[pos:m.start()].strip()
                if pre:
                    html.append(f"<pre>{pre}</pre>\n")
                p = re.sub(r"\x02html:|\x05", "", m.group(0))
                html.append(f"<p>{p}</p>\n")
                pos = m.end()

            pre = output[pos:].strip()
            if pre:
                html.append(f"<pre>{pre}</pre>\n")

            return HTMLWithTextFallback("".join(html))

        else:
            return output

    def get_completions(self, info):
        return [s for s in completion_symbols if s.startswith(info["obj"])]
