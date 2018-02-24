# February 22, 2018
Er begyndt grundig gennemlæsning af BSc rapport, og gennemgår de vigtigste udregninger i hånden igen.

# February 15, 2018
Jeg vil nu som noget nyt begynde at skrive tl;dr (Too Long; Didn't Read) opsummeringer øvert i hver worklog entry, så man kan få et hurtigt overblik, og ikke vil læse det hele i detaljer.

tl;dr
* Møde med HH, lidt snak om intuition omkring transfer orbits til Mars, samt lidt tilbageblik på BSc projekt.
* Har brugt en god del af dagen på at undersøge Python IDEs fordi Python plots i eksterne vinduer er en forfærdelig oplevelse. Jeg er endt på PyCharm Pro pga. dens "Scientific View", som er helt genialt.

## Møde (HH)
HH og jeg snakkede lidt om forskellige intuition omkring hvilke transfer orbits der kunne være interessante at kigge på, og jeg kom i tanke om at jeg havde lavet noget Hohmann transfer mellem jordne og Mars analytisk på i Ae105 kurset på Caltech, som jeg vil genopfriske og præsentere ved næste møde eller næste igen.

Jeg laver et udkast til en projektbeskrivelse og projektplan vel inden torsdag, og lægger op i repo (skal nok sende en email ud).

###  Old code + Python IDE: PyCharm Pro
Jeg beggyndte at kigge på den den gamle BSc kode, og blev igen mindet om hvor utrolig nedern det er med figurer på popper up bagved editoren osv. Jeg brugte SublimeText + Terminal dengang, men jeg besluttede mig for at prøve noget andet.

* **Spyder:** Har brugt det lidt som hjælpelærer, og det har to store styrker: integrerede plots og variable explorer (og basic debugging tools). Men der er ret _wonky_ som applikation, og på mange måder ikke særlig lækkert at bruge.
* **PyCharm:** Full-stack development IDE, som jeg før har snuset til, men synes var for stort / tungt at danse med (ligesom Eclipse). Jeg har dog til min store glæde fundet ud af at PyCharm Pro (som kan fås med educational license). Så kom der styr på en ting mere.

# February 8, 2018

## Møde (Poul + HH + Ole)
Første fællesmøde med alle vejledere.
Alle enige om at projektet er sjovt og højaktuelt med tirsdagens Falcon Heavy launch og Tesla Roadsteren i orbit.

* High-level diskussion af projektet.
* Gandalf vil udarbejde et udkast til en skitse til en projektplan, præsentere til HH i næste uge.
* Poul vil undersøge mere om hvordan man traditionelt laver baner til Mars.
* Ole foreslår at vi holder fast i månen, og måske først tester en ES algoritme på den før vi tager fat i Mars. Alle er enige om at prøve af på månen først, og at det interessante mål stadig er at komme til Mars.
* Det diskuteres om hvordan Asteroidebæltet håndteres i modellen. Ole foretog en hurtig Google søgning, der tyder på at asteroidebæltet er meget tyndt 'befolket' med asteroider, og at man sandsynligvis derfor kan se bort fra det. Gandalf og Poul vil undersøge endelig bekræftelse. Alternativt kan man altid lave en orbit en smule ude af planen af solsystemet.
* Gandalf og Poul vil færdiggøre artikel som i bund og grund er BSc projektet kogt ned i en kort artikel, og dermed også få repeteret BSc projektet i samme hug.
* Ole foreslår at jeg Googler "variational optimization" som endnu en mulig søgningsmetode.


# February 7, 2018

### Tower / Git studier done
Jeg lærte et par nyttige ting undervejs:
#### Git LFS (Large File Storage)
Hvis man har meget store binære filer i sit repo som ændrer sig en smule hele tiden, kan det give et meget stort repository size meget hurtigt fordi git lagerer en komplet kopi af alle versioner af de binære filer.
Dette kan løses, i hvert fald delvist, med Git LFS. Det gar i korte træk ud på at man dropper kravet om at gemme alle versioner af en bestemt fil / mappe / file extension / filename pattern *lokalt* men kun have de filer liggende lokalt som skal bruges i den nuværende revision. Alle versioner af store filer markeret til LFS ligger stadig på remote server (i LFS Store) men lokalt ligger alle version af filerne kun som *pointere* til remote LFS Store, og kun filer som skal bruges i den nuværende checked out version, er downloaded lokalt. Dvs. det løser problemet lokalt, dog vil alle versioner af store filer stadig ligge på remote server. Good to know.
Gode forklaringer:
* https://www.git-tower.com/learn/git/ebook/en/command-line/advanced-topics/git-lfs#chapter_installing+git+lfs
* https://www.atlassian.com/git/tutorials/git-lfs
* https://www.youtube.com/watch?time_continue=16&v=9gaTargV5BY
#### Git Submodules
Ofte vil man gerne inkludere eksterne biblioteker og andre resourcer. Man kan selvfølgelig downloade disse og kopiere dem ind i ens eget projekt. Der er to problemer med dette:
1. Man blander ekstern kode med ens egen unikke kode / projekt filer, men det er mere clean at holde disse ting adskildt, specielt hvis man skal dele koden udadtil med resten af verden senere.
2. Hvis det eksterne bibliotek bliver opdateret (med fx. bugfixes eller nye features), er det ret bøvlet at opdateret dette biblioteks kode i ens eget repo; igen er vi nødt til at hente de rå filer, og overskrive de gamle filer.

Submodules gør det muligt at have et "git repo indeni et git repo" således at det interne repo (kaldet et submodule), ikke bliver tracket af parent repo, men at de holdes som to separate git repos selvom det ene ligger indeni det andet. Det er dog stadig nemt at holde de interne submodule opdateret.
En vigtig forskel fra normale git repos og submodule repos er at submodules altid peger på en bestemt commit, snarere end en bestemt branch. Dette er fordi at submodules ofte bruges til eksterne libraries som man ikke vil have ændrer sig så ofte, medmindre man manuelt gør det.

God forklaring på:
* https://www.git-tower.com/learn/git/ebook/en/desktop-gui/advanced-topics/submodules

### .bib file citekeys (evt. via Alfred workflow)
Jeg har søgt forgæves på nettet efter et Alfred workflow der kan lave autocompletion og insertion af BibTeX citekeys fra en .bib fil ind i et tekstfelt med formatering fx. [@Newton], som bruges i pandoc / pandoc-citeproc. Grunden til at jeg kunne bruge dette er at Typora (min primære markdown editor), desværre ikke understøtter autocompletion / suggestion af citekeys fra en .bib fil, som mange dedikerede LaTeX editorer og LaTeX pakker til populære text editors (fx. LaTEXTools til SublimeText), gør det. Det betyder at jeg 100% manuelt skal sidde og skrive alle citations uden ind nogen hjælp, hvilket er en smule træls, men noget jeg må leve med hvis det er, for jeg kan godt lide Typora/Markdown/pandoc workflowet fremfor det rene LaTeX workflow.

Efter at have søgt Google, har jeg oprettet en [issue](https://github.com/andrewning/alfred-workflows-scientific/issues/9) på denne persons Github repo for et Alfred workflow, samt oprettet [dette](https://www.alfredforum.com/topic/11223-autocompletion-references-from-bib-file/) forum indlæg på alfredforum.com. Mere kan jeg ikke gøre foreløbigt.

PS: Jeg arbejde ikke på thesis i mandags (February 5) da jeg havde brug for at arbejde på AI i stedet der.

# February 4, 2018

### Tower (git client) familiarisering
I dag var ren studie af Tower, hvor jeg gjorte mig bekendt med programmet, og har fulgt deres [video læringsmateriale](https://www.git-tower.com/learn/git/videos), som jeg er ca. halvt færdig med.

# February 1, 2018

### Git client besluttet: Tower
Jeg har konkluderet at jeg godt kunne bruge en Git klient med lidt flere features, og er endt på [Tower](https://www.git-tower.com/). Så skulle have sat mig i den, men brugte en del tid på at læse deres [blog](https://www.git-tower.com/blog/home) i stedet. De har mange gode artikler og tips. Jeg vil dog ikke bruge mere arbejdstid på denne blog, men må sætte mig ordentligt ind i programmet ved lejlighed.

### Hazel script til automatisering af .bib fil kopiering fra Mendeley
Dernæst færdiggjorte jeg mit Mendeley workflow ved at sætte to [Hazel](https://www.noodlesoft.com) script op som:
1. Automatisk flytter alle (PDF) filer fra min `Mendeley Watched Folder` ind i en backup folder efter de har været der i 1 minut (Mendeley importerer filer fra watched folder ind i library, men lader dem ligge, hvilke kan blive lidt rodet).
2. Automatisk kopierer .bib filen tilhørende thesis projektet ind i thesis mappen, således at jeg altid har en up-to-date kopi af .bib filen i thesis Github repo, så alt er nicely self contained.

Af mine værktøjsmæssige forberedelser mangler jeg nu:
1. Sætte mig færdigt ind i Tower.
2. Forsøge et [Alfred](https://www.alfredapp.com) workflow hvor jeg kan indsætte citeringer direkte fra Alfred.
3. Forsøge et Alfred workflow hvor jeg kan køre terminal command direkte på den åbne mappe i Finder.
4. Sætte mit Typora/pandoc workflow fuldt op til indskrivningen. Så skriver jeg specialet i Markdown, og kan let konvertere til .tex, .pdf, .html, og endda .doc (*gys*), bl.a. Jeg brugte dette workflow i min LearningTech rapport sidste semester, og fandt det glimrende.

Efter jeg har gjort dette, tager jeg parallelt fat på:
1. Gennemlæsningen af BSc projekt + færdigskrivning af artikel over denne
2. Grundig læsning af artikel [Evolution Strategies as a Scalable Alternative to Reinforcement Learning](https://arxiv.org/abs/1703.03864)

# January 31, 2018

### Reference manager decision: Mendeley
Efter en del research og trial and error endte jeg med... Mendeley. Muligheden for “Create one BibTeX file per group” i Mendeley er afgørende for mig da det betyder man kan synce .bib for hvert enkelt projekt, fx. Thesis, kun med de relevante referencer i en fil til mappen med resten af rapporten, dvs. den bliver 100% self contained selvom man bruger BiBTeX og Mendeley.

Vil nok prøve at give den nye Readcube Papers app en chance når betaen kommer, men jeg tvivl på at der er ligeså god BiBTeX support som i Mendeley, så jeg spår den ikke mange chancer. Anyway så kom der låg på det.

### Text editors
Jeg undersøgte om [Scrivener](https://www.literatureandlatte.com/scrivener/overview) eller [Ulysses](https://ulyssesapp.com) havde noget at byde på. Selvom de var interessante på hver deres måde (specielt Ulysses som jeg vil bruge til andre ting), vil jeg holde mig til [Typora](https://typora.io)/[pandoc](http://pandoc.org)/latex workflowet for specialet, evt. med [DEVONthink](http://www.devontechnologies.com/products/devonthink/devonthink-pro-office.html) for søgning og opdagelse af relationer imellem tekst dokumenter, selvom det muligvis er overkill.

Dermed har jeg blot tilbage at sætte et markdown/makefile workflow op, så er jeg klar til at skrive. Kan altid finde en LaTeX template senere. Det gør jeg bare når det lige passer mig.

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

# Ordliste
ES = Evolution Strategies