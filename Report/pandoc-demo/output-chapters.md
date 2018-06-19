This is a demo file for pandoc-crossref. With this filter, you can
cross-reference figures (see figs. 1.1-1.3), display equations (see
eq. 2.1), tables (see tbl. 3.1) and sections (secs. 1, 2, 4.1-4.3)

For immediate example, see fig. 1

![Figure \# 1: A figure](img1.jpg){#fig:figure0}

There is also support for code blocks, for example, lsts. 4.1-4.3

It's possible to capitalize reference prefixes, like this: Fig. 1.1.

In case of multiple references, capitalization is determined by first
reference. Figs. 1.1, 1.2 is capitalized, while figs. 1.1, 1.2 is not.

It is also possible to mix different references, like fig. 1.1,
tbl. 3.1, lsts. 4.1, 4.2, figs. 1.2, 1.3, which will be grouped in order
they are specified. You can even intermix this with regular citations,
although it's not recommended: fig. 1.1, tbl. 3.1,
[@unprocessedCitation]

You can also have custom chapter reference labels, like
sec. AppA.CustLab

Subfigures are supported, see figs. 1.4, 1.4 (b)

Chapter 1. Figures {#sec:sec1}
==================

![Figure \# 1.1: First figure](img1.jpg){#fig:figure1}

![Figure \# 1.2: Second figure](img2.jpg){#fig:figure2}

![Figure \# 1.3: Third figure](img3.jpg){#fig:figure3}

![Unlabelled image](img1.jpg)

<div id="fig:subfigures" class="subfigures">

![a](img1.jpg)

![b](img1.jpg){#fig:subfigureB}

Figure \# 1.4: Subfigures caption. a — Subfigure a, b — Subfigure b

</div>

Chapter 2. Equations {#sec:sec2}
====================

Display equations are labelled and numbered

[$$ P_i(x) = \sum_i a_i x^i \qquad(2.1)$$]{#eq:eqn1}

Since 0.1.6.0 those can also appear in the middle of paragraph
[$$a x^2 + b x^2 + c = 0\qquad(2.2)$$]{#eq:quadr} like this.

Chapter 3. Tables
=================

<div id="tbl:table1">

  First Header   Second Header
  -------------- ---------------
  Content Cell   Content Cell
  Content Cell   Content Cell

  : *Table 3.1*: Table example

</div>

Table without caption:

  First Header   Second Header
  -------------- ---------------
  Content Cell   Content Cell
  Content Cell   Content Cell

Chapter 4. Code blocks
======================

There are a couple options for code block labels. Those work only if
code block id starts with `lst:`, e.g. `{#lst:label}`

`caption` attribute {#sec:caption-attr}
-------------------

`caption` attribute will be treated as code block caption. If code block
has both id and `caption` attributes, it will be treated as numbered
code block.

<div id="lst:captionAttr" class="listing haskell">

Listing 4.1: Listing caption

``` {.haskell}
main :: IO ()
main = putStrLn "Hello World!"
```

</div>

\pagebreak

Table-style captions {#sec:table-capts}
--------------------

Enabled with `codeBlockCaptions` metadata option. If code block is
immediately adjacent to paragraph, starting with `Listing:` or `:`, said
paragraph will be treated as code block caption.

<div id="lst:tableCaption" class="listing haskell">

Listing 4.2: Listing caption

``` {.haskell}
main :: IO ()
main = putStrLn "Hello World!"
```

</div>

Wrapping div {#sec:wrapping-div}
------------

Wrapping code block without label in a div with id `lst:...` and class,
starting with `listing`, and adding paragraph before code block, but
inside div, will treat said paragraph as code block caption.

<div id="lst:wrappingDiv" class="listing haskell">

Listing 4.3: Listing caption

``` {.haskell}
main :: IO ()
main = putStrLn "Hello World!"
```

</div>

Unnumbered chapter. {#unnumbered-chapter. .unnumbered}
===================

This chapter doesn't change chapter prefix of referenced elements,
instead keeping number of previous chapter, e.g.
[$$ S(x) = \int_{x_1}^{x_2} a x+b \  \mathrm{d}x \qquad(4.1)$$]{#eq:eqn2}

Chapter 5. Reference lists
==========================

It's also possible to show lists of figures and tables, like this:

\listoffigures
[]: hack to split raw blocks \listoftables
[]: hack to split raw blocks \listoflistings

Appendix A. Custom labels {#appendix-a.-custom-labels label="AppA"}
=========================

This section will have custom label {#sec:custlabs label="CustLab"}
-----------------------------------
