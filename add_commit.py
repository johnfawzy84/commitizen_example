import sys, os, getopt, subprocess
from typing import no_type_check

def call( cmd,cwd=".", skipExceptionOnError=False, returnStdout = False):
    print ("Calling Command: " + cmd )
    output = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE if returnStdout else sys.stdout, stderr=subprocess.PIPE, encoding='utf-8')
    if (output.returncode != 0):
        print ("\tFailed with error code " + str(output.returncode))
        if not output.stdout is None:
            print ("\t\tstdout: " + output.stdout)
        if not output.stderr is None:
            print ("\t\tstderr: "+ output.stderr)
        if not skipExceptionOnError:
            raise Exception("call Failed.",output)
    else:
        print ("\tSucceeded!")
    return output

if __name__ == "__main__":
    call("git fetch --all --tags")
    call("git add -A")
    call("cz commit")
    bump_output = call(cmd="cz bump -ch",returnStdout = True)
    while "available" in bump_output.stderr or "available" in bump_output.stdout : 
        bump_output = call("cz bump -ch")
    call("git push origin --tags")
        

        
            