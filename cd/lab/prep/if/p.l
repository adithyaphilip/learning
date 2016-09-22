%{
#include "y.tab.h"
%}
%%
if return IF;
cond return COND;
\( return OB;
\) return CB;
\{ return OFB;
\} return CFB;
%%
int yywrap() {
    return 1;
}

