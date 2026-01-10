newPackage "JupyterKernel"

export {"changeJupyterMode"}

importFrom(Core, {
	"InputPrompt",
	"InputContinuationPrompt",
	"Hypertext"})
importFrom(Varieties, "CoherentSheaf")

protect Jupyter

jupyterMode = WebApp

ZZ#{Jupyter, InputPrompt} = ZZ#{Standard, InputPrompt}
-- should match continuation_prompt_regex passed to REPLWrapper
ZZ#{Jupyter, InputContinuationPrompt} = x -> "... : "

getMethod = symb -> x -> (lookup({jupyterMode, symb}, class x) ?? identity) x
Thing#{Jupyter, BeforePrint}  = getMethod BeforePrint
Thing#{Jupyter, NoPrint}      = getMethod NoPrint
Thing#{Jupyter, Print}        = getMethod Print
Thing#{Jupyter, AfterPrint}   = getMethod AfterPrint
Thing#{Jupyter, AfterNoPrint} = getMethod AfterNoPrint
Thing#{Jupyter, print}        = getMethod print

changeJupyterMode = mode -> (
    jupyterMode = mode;
    lineNumber -= 1;)

topLevelMode = Jupyter

-- override some hypertext methods for syntax highlighting w/ highlight.js
replaceClass = method()
replaceClass(String, Thing) := (cls, x) -> x
replaceClass(String, Option) := (cls, o) -> o#0 => cls
replaceClass(String, Hypertext) := (cls, x) -> apply(x, replaceClass_cls)

replaceHypertext = (T, cls) -> (
    oldhypertext := lookup(hypertext, T);
    hypertext T := replaceClass_cls @@ oldhypertext)

replaceHypertext(Dictionary, "hljs-type")
replaceHypertext(Type, "hljs-type")
replaceHypertext(Command, "hljs-built_in")
replaceHypertext(Function, "hljs-built_in")
replaceHypertext(FunctionBody, "hljs-built_in")
replaceHypertext(Boolean, "hljs-literal")
replaceHypertext(File, "hljs-literal")
replaceHypertext(IndeterminateNumber, "hljs-literal")
replaceHypertext(Manipulator, "hljs-literal")
replaceHypertext(Nothing, "hljs-literal")
replaceHypertext(Package, "hljs-literal")
replaceHypertext(Net, "hljs-string")
replaceHypertext(String, "hljs-string")
replaceHypertext(Time, "hljs-comment")
