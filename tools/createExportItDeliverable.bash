cd ..
tar --exclude "tools" --exclude=".git" --exclude=".vscode" --exclude="__pycache__" --exclude="tests" --exclude=".gitignore" --exclude=".gitmodules" --exclude="commands/__pachace__" --exclude="commands/config" --exclude="commands/logs" -zcvf ./tools/ExportIt.tar.gz .

zip -r ./tools/ExportIt.zip . -x "tools/*" -x ".git/*" -x ".vscode/*" -x "__pycache__/*" -x "tests/*" -x ".gitignore" -x ".gitmodules" -x "commands/__pachace__/*" -x "commands/config/*" -x "commands/logs/*" 

