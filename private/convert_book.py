import glob
import sys
import re
import shutil
import os


sys.path.append('/Users/massimodipierro/Dropbox/web2py')

HEADER = r"""
\documentclass[justified,sixbynine,notoc]{tufte-book}
\title{web2py\\{\small Full-Stack Web Framework, 4th Edition}}
\author{Massimo Di Pierro}
\publisher{Experts4Solutions}

% For nicely typeset tabular material
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{makeidx}
\usepackage{tocloft}
\usepackage{parskip}
\usepackage{upquote}
%\usepackage{CJK}

\makeindex
\usepackage{listings}
\usepackage{url}
\usepackage[utf8x]{inputenc}

\sloppy

\definecolor{lg}{rgb}{0.9,0.9,0.9}
\definecolor{dg}{rgb}{0.3,0.3,0.3}
\def\ft{\small\tt}
\def\inxx#1{\index{#1}}

\lstset{language=Python,
keywords={A,B,BEAUTIFY,BODY,BR,CENTER,CLEANUP,CODE,CRYPT,DAL,DIV,EM,EMBED,FIELDSET,FORM,Field,H1,H2,H3,H4,H5,H6,HEAD,HR,HTML,HTTP,I,IFRAME,IMG,INPUT,IS\_ALPHANUMERIC,IS\_DATE,IS\_DATETIME,IS\_DATETIME\_IN\_RANGE,IS\_DATE\_IN\_RANGE,IS\_DECIMAL\_IN\_RANGE,IS\_EMAIL,IS\_EMPTY\_OR,IS\_EQUAL\_TO,IS\_EXPR,IS\_FLOAT\_IN\_RANGE,IS\_IMAGE,IS\_INT\_IN\_RANGE,IS\_IN\_DB,IS\_IN\_SET,IS\_IPV4,IS\_LENGTH,IS\_LIST\_OF,IS\_LOWER,IS\_MATCH,IS\_NOT\_EMPTY,IS\_NOT\_IN\_DB,IS\_NULL\_OR,IS\_SLUG,IS\_STRONG,IS\_TIME,IS\_UPLOAD\_FILENAME,IS\_UPPER,IS\_URL,LABEL,LEGEND,LI,LINK,LOAD,MARKMIN,MENU,META,OBJECT,OL,ON,OPTGROUP,OPTION,P,PRE,SCRIPT,SELECT,SPAN,SQLDB,SQLFORM,SQLField,SQLTABLE,STYLE,T,TABLE,TAG,TBODY,TD,TEXTAREA,TFOOT,TH,THEAD,TITLE,TR,TT,UL,URL,XHTML,XML,cache,embed64,local\_import,redirect,request,response,session,xmlescape},
   breaklines=true, basicstyle=\ttfamily\color{black}\footnotesize,
   keywordstyle=\bf\ttfamily, %\color{Orange},                                                                             
   commentstyle=\it\ttfamily, %\color{OliverGreen},                                                                       
   stringstyle=\color{dg}\it\ttfamily, %\color{Purple},                                                                  
   numbers=left, numberstyle=\color{dg}\tiny, stepnumber=1, numbersep=5pt,                                                
   backgroundcolor=\color{lg}, tabsize=4, showspaces=false,                                                             
   showstringspaces=false}

\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{4}
% Generates the index
\begin{document}

\frontmatter

\maketitle
\thispagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{2mm}
{\footnotesize
\vskip 1in
Copyright 2008-2013 by Massimo Di Pierro. All rights reserved.
\vskip 1cm
No part of this publication may be reproduced, stored in a retrieval
system, or transmitted in any form or by any means, electronic,
mechanical, photocopying, recording, scanning, or otherwise, except
as permitted under Section 107 or 108 of the 1976 United States
Copyright Act, without either the prior written permission of the
Publisher, or authorization through payment of the appropriate
per-copy fee to the Copyright Clearance Center, Inc., 222 Rosewood
Drive, Danvers, MA 01923, (978) 750-8400, fax (978) 646-8600, or on
the web at www.copyright.com. Requests to the Copyright owner for
permission should be addressed to:
\begin{verbatim}
Massimo Di Pierro
School of Computing
DePaul University
243 S Wabash Ave
Chicago, IL 60604 (USA)
Email: massimo.dipierro@gmail.com
\end{verbatim}

Limit of Liability/Disclaimer of Warranty: While the publisher and
author have used their best efforts in preparing this book, they
make no representations or warranties with respect to the accuracy
or completeness of the contents of this book and specifically
disclaim any implied warranties of merchantability or fitness for a
particular purpose.  No warranty may be created ore extended by
sales representatives or written sales materials. 
The advice and strategies contained herein may not be
suitable for your situation. You should consult with a professional
where appropriate.  Neither the publisher nor author shall be liable 
for any loss of profit or any other commercial damages, including
but not limited to special, incidental, consequential, or other damages. \\ \\

Library of Congress Cataloging-in-Publication Data: \\ \\
ISBN: 978-0-578-09793-0 \\
Build Date: \today
}

\newpage
%\begin{center}
%\noindent\fontsize{12}{18}\selectfont\itshape
\nohyphenation
\thispagestyle{empty}
\phantom{placeholder}
\vspace{2in}
\hskip 3in
{\it to my family}
%\end{center}
\newpage
\thispagestyle{empty}
\phantom {a}
\newpage

\setlength{\cftparskip}{\baselineskip}
\tableofcontents

\mainmatter
\begin{fullwidth}
%\begin{CJK*}{UTF8}{min}


\chapter*{Preface}
"""

FOOTER = r"""
\end{fullwidth}

\backmatter
\printindex

\begin{thebibliography}{999}
@BIBITEMS
\end{thebibliography}
\end{document}
"""

from gluon.contrib.markmin.markmin2latex import render

def getreference(path):
    data = open(path).read().split('\n')
    d = {}
    for line in data:
        if ':' in line and not line.startswith('#'):
            items=line.split(':',1)
            d[items[0].strip()]=items[1].strip()
    return d

def assemble(path):
    path = os.path.abspath(path)
    path1 = os.path.join(path,'??.markmin')
    text = '\n\n'.join(open(f,'r').read() for f in glob.glob(path1))
    text = text.replace('@///image',os.path.join(path,'images'))
    body, title, authors = render(text)
    body = body.replace('\\section{','\\chapter{'
                        ).replace('subsection{','section{')
    bibitems = []
    for item in re.compile('\\cite\{(.*?)\}').findall(body):
        for part in item.split(','):
            if not part in bibitems: bibitems.append(part)
    bibliography = []
    for item in bibitems:
        reference = getreference(os.path.join(path,'references',item))
        bibliography.append((item,reference['source_url'])) 
    txtitems = '\n'.join('\\bibitem{%s} \\url{%s}' % item for item in bibliography)
    return HEADER + body + FOOTER.replace('@BIBITEMS',txtitems)

if __name__=='__main__':
    print assemble(sys.argv[1])
