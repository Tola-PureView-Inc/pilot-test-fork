# Example Python code with various issues for demonstration

import os
import subprocess

def bad_function(user_input):
    # Security issue: using eval
    result = eval(user_input)
    
    # Style issue: line too long
    very_long_line = "This is a very long line that exceeds the maximum line length configured in the coding agent and should trigger a style warning"
    
    # Security issue: subprocess with shell=True
    subprocess.call(f"echo {user_input}", shell=True)
    
    # Style issue: trailing whitespace on next line
    x = 1    
    
    return result

class UndocumentedClass:
    def method_without_docs(self):
        pass

# Style issue: double semicolon
x = 1;;

print("Example code loaded")