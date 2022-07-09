(cd ..

rm ./deliverables/ExportIt.tar.gz
rm ./deliverables/ExportIt.zip
rm ../commands/logs/deliverable.log

tar --exclude "__pycache__/*" --exclude "apper/apper/__pycache__/*" --exclude "commands/__pycache__/*" --exclude "tools" --exclude=".git" --exclude=".vscode" --exclude="__pycache__" --exclude="tests" --exclude=".gitignore" --exclude=".gitmodules" --exclude="commands/__pachace__" --exclude="commands/config" --exclude="bin" --exclude="commands/logs" --exclude "deliverables/*" -zcvf ./deliverables/ExportIt.tar.gz .

sleep 2

zip -r ./deliverables/ExportIt.zip . -x "__pycache__" -x "apper/apper/__pycache__" -x "commands/__pycache__" -x "tools" -x ".git" -x ".vscode" -x "__pycache__" -x "tests" -x ".gitignore" -x ".gitmodules" -x "commands/__pachace__" -x "commands/config" -x "bin" -x "commands/logs" -x "deliverables"
) | tee ../commands/logs/deliverable.log
