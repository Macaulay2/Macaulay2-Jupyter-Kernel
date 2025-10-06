jupyterMode = WebApp

-- remove old Jupyter methods if they exist
scan({Thing, Nothing, Boolean, ZZ, InexactNumber, Expression, Net, Describe,
	Ideal, MonomialIdeal, Matrix, Module, RingMap, Sequence,
	CoherentSheaf}, cls -> remove(cls, {Jupyter, AfterPrint}))

importFrom(Core, {"InputPrompt", "InputContinuationPrompt"})
ZZ#{Jupyter, InputPrompt} = ZZ#{Standard, InputPrompt}
-- should match continuation_prompt_regex passed to REPLWrapper
ZZ#{Jupyter, InputContinuationPrompt} = x -> "... : "

getMethod = symb -> x -> (
    (lookup({jupyterMode, symb}, class x)) x;
    if isMember(jupyterMode, {WebApp, TeXmacs}) then << "<p></p>" << endl)
Thing#{Jupyter, Print}        = getMethod Print
Thing#{Jupyter, AfterPrint}   = getMethod AfterPrint
Thing#{Jupyter, AfterNoPrint} = getMethod AfterNoPrint

noop = (trigger) -> (lineNumber -= 1;)

mode = (newmode) -> (
    jupyterMode = newmode;
    noop(mode);
)

topLevelMode = Jupyter
