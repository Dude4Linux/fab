import os
import sys

import stdtrap
import executil

from executil import ExecError

CPP_ARGS = ("-I", "-D", "-U")

class Error(Exception):
    pass

def getopt(argv):
    """get cpp arguments in argv -> (cpp_arguments, non_cpp_arguments)"""

    argv = argv[:]

    opts = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        
        for cpp_arg in CPP_ARGS:
            if arg.startswith(cpp_arg):
                if arg == cpp_arg:
                    opt = arg
                    try:
                        val = argv[i + 1]
                    except IndexError:
                        raise Error("no value for option " + opt)

                    del argv[i + 1]
                    del argv[i]
                else:
                    opt = arg[:len(cpp_arg)]
                    val = arg[len(cpp_arg):]

                    del argv[i]

                opts.append((opt, val))
                break
        else:
              i += 1
              
    return opts, argv

def cpp(input, cpp_opts=[]):
    """preprocess <input> through cpp -> preprocessed output
       input may be path/to/file or iterable data type
    """
    args = [ "-Ulinux" ]

    for opt, val in cpp_opts:
        args.append(opt + val)

    include_path = os.environ.get('FAB_PLAN_INCLUDE_PATH')
    if include_path:
        args.append("-I" + include_path)

    command = ["cpp", input]
    if args:
        command += args

    trap = stdtrap.StdTrap()
    try:
        executil.system(*command)
    except ExecError, e:
        trap.close()
        trapped_stderr = trap.stderr.read()
        raise ExecError(" ".join(command), e.exitcode, trapped_stderr)

    trap.close()
    return trap.stdout.read()
