# July 12, 2018
## Refactored symplectic ligning + Git LFS snask
Startede med at omskrive symplectic ligning lidt, så vi ikke bliver bidt af det igen, som forberedlese til simplificering af den del af koden. Dagen blev lidt derailed af at vi begge havde git problemer. Vores indførelse af LFS til PDF filer for chapters gav nogle obskure problemer. Gandalf gjorde det forfra i command line og nu virker det tilsyneladende fint.

# July 11, 2018 
## Pair-programming: forståa sympletic funktionen i bsc-koden
Har brugt en del af dagen på at forstå symplectic funktionen i symplectic.py hvor det meste af logikken sker. Dette er relevant både ift. at implenetere ES i bsc-koden og den nye pagmo basererede kode.

## Debugger helvede
Vi rodede begge lidt med at få debuggeren til at køre i VSCode. Gandalf konkluderede at debuggeren i VSC tager 27 sekunder om at starte på bibliotekets computere. P-hands. Vil prøve at køre det ud af C: drevet (lokalt) i stedet for L: drevet (netværk) i morgen, men er ikke forhåbeningsfuld. 

## Pandoc virker endelig på windows også
Halleluja.

# July 10, 2018
## Moon code overblik
Gandalf og Oisin har pair programmeret i dag. Specifikt har vi kørt koden igennem lidt birds-eye view, hvorefter vi har fokuseret på "The business end", altså solverne og søgealgoritmen. Vi har i den process fundet en fortegnsfejl i implementeringen af Hamilton-ligningerne, der har introduceret en fejl på ca. en procent i BSc bevægelsesligningerne. Værd at sende et addendum ud til alle de stakkels videnskabsfolk der bruger de resultater som hjørnesten i deres egne projekter. Der er garanteret millioner af ERC penge på spil.

# July 9, 2018
## MikTeX portable + pandoc bug time wasting
Har ikke kunne compile mit afsnit fordi MikTeX er outdated, så har bare smadret rundt i at få en portable version til at virke. Endte med at lave en form for alias i powerscript profile + compile den seneste version af pandoc fordi der åbenbart er [en bug](https://github.com/jgm/pandoc/issues/4681) i seneste release mht. absolute path på `--pdf-engine` argument.  FML, i morgen stikker Oisin og jeg hovederne sammen og laver noget actually worthwhile.

## report -- Oisin
Jeg har skrevet halvanden sides penge om Salimans-NES og dets forskelle fra andre ES typer, samt lidt opdateret info om hvordan pagmo er integreret i vores løsning. Mht. ES, bør jeg nok tilføje lidt om ES vs helt andre algoritmer, og hvordan de opfører sig på forskellige problemtyper.

Har ifm. ovenstående læst nærmere på Salimans ES paper, og føler at have dybnet min forståelse for det underliggende optimeringsproblem. Jeg har altid haft svært ved at forstå concepter kommunikeret udelukkende vha. formel logik, så jeg har fundet en metafor der gør mig glad. Den er skrevet i rapporten.

# July 6th
## Pagmo -- Oisin
Jeg har implementeret Karpathy/Salimans ES i pagmo, så den er trivielt paralleliserbar. Kører pænt på den lokale maskine. Kører også på HPC, men lidt skrabet. Jeg kunne virkelig godt tænke mig en måde at vise plots fra HPC runs på en måde der ikke involverer at gemme en lokal fil og hente den via scp (-_-)

Næste trin er at smide noget jord-måne simulering ind i det problem vi løser (lige nu er det et toy problem space: et sortiment af gaussians). Det bliver velsagtens noget med at kopiere Gandalf's gamle kode ind i mit framework. Tentativ deadline for det er sat i slutningen af næste uge.

## Gandalf: Visual Studio Code indføring
Grundet at værkstedsbesøget for min Macbook Pro trækker ud, har jeg hele ugen været nødsaget til halvt at bruge tiden på at sætte værktøjer op på windows maskinerne i biblioteket. Jeg troede jeg var færdig, men i dag gik det op for mig at jeg ikke har PyCharm til rådighed, og SublimeText kan ikke debugge ordentligt. Så jeg brugte dagen på at sætte mig grundigt ind i VSCode, som hermed er blevet min nye editor of choice.

# July 5th, 2018
## Projekt Roadmap
Oisin og jeg har lavet et detaljeret roadmap for resten af måneden i Asana, kan ses her:  https://app.asana.com/0/732675643618740/timeline

## Gandalf: ES Openai blog + kode eksempler kørt igennem
I dag kørte jeg [Karparhy's natural ES eksempel](https://github.com/karpathy/randomfun/blob/master/es.ipynb) igennem med 2D hillclimbing (og fandt også et par [småfejl](https://github.com/karpathy/randomfun/pull/3) i den. I morgen starter jeg på at kigge på at få det ind i R3B moon koden.

# June 29, 2018
##  Møde (OW+GS+ODK)
###  Paperen Izzo2018 (Machine learning and evolutionary techniques in interplanetary trajectory design)
Vi snakkede om hvad det er de egentlig har gjort:
1. Regne nogle optimale baner ud med control theory
2. Generere et træningssæt ved at lave noget random walk rundt om de optimale baner, og gemme dataen om forskellen i delta-v osv.
3. Bruge de generede træningssæt til at træne et ret standard feed-forward neuralt netværk til at lære de optimale kontinuerte input $u(t)$ .
Vi skal holde fast i den oprindelige plan med at lave ES på interplanetary transfers, og også overveje at køre det hele med egen kode; behøver vi PyKEP til dette? Er der nogen grund til at vi ikka kan gemme relevante planeters bevægelse i en slags tabel, og så have en simpel simulator, og fokusere vores energi på at optimere inputs til denne simple simulator?

### Egen simulator til Mars?
1. Er der nogen grund til at conic patched comic sections osv.? Kan vi ikke bare løse systemet af Newton's 2. lov numerisk? Hvorfor have de her 3 legeme systemer som skal strikkes sammen?

Vi nok vil bevæge os i retning af at lave vores egen simulator nu.

# June 28
##  Gandalf: opsummering af seneste uger (pandoc/LaTeXTypora)
Da jeg er 95% færdig med det jeg har brugt det meste tid på de seneste par uger, venter jeg lige til jeg er helt færdig. Jeg har imidlertid lige skiftet fokus nu, dels fordi jeg lige skulle catche up med et paper inden et Ole møde, og dels fordi min computer skal til reperation i et par dage. Men jeg skriver snart en log af hvad der er sket.
## Tsiolkovsky's rocket equation
Har fulgt og selv genopskrevet to udledninger af denne vigtige ligning:
$$
\Delta v = v_e \ln{\frac{m_0}{m_f}}
$$
hvor $\Delta v$ er ændring i fart af raket, $v_e$ er udstødningshastigheden i rakettens system, $m_f$ er rakettens masse efter udstødning, $m_0$ er rakettens masse før udstødning.

[Wiki](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation)

## Specific impulse
Et mål for hvor effektiv en raket er ift. massen/vægten af dets brændstof. Fra [wikipedia](https://en.wikipedia.org/wiki/Specific_impulse):
> Specific impulse (usually abbreviated Isp) is a measure of how effectively a rocket uses propellant or jet engine uses fuel. By definition, it is the total impulse (or change in momentum) delivered per unit of propellant consumed and is dimensionally equivalent to the generated thrust divided by the propellant mass flow rate or weight flow rate.

Og denne grundlæggende relation:
$$
F_\text{thrust} = g_0 \cdot I_\text{sp} \cdot \dot m,
$$
Hvor F_{thrust} er fremdriftskraften, $g_0$ er tyngdeacceleration, $I_{sp}$ er den specifikke impuls og $\dot m$  er massetabsraten.

# June 12
## pykep/pygmo
Oisin: Reading docs for pykep and pygmo, forked pykep to make some changes to the plotting functionality. Figure that might be useful later as well. Posted some questions for next meeting. I really want to get to implementing our own ES-algorithm, though pygmo has a very nice CMA-ES that looks like it might do what we need outta the box.

## hpc
Oisin: Yesterday, I got HPC@DTU to run my initial experimentation-code, and it took us to mars nicely. Made a branch for HPC@DTU adventures, but i rebased that back onto master again today.

# June 9, 2018
## LaTeX stuff...
Gandalf: Har bare læst op på LaTeX packages og videreudforsket Typora+pandoc>LaTeX worketflowet yderligere.

# June 8, 2018
## EJP LaTeX requirments...
Gandalf brugte dagen på at sætte sig ind i EJPs (European Journal of Physics) LaTeX requirements, så de bliver glade første gang vi submitter og forhåbenligt ikke behøver nogen formaterings-mæssige rettelser.


# June 7, 2018
## Not much...
Gandalf: For mig ikke en særlig produktiv dag. Bøvlede med nogle Mac high-cpu process problemer, og kom ikke så meget videre.


# June 6, 2018
## At få BSc koden til at køre igen
Gandalf: Den gamle kode kører fint. Har i hvert fald kørt nogle gemte baner, og de kører fint og giver figurer. Prøver en søgning i morgen eller fredag. Numbapro var blevet discountinued, men er blevet FOSS med numba, så np. Kun få til skulle ændres for at det virkede.

Har kigget lidt på noget teori, og ting til mødet i morgen, nu i Asana meeting noterne.

# June 5, 2018
## PyKEP
Oisin has been looking at defining custom problems with Pagmo (solver for PyKEP), and at migrating to hpc@dtu. Docker is not available on hpc@dtu, so we'll have to set up a more custom environment. Little experiment notebook added to repo, requires PyKEP installed.
## Paper LaTeX stuff
Fiksede bare en masse problemer i LaTeX kildekoden for paperen i dag, og fik reduceret antallet af errors far ~50 til ~30. Undervejs opdagede jeg dog at vi har brug den forkerte template (my bad!), og det ser umiddelbart ud som om at den rigtige template fra European Journal of Physics er 1-column, ikke 2-column, hvilket formegentlig betyder at jeg ikke havde behøvet at fikse figurene. Oh well... vi får se når vi først har fået oprettet paperen som den rigtige article type og jeg får kigget på den endelige LaTeX template.

# June 4, 2018
## Projekt status
Første fælles Thesis work session i 2 måneder. Oisin og Gandalf snakker om status for projektet, og opdaterer Asana.

## PyKEP
Ret kraftigt program. Outputter nogle pæne baner i et 3D plot og alt muligt! Har nogle predefinerede missiontyper (gravity assist + single deep space maneuver) som er helt kriminelt nemme at have med at gøre 

(groft sagt: **goto([earth, mars, earth])**).

Kan oven i købet finde dem med et utal af søgemetoder, bl.a. CMA-ES, der er tangentielt relateret til Salimans etal.. 

Muligheder for at lave helt custom missionstyper, som Oisin vil kigge på i morgen. Open source.

## Paper progress
Paper printet ud og gennemlæst -> nye rettelser. Gandalf begyndt at fikse figurer.

# March 19, 2018
## Møde (Poul+Oisin)
Snakkede lidt om det hele og fik Oisin up to speed.

## PyKEP og Docker
Oissin og Gandalf sad resten af eftermiddagen og kæmpede med installation af [PyKEP](https://esa.github.io/pykep/) og Docker image.
PyKEP virker som en mulighed ift. at bruge et eksisterende library, så vi vil gerne prøve det lidt af så vi kan tage stilling til om vi skal lave vores egen simulering eller ej. Det virker umiddelbart lovende.

# March 9, 2018
* Har sat et repostory op for gammelt BSc projekt + oprettet Asana workspace så vi alle kan samarbejde bedre, specielt nu hvor Oisin også er med.
* Har rodet med noget LaTeX teknisk omkring farver som jeg brugte til Pouls svar i poul-q.pdf

# March 8, 2018
## Møde (Poul)
Vi snakkede om mine spørgsmål fra poul-q.pdf som tidligere sendt ud på mail, samt øvrige spørgsmål. Jeg har fået anbefalet at tjekke følgende ud af en ven fra Caltech (Casey Handmer, som nu er "levitation engineer" hos Hyperloop One):
- [ ] [PyKEP](https://esa.github.io/pykep/) - Et open source python bibliotek fra ESA til orbit simulering i solsystemet, implementeret i C++ med python interface og mange bells and whistles.
- [ ] [Porkchop plots](https://en.wikipedia.org/wiki/Porkchop_plot)
- [ ] [Lambert's problem / algorithm](https://en.wikipedia.org/wiki/Lambert%27s_problem)

Casey's fulde besked:
> I only just started work on this problem and its slow progress. 
The short answer is PyKEP. 
The long is that traditional porkchop plots are done with Lambert's algorithm, but they tend to break if there's too much plane involved. Damon Landau at JPL has been working this problem too.
I'm currently traveling, but please update me next week on my gmail?

Jeg lægger snart en poul-q.pdf opdateret med Pouls svar op.

# March 1 + March 4 + March 5 + March 7 ,2018
## BSc gennemlæsning
Alle disse dage arbejdede jeg kun sparsomt og lidt ufokuseret, men på det samme: gennemlæsning af BSc projekt, overførsel af materiale til paper på ShareLaTeX med HH o Poul, og rettelse af småfejl / gen-forståelse af alt undervejs.

# February 28, 2018
Har læst en del om blandede orbital mechanics emener i dag:
* Interplanetary Transport Network (ITN)
* Sphere of influence
* Hill sphere
* Roche lobe
* Lagrange points
* Halo orbits
* Lissajous orbits
* Genudledt nogle basic udtryk (escape velocity, geostationary orbit)

# February 26, 2018
tl;dr:
* Videre med BSc gennemlæsning / paper.
* Lærte programmet Sketch at kende, rettede en figur.

Kom et stykke videre i gennemlæsning og gen-håndregning af BSc rapport, samt paper skrivning.

Fandt en lille fejl i en figur, og prøvede at åbne den i Inkscape for at rette. Kunne ikke få Inkscape til at virke indenfor de første 30 min på min Mac. Brugte en del tid på at lære et andet vektortegningsprogram at kende, Sketch, som jeg har haft liggende på min Mac et stykke tid. Så nu er jeg i det mindste rustet til at lave flere fine vektor grafik figurer manuelt, hvis det bliver nødvendigt (afhængigt af omstændighederne vil jeg selvfølgelig også overveje TikZ).

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