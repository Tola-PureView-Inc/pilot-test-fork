// Example JavaScript code with various issues

function badFunction(userInput) {
    // Security issue: using eval
    var result = eval(userInput);
    
    // Style issue: using var instead of let/const
    var x = 1;
    
    // Style issue: using == instead of ===
    if (x == 1) {
        console.log("Bad comparison");
    }
    
    // Security issue: potential XSS with innerHTML
    document.getElementById("output").innerHTML = "<div>" + userInput + "</div>";
    
    // Style issue: very long line that exceeds the configured maximum length and should trigger a warning
    var veryLongVariableName = "This is a very long line that should trigger a style warning because it exceeds the maximum configured line length";
    
    return result;
}

// Missing documentation
class UndocumentedClass {
    constructor() {
        this.value = 0;
    }
}