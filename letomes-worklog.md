# January 29, 2018)

## Møde (Poul + HH)
Meet and greet. Lidt snak om BSc projektet, om hvad målet er, og hvad evolution strategies grundlæggende er.

Før special officielt oprettes som kursus er der to ting der skal på plads:
1. Gandalf undersøger hvad reglerne er ift. forlængelse af MSc projekt når man har kurser samtidig med.
2. Titel af projekt. Vores nuværende working title er "Low Energy Transfer Orbits to Mars using Evolution Strategies" - spørgsmålet er blot om dette er generelt nok, idet vi nok også kommer til at forsøge andre metoder end kun ES. Så det kan vi vi alle tænke lidt over.

Vi foreslår et intro møde hvor alle er til stede næste uge, måske torsdag 8/2.

### Start på research af reference managers
Har før brugt Mendeley, men er ikke helt tilfreds.
Lang historie kort:
1. Håber på / sætter min lid til den kommende joint [Papers/Readcube app](http://blog.readcube.com/post/165237712272/glimpse-into-the-new-readcube-papers-app) som kan komme [når som helst](http://blog.readcube.com/post/168755698872/great-things-are-coming) nu.
2. Jeg starter nok med at bruge Papers snart, og så migrere når betaen at den nye app nævnt i punkt 1 kommer ud.
3. Kan være at jeg må falde tilbage på Mendeley hvis nævnte beta er for buggy og/eller for dårlig support af BiBTeX. Fingers crossed.


# January 31, 2018

### Reference manager decision: Mendeley
Efter en del research og trial and error endte jeg med... Mendeley. Muligheden for “Create one BibTeX file per group” i Mendeley er afgørende for mig da det betyder man kan synce .bib for hvert enkelt projekt, fx. Thesis, kun med de relevante referencer i en fil til mappen med resten af rapporten, dvs. den bliver 100% self contained selvom man bruger BiBTeX og Mendeley.

Vil nok prøve at give den nye Readcube Papers app en chance når betaen kommer, men jeg tvivl på at der er ligeså god BiBTeX support som i Mendeley, så jeg spår den ikke mange chancer. Anyway så kom der låg på det.

### Text editors
Jeg undersøgte om [Scrivener](https://www.literatureandlatte.com/scrivener/overview) eller [Ulysses](https://ulyssesapp.com) havde noget at byde på. Selvom de var interessante på hver deres måde (specielt Ulysses som jeg vil bruge til andre ting), vil jeg holde mig til [Typora](https://typora.io)/[pandoc](http://pandoc.org)/latex workflowet for specialet, evt. med [DEVONthink](http://www.devontechnologies.com/products/devonthink/devonthink-pro-office.html) for søgning og opdagelse af relationer imellem tekst dokumenter, selvom det muligvis er overkill.

Dermed har jeg blot tilbage at sætte et markdown/makefile workflow op, så er jeg klar til at skrive. Kan altid finde en LaTeX template senere. Det gør jeg bare når det lige passer mig.

# February 1, 2018

### Git client: Tower
Jeg har konkluderet at jeg godt kunne bruge en Git klient med lidt flere features, og er endt på [Tower](https://www.git-tower.com/). Så skulle have sat mig i den, men brugte en del tid på at læse deres [blog](https://www.git-tower.com/blog/home) i stedet. De har mange gode artikler og tips. Jeg vil dog ikke bruge mere arbejdstid på denne blog, men må sætte mig ordentligt ind i programmet ved lejlighed.

### Hazel script til automatisering af .bib fil kopiering fra Mendeley
Dernæst færdiggjorte jeg mit Mendeley workflow ved at sætte to [Hazel](https://www.noodlesoft.com) script op som:
1. Automatisk flytter alle (PDF) filer fra min `Mendeley Watched Folder` ind i en backup folder efter de har været der i 1 minut (Mendeley importerer filer fra watched folder ind i library, men lader dem ligge, hvilke kan blive lidt rodet).
2. Automatisk kopierer .bib filen tilhørende thesis projektet ind i thesis mappen, således at jeg altid har en up-to-date kopi af .bib filen i thesis Github repo, så alt er nicely self contained.

Af mine værktøjsmæssige forberedelser mangler jeg nu:
1. Sætte mig færdigt ind i Tower
2. Sætte mit Typora/pandoc workflow fuldt op til indskrivningen. Så skriver jeg specialet i Markdown, og kan let konvertere til .tex, .pdf, .html, og endda .doc (*gys*), bl.a. Jeg brugte dette workflow i min LearningTech rapport sidste semester, og fandt det glimrende.

Efter jeg har gjort dette, tager jeg parallelt fat på:
1. Gennemlæsningen af BSc projekt + færdigskrivning af artikel over denne
2. Grundig læsning af artikel [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://arxiv.org/abs/1703.03864)