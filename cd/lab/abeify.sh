#!/bin/bash
ABEBIN=~/.abebin
ABEBABE=~/.abethebabe
# create script directory
mkdir $ABEBIN 2> abeify.err
# add script directory to path in .bashrc if not exist
BASHRC=~/.bashrc
if [[ $(cat $BASHRC) != *$HOME"/.abebin"* ]]
then
printf "PATH=\$PATH\":$ABEBIN\"\nexport PATH\n" >> $BASHRC
fi
# scripts in ABEBIN
## ctoff script
CTOFF=$ABEBIN/ctoff
echo "nohup $@& 2>~/ctoff.err >~/ctoff.out" > $CTOFF
chmod +x $CTOFF
### scripts using ctoff
CTCHROME=$ABEBIN/ctchrome
echo "ctoff google-chrome-stable" > $CTCHROME
## abelexify
LEXIFY=$ABEBIN/abelexify
echo "lex -o \$1.yy.c \$1;gcc -ll -o \$1.c \$1.yy.c;./\$1.out \$2" > $LEXIFY
chmod +x $LEXIFY
