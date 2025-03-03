jupyterMode = Standard

-- remove old Jupyter methods if they exist
scan({Thing, Nothing, Boolean, ZZ, InexactNumber, Expression, Net, Describe,
	Ideal, MonomialIdeal, Matrix, Module, RingMap, Sequence,
	CoherentSheaf}, cls -> remove(cls, {Jupyter, AfterPrint}))

importFrom(Core, {"InputPrompt", "InputContinuationPrompt"})
ZZ#{Jupyter, InputPrompt} = ZZ#{Standard, InputPrompt}
ZZ#{Jupyter, InputContinuationPrompt} = ZZ#{Standard, InputContinuationPrompt}

Nothing#{Jupyter, Print}        =
Nothing#{Jupyter, AfterPrint}   =
Nothing#{Jupyter, AfterNoPrint} =
   File#{Jupyter, AfterNoPrint} = x -> null

sentinel = (str, f) -> x -> (
    << "--" << str << endl;
    f x;)

Thing#{Jupyter, Print} = x -> (
    sentinel("VAL", lookup({jupyterMode, Print}, class x))) x
Thing#{Jupyter, AfterPrint} = x -> (
    sentinel("CLS", lookup({jupyterMode, AfterPrint}, class x))) x
Thing#{Jupyter, AfterNoPrint} = x -> (
    sentinel("CLS", lookup({jupyterMode, AfterNoPrint}, class x))) x


noop = (trigger) -> (lineNumber -= 1;)

mode = (newmode) -> (
    jupyterMode = newmode;
    noop(mode);
)

topLevelMode = Jupyter
