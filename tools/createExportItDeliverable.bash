(cd ..

tar --exclude "__pycache__/*" --exclude "apper/apper/__pycache__/*" --exclude "commands/__pycache__/*" --exclude "tools" --exclude=".git" --exclude=".vscode" --exclude="__pycache__" --exclude="tests" --exclude=".gitignore" --exclude=".gitmodules" --exclude="commands/__pachace__" --exclude="commands/config" --exclude="bin" --exclude="commands/logs" -zcvf ./deliverables/ExportIt.tar.gz .

zip -r ./deliverables/ExportIt.zip . -x "__pycache__/*" -x "apper/apper/__pycache__/*" -x "commands/__pycache__/*" -x "tools/*" -x "bin/*" -x ".git/*" -x ".vscode/*" -x "__pycache__/*" -x "tests/*" -x ".gitignore" -x ".gitmodules" -x "commands/__pachace__/*" -x "commands/config/*" -x "commands/logs/*" 
) | tee deliverable.log
