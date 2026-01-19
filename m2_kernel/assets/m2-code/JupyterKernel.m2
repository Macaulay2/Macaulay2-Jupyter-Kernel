newPackage "JupyterKernel"

export {"changeJupyterMode"}

importFrom(Core, {
	"htmlFilename",
	"InputPrompt",
	"InputContinuationPrompt",
	"toURL"
	})

beginDocumentation()

protect Jupyter

-- in case we try to reload this package:
path = append(path, currentFileDirectory)

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

-- make links in help point to webpage
oldHtmlFilename = lookup(htmlFilename, DocumentTag)
htmlFilename DocumentTag := t -> (
    "https://www.macaulay2.com/doc/Macaulay2/",
    last oldHtmlFilename t)

oldToURL = lookup(toURL, String)
toURL String := url -> replace(
    "^(?:common/)?share/",
    "https://www.macaulay2.com/doc/Macaulay2/share/", oldToURL url)
toURL FilePosition := p -> replace(
    regexQuote prefixDirectory, "https://www.macaulay2.com/doc/Macaulay2/", p#0)

-- redefine show to display things in Jupyter

show Hypertext := show TEX := print

mimetypecmd = (
    if run "command -v xdg-mime > /dev/null" == 0
    then "!xdg-mime query filetype "
    else if run "command -v mimetype > /dev/null" == 0
    then "!mimetype -b "
    else if run "command -v file > /dev/null" == 0
    then "!file --mime -b "
    else "false ")

windowOpen = url -> print LITERAL("<script>window.open(\"" | url |"\")</script>")

show URL := url -> (
    url = url#0;
    if match("^http", first url) then windowOpen url
    else (
	file := (
	    if (m := regex("^file://(.*)", url)) =!= null
	    then substring(m#1, url)
	    else url);
	if not fileExists file then error(file, " does not exist");
	makeDirectory "show_files";
	copyFile(file, file = "show_files/" | baseFilename file);
	mimetype := first lines get(mimetypecmd | file);
	if match("^image", mimetype) then print IMG("src" => file)
	else windowOpen("/files/" | file)))
