# switch
def switch(language):
    switcher = {
        "C": ["January","one"],
        "Python": ["February","2"],
        "Java": ["March","3"]
    }
    res = switcher.get(argument, "Invalid month")
    return res
    
print switch_demo("C")[0]
print switch_demo("Java")[1]