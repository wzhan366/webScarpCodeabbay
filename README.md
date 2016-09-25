# Web Scarp - Codeabbay

This one is just try to scarp the problmes which I practiced on codeabbay.
Then, print them out for review and make notes.

## Idea
- Get problem names. I get the solved problem name list from my profile and store it in a txt file.
- Scrap each problem page using their name. 
- Convert Scarped html files to pdf files
- Merge pdf files

- Tags. I also scarp tags of each problem to see which type problem I'm good at and which type I'm not

## Key step or tool
### Step
-Xhtml2pdf error. 
    The xhtml2pdf library has some handler error, you should use this code to avoid it:

>    import logging
>   class PisaNullHandler(logging.Handler):
>        def emit(self, record):
>           pass
>    logging.getLogger("xhtml2pdf").addHandler(PisaNullHandler())
'''

-Where to parse
    We use the class name of table tag to locate the table and parse info of table.

### Tool
- Scrap tool, beautiful soup 
- PDF convert, xhtml2pdf


