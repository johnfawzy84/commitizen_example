import sys, os, getopt, subprocess
from typing import no_type_check

def call( cmd,cwd=".", skipExceptionOnError=False, returnStdout = False):
    print ("Calling Command: " + cmd )
    output = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE if returnStdout else sys.stdout, stderr=subprocess.PIPE)
    if (output.returncode != 0):
        print ("\tFailed with error code " + str(output.returncode))
        if not output.stdout is None:
            print ("output:",output.stdout )
        if not output.stderr is None:
            print ("error:",output.stderr)
        if not skipExceptionOnError:
            raise Exception("call Failed.",output)
    else:
        print ("\tSucceeded!")
    return output

def handle_version_bump():
    try:
        call(cmd="cz bump -ch")
    except Exception as e:
        if (e.args[1].returncode == 7):
            print("version is available pumping up again!")
            return True
    return False

if __name__ == "__main__":
    call("git fetch --all --tags")
    call("git add -A")
    call("cz commit") #commit with commitizen
    # call(cmd="cz bump -ch")
    while (handle_version_bump()):
        pass
    # while "available" in bump_output.stderr or "available" in bump_output.stdout : 
    #     bump_output = call("cz bump -ch",returnStdout = True)
    call("git push origin --tags")
        

        
            