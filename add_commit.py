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
            raise Exception("call Failed.")
    else:
        print ("\tSucceeded!")
    return output

if __name__ == "__main__":
    output = call( cwd="." , cmd="git branch -r", returnStdout=True)
    print (len(output.stdout.split("\n")))
    if output.stderr == '' : 
        call(cmd="git fetch --all")
        for line in output.stdout.strip().split("\n"):
            line = line.strip() 
            if not("HEAD" in line) :
                call( cmd='git branch --track "{}" "{}" --force'.format(line,line.split("/")[1]))
        call("git fetch --all")
        call("git pull --all")
        call("git add -A")
        call("cz commit")
        bump_output = call("cz bump -ch")
        while bump_output.stderr != None : 
            bump_output = call("cz bump -ch")
        

        
            