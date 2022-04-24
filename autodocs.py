import os

from sympy import fu
import config
#from sample import main
import inspect
import sys
import json
# appending a path

cwd=os.getcwd()

base_dir=os.path.join(cwd, config.BASE_DIR)


module_path=os.path.join(base_dir, config.RUNNER_FILE)
sys.path.append(base_dir)

#from importlib.machinery import SourceFileLoader
#import main
# imports the module from the given path
#main = SourceFileLoader(config.RUNNER_FILE.split(".py")[0],module_path).load_module()

print("[+] create a folder name documentation...")
os.system("mkdocs new documentation")
print("[-] Documentation folder Created!!!")

with open("documentation/mkdocs.yml","w") as f:
    f.write(
'''
site_name: My Docs
nav:
\t- Home: 'index.md'
\t- Usage: 'package-index.md'
\t- API: 'cose.md'


theme: readthedocs
'''
    )
import ast
def show_info(functionNode):
   
    all_args=[]
    for arg in functionNode.args.args:
        #import pdb; pdb.set_trace()
        all_args.append(arg.arg)
    #print("Code",ast.unparse(functionNode.body))
    #for b in functionNode.body:
    #    print("Code",ast.unparse(b))
    return functionNode.name,ast.get_docstring(functionNode),all_args


files = []
for (dirpath, dirnames, filenames) in os.walk(config.BASE_DIR):
    for filename in filenames:
        if filename.endswith('.py'):
            files.append(os.sep.join([dirpath, filename]))
#filename = "sample/abcde/utils.py"
tree={}
for filename in files:
    nameofutils=filename.replace("\\",".").split(".py")[0]
    tree[nameofutils]={}
    with open(filename) as file:
        node = ast.parse(file.read())
    code=ast.unparse(node)
    #print("COde",code)
    tree[nameofutils]["code"]=code
    tree[nameofutils]["modules"]=[]
    tree[nameofutils]["classes"]=[]
    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    
    for function in functions:
        _temp={}
        #print("Code",ast.unparse(function.body))
        func_name,docstring,args=show_info(function)
        _temp["func_name"]=func_name
        _temp["docstring"]=docstring
        _temp["args"]=args
        tree[nameofutils]["modules"].append(_temp)



    for class_ in classes:
        _temp={}
        _temp["class"]=class_.name
        _temp["modules"]=[]
        #node.get_docstring(class_.name)
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            #print(inspect.getsource(namespace[class_.name]))
            #print("Code:",ast.get_source_segment(node,method.body[0]))
            func_name,docstring,args=show_info(method)
            _temp["modules"].append({
                "func_name":func_name,
                "docstring":docstring,
                "args":args
            })
        tree[nameofutils]["classes"].append(_temp)

with open("documentation\docs\package-index.md","w") as f:
    text="# Index\n\n"

    for t in tree:
        text+="### "+t+"\n\n"
        if "classes" in tree[t]:
            for idx,m in enumerate(tree[t]["classes"]):
                text+="#### Class-> "+m["class"]+":####\n\n"
                
                for n in m["modules"]:
                    text+="*** Module-> "+n["func_name"]+"("+",".join(n["args"])+"):"+"***\n\n"
                    if n["docstring"]!=None:
                        text+="```python\n "+n["docstring"]+" \n```\n\n"
                
        for m in tree[t]["modules"]:
            text+="*** Module-> "+m["func_name"]+"("+",".join(m["args"])+")"+"***\n\n"
            if m["docstring"]!=None:
                text+="```python\n "+m["docstring"]+" \n```\n\n"
        text+="---\n"
        
    f.write(text)

with open("documentation\docs\code.md","w") as f:
    text="# Source Code Index\n\n"

    for t in tree:
       text+="### "+t+"\n\n"
       text+="```python\n"+tree[t]["code"]+" \n```\n\n"
        
    f.write(text)