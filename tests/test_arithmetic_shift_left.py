import sys

from niveristand import _decorators, RealTimeSequence, TranslateError, VeristandError
from niveristand import realtimesequencetools
from niveristand.clientapi import BooleanValue, ChannelReference, DoubleValue, I32Value, I64Value
from niveristand.library.primitives import localhost_wait
import pytest
from testutilities import rtseqrunner, validation

a = 1
b = 2


@_decorators.nivs_rt_sequence
def return_constant():
    a = I32Value(5)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_simple_numbers():
    a = DoubleValue(0)
    a.value = 1 << 3
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_num_nivsdatatype():
    a = DoubleValue(0)
    a.value = 1 << DoubleValue(3)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_nivsdatatype_nivsdatatype():
    a = DoubleValue(0)
    a.value = DoubleValue(1) << DoubleValue(3)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_nivsdatatype_nivsdatatype1():
    a = DoubleValue(0)
    a.value = DoubleValue(1) << I32Value(3)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_nivsdatatype_nivsdatatype2():
    a = BooleanValue(0)
    a.value = BooleanValue(1) << BooleanValue(3)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_nivsdatatype_nivsdatatype3():
    a = DoubleValue(0)
    a.value = I32Value(1) << I32Value(3)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_multiple_types():
    a = I32Value(0)
    a.value = 1 << I32Value(3) << 5
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_multiple_types1():
    a = I64Value(1)
    a.value = 1 << I64Value(5) << 3 << I32Value(7)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq():
    a = DoubleValue(0)
    a.value = 1 << return_constant()
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq1():
    a = DoubleValue(0)
    a.value = return_constant() << 1
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq2():
    a = DoubleValue(0)
    a.value = I32Value(1) << return_constant()
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq3():
    a = DoubleValue(0)
    a.value = return_constant() << I32Value(1)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq4():
    a = DoubleValue(0)
    a.value = I32Value(1) << return_constant()
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_use_rtseq5():
    a = DoubleValue(0)
    a.value = return_constant() << I32Value(1)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_with_parantheses():
    a = I32Value(0)
    a.value = 1 << (2 << 1)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_with_parantheses1():
    a = DoubleValue(0)
    a.value = 1 << (DoubleValue(2) << I32Value(1))
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_with_parantheses2():
    a = DoubleValue(0)
    a.value = DoubleValue(1) << (I32Value(2) << 1.0) << DoubleValue(4)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variables():
    a = I32Value(5)
    b = I32Value(0)
    b.value = 1 << a
    return b.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variables1():
    a = I64Value(5)
    b = I64Value(0)
    b.value = 1 << a.value
    return b.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variable_variable():
    a = I32Value(1)
    b = I64Value(3)
    c = I32Value(0)
    c.value = a.value << b.value
    return c.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variable_variable1():
    a = I32Value(1)
    b = I64Value(3)
    c = DoubleValue(0)
    c.value = a.value << b.value
    return c.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variable_rtseq():
    a = I32Value(1)
    b = DoubleValue(0)
    b.value = a.value << return_constant()
    return b.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_variable_rtseq1():
    a = I32Value(1)
    b = DoubleValue(0)
    b.value = return_constant() << a.value
    return b.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_to_channelref():
    a = DoubleValue(0)
    b = ChannelReference("Aliases/DesiredRPM")
    b.value = 5.0
    localhost_wait()
    a.value = 1 << b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_binary_unary():
    a = I32Value(0)
    a.value = 3 << - 1
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_number():
    a = I32Value(1)
    a.value <<= 2
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_nivsdatatype():
    a = I32Value(1)
    a.value <<= I32Value(2)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_nivsdatatype1():
    a = I64Value(1)
    a.value <<= I64Value(2)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_nivsdatatype2():
    a = I64Value(1)
    a.value <<= I32Value(2)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_nivsdatatype3():
    a = I32Value(1)
    a.value <<= I64Value(2)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_nivsdatatype4():
    a = I32Value(1)
    a.value <<= DoubleValue(2)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_variable():
    a = I32Value(1)
    b = I32Value(2)
    a.value <<= b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_variable1():
    a = I64Value(1)
    b = I64Value(2)
    a.value <<= b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_variable2():
    a = I32Value(1)
    b = I64Value(2)
    a.value <<= b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_variable3():
    a = I64Value(1)
    b = I32Value(2)
    a.value <<= b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_variable4():
    a = I32Value(1)
    b = DoubleValue(2)
    a.value <<= b.value
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_rtseq():
    a = I32Value(1)
    a.value <<= return_constant()
    return a.value


@_decorators.nivs_rt_sequence
def arithemtic_shift_left_augassign_paranthesis():
    a = I32Value(1)
    a.value <<= (2 + I32Value(1)) + I64Value(1)
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_augassign_channelref():
    a = DoubleValue(1)
    b = ChannelReference("Aliases/DesiredRPM")
    b.value = 5.0
    localhost_wait()
    a.value <<= b.value
    return a.value


# <editor-fold desc=Invalid tests>
@_decorators.nivs_rt_sequence
def arithmetic_shift_left_invalid_variables():
    return a.value << b


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_invalid_variables1():
    return a.value << b.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_to_None():
    a = DoubleValue(0)
    a.value = None << 1
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_invalid_rtseq_call():
    a = DoubleValue(0)
    a.value = return_constant << 1
    return a.value


@_decorators.nivs_rt_sequence
def arithmetic_shift_left_complex_expr():
    a = DoubleValue(0)
    a.value = 1 << (2 if 2 < 3 else 4)
    return a.value

# </editor-fold>


run_tests = [
    (return_constant, (), 5.0),
    (arithmetic_shift_left_simple_numbers, (), 8),
    (arithmetic_shift_left_nivsdatatype_nivsdatatype1, (), 8),
    (arithmetic_shift_left_nivsdatatype_nivsdatatype3, (), 8),
    (arithmetic_shift_left_variables, (), 32),
    (arithmetic_shift_left_variables1, (), 32),
    (arithmetic_shift_left_multiple_types, (), 256),
    (arithmetic_shift_left_multiple_types1, (), 32768),
    (arithmetic_shift_left_with_parantheses, (), 16),
    (arithmetic_shift_left_variable_variable, (), 8),
    (arithmetic_shift_left_variable_variable1, (), 8),
    (arithmetic_shift_left_augassign_number, (), 4),
    (arithmetic_shift_left_augassign_nivsdatatype, (), 4),
    (arithmetic_shift_left_augassign_nivsdatatype1, (), 4),
    (arithmetic_shift_left_augassign_nivsdatatype2, (), 4),
    (arithmetic_shift_left_augassign_nivsdatatype3, (), 4),
    (arithmetic_shift_left_augassign_variable, (), 4),
    (arithmetic_shift_left_augassign_variable1, (), 4),
    (arithmetic_shift_left_augassign_variable2, (), 4),
    (arithmetic_shift_left_augassign_variable3, (), 4),
    (arithemtic_shift_left_augassign_paranthesis, (), 16),
    (arithmetic_shift_left_use_rtseq, (), 32),
    (arithmetic_shift_left_use_rtseq1, (), 10),
    (arithmetic_shift_left_use_rtseq2, (), 32),
    (arithmetic_shift_left_use_rtseq3, (), 10),
    (arithmetic_shift_left_use_rtseq4, (), 32),
    (arithmetic_shift_left_use_rtseq5, (), 10),
    (arithmetic_shift_left_variable_rtseq, (), 32),
    (arithmetic_shift_left_variable_rtseq1, (), 10),
    (arithmetic_shift_left_complex_expr, (), 4),
    (arithmetic_shift_left_augassign_rtseq, (), 32),
]

skip_tests = [
    (arithmetic_shift_left_invalid_rtseq_call, (), "RTSeq call not implemented yet."),
    (arithmetic_shift_left_binary_unary, (), "Different behaviour between python and SPE."),
]

fail_transform_tests = [
    (arithmetic_shift_left_invalid_variables, (), TranslateError),
    (arithmetic_shift_left_invalid_variables1, (), TranslateError),
    (arithmetic_shift_left_num_nivsdatatype, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_nivsdatatype_nivsdatatype, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_nivsdatatype_nivsdatatype2, (), VeristandError),  # cannot do shift left on Boolean
    (arithmetic_shift_left_with_parantheses1, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_with_parantheses2, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_augassign_nivsdatatype4, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_augassign_variable4, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_to_channelref, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_augassign_channelref, (), VeristandError),  # cannot do shift left on Double
    (arithmetic_shift_left_to_None, (), TranslateError),
]

py_only_errs = [
    (arithmetic_shift_left_nivsdatatype_nivsdatatype1, (), 8),  # cannot do shift left on float
]


def idfunc(val):
    return val.__name__


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_transform(func_name, params, expected_result):
    RealTimeSequence(func_name)


@pytest.mark.parametrize("func_name, params, expected_result", list(set(run_tests) - set(py_only_errs)), ids=idfunc)
def test_runpy(func_name, params, expected_result):
    actual = func_name(*params)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_run_py_as_rts(func_name, params, expected_result):
    actual = realtimesequencetools.run_py_as_rtseq(func_name)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", run_tests, ids=idfunc)
def test_run_in_VM(func_name, params, expected_result):
    actual = rtseqrunner.run_rtseq_in_VM(func_name)
    assert actual == expected_result


@pytest.mark.parametrize("func_name, params, expected_result", fail_transform_tests, ids=idfunc)
def test_failures(func_name, params, expected_result):
    with pytest.raises(expected_result):
        RealTimeSequence(func_name)
    with pytest.raises(expected_result):
        func_name(*params)


@pytest.mark.parametrize("func_name, params, reason", skip_tests, ids=idfunc)
def test_skipped(func_name, params, reason):
    pytest.skip(func_name.__name__ + ": " + reason)


def test_check_all_tested():
    validation.test_validate(sys.modules[__name__])
