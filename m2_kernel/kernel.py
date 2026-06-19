import os
import re
import sys
import configparser
import subprocess
from metakernel.process_metakernel import ProcessMetaKernel
from metakernel.replwrap import REPLWrapper
from .symbols import completion_symbols
from .mode_magic import ModeMagic
from ._version import __version__

class M2Display:
    "Rich display object carrying independent HTML and native-text representations."
    def __init__(self, html, text):
        self._html = html
        self._text = text
    def _repr_html_(self):
        return self._html
    def __repr__(self):
        return self._text

class M2Kernel(ProcessMetaKernel):
    implementation = "macaulay2_jupyter_kernel"
    implementation_version = __version__

    @property
    def banner(self):
        return (
            f"Jupyter Kernel for Macaulay2 (v{__version__})\n" +
            f"Running Macaulay2 v{self.version}")

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
        "language": "Macaulay2",
        "name": "M2",
    }

    @property
    def help_links(self):
        return super().help_links + [
            {
                "text": "Macaulay2 Documentation",
                "url": "https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/",
            },
        ]

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
        \x0e([^\x12]*)\x12([^\x11]*)\x11([^\x12]*)\x12 # rich: with prompt
        | \x11([^\x12]*)\x12                           # rich: without prompt
        | \x1f(.*?)\x16                                # native text region
        """,
        re.DOTALL | re.VERBOSE
    )
    texmacs_regex = re.compile(
        r"""
        \x02html:([^\x05]*)\x05   # rich html region
        | \x1f(.*?)\x16           # native text region
        """,
        re.DOTALL | re.VERBOSE
    )

    def do_execute_direct(self, code, silent=False):
        # run parent do_execute_direct silently so we can modify the output
        output = super().do_execute_direct(code, True)

        if self.mode == "webapp":
            output = repr(output)
            html = []
            text = []
            pos = 0

            for m in self.webapp_regex.finditer(output):
                gap = output[pos:m.start()].strip()
                if gap:
                    html.append(f"<pre>{gap}</pre>\n")
                    text.append(gap)
                if m.group(5) is not None:          # native text region
                    text.append(m.group(5))
                else:                                # rich HTML region
                    p = re.sub(r"[\x0e\x11\x12]", "", m.group(0))
                    html.append(f"<p>{p}</p>\n")
                pos = m.end()

            gap = output[pos:].strip()
            if gap:
                html.append(f"<pre>{gap}</pre>\n")
                text.append(gap)

            return M2Display("".join(html), "\n\n".join(text))

        elif self.mode == "texmacs":
            output = repr(output)
            html = []
            text = []
            pos = 0

            for m in self.texmacs_regex.finditer(output):
                gap = output[pos:m.start()].strip()
                if gap:
                    html.append(f"<pre>{gap}</pre>\n")
                    text.append(gap)
                if m.group(2) is not None:          # native text region
                    text.append(m.group(2))
                else:                                # rich HTML region
                    p = re.sub(r"\x02html:|\x05", "", m.group(0))
                    html.append(f"<p>{p}</p>\n")
                pos = m.end()

            gap = output[pos:].strip()
            if gap:
                html.append(f"<pre>{gap}</pre>\n")
                text.append(gap)

            return M2Display("".join(html), "\n\n".join(text))

        else:
            self.Write(repr(output))

    def get_completions(self, info):
        return [s for s in completion_symbols if s.startswith(info["obj"])]
