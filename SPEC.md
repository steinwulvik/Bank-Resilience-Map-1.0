# Bank Resilience Map
## Kravspesifikasjon – versjon 1.0

## 1. Kort om konseptet

Bank Resilience Map er en interaktiv demonstrator for å forstå hvordan bankens viktige tjenester avhenger av interne systemer og eksterne IT-leverandører. Brukeren kan simulere en driftsforstyrrelse og se hvilke tjenester som kan bli påvirket, hvilke avhengigheter som må undersøkes, og hvilke oppfølgingsoppgaver som bør vurderes.

Demonstratoren bruker oppdiktede banker, systemer, leverandører og hendelser. Den viser en arbeidsflyt og et produktkonsept, og gir ikke en formell risikovurdering eller dokumenterer faktisk DORA-etterlevelse.

## 2. Målbilde for sluttproduktet

Bank Resilience Map skal være et arbeidsverktøy som gir bankens ansatte et oppdatert, etterprøvbart bilde av hvordan kritiske tjenester avhenger av teknologi, interne team og eksterne leverandører. Når en forstyrrelse oppstår – eller når banken planlegger en endring – skal brukeren kunne gå fra et forretningsmessig spørsmål til en forståelig konsekvensanalyse og videre til koordinert oppfølging.

Sluttproduktet skal gi brukeren denne sammenhengende opplevelsen:

1. **Forstå utgangspunktet:** Se kritiske banktjenester, eiere, driftsstatus, gjenopprettingsmål og datadekning i en samlet oversikt.
2. **Utforske avhengigheter:** Følge en tjeneste gjennom applikasjoner, infrastruktur, dataflyt, interne team og leverandører. Hver relasjon skal ha kilde, eier og sist bekreftet dato.
3. **Vurdere endring eller hendelse:** Velge en faktisk hendelse eller planlagt endring og angi omfang, varighet, område og berørte komponenter.
4. **Se konsekvenser og usikkerhet:** Se direkte og indirekte påvirkning på tjenester, kanaler og kundereiser. Resultatet skal vise hva som støtter vurderingen, hva som er antatt, og hvor bildet er ufullstendig.
5. **Koordinere respons:** Følge opp oppgaver med ansvarlig rolle, frist og status, og føre en tidsstemplet beslutningslogg.
6. **Dokumentere og lære:** Eksportere en sporbar oppsummering og registrere forbedringstiltak etter hendelsen.

Et produksjonsprodukt skal kunne hente informasjon fra bankens autoritative kilder for tjenestekatalog, system- og ressursdata, leverandørregister, overvåking og hendelseshåndtering. Integrasjoner skal vise dataeier, oppdateringsstatus, tilgang og feilhåndtering. Manglende eller utdaterte data skal aldri se ut som et komplett risikobilde.

Demonstratoren er et avgrenset, syntetisk uttrykk for dette målbildet og er ikke et produksjonsklart produkt.

### 2.1 Selvbetjent demonstrasjon

Demonstratoren er en offentlig webapp med en stabil lenke. En besøkende skal kunne åpne lenken og forstå verdien uten at noen viser appen:

- Introsiden forklarer kort hvilket bankproblem appen belyser, hvem den er laget for, og hva demonstrasjonen viser. Den har ingen menyfaner, og en synlig «Gå til demoen»-knapp nederst starter eksempelbank-flyten uten konto eller personlig informasjon.
- Demoen starter i Scenario. Hovedflyten navigeres med trinnene 1–4: Scenario, Påvirkning, Hendelsesrom og Rapport.
- Avhengighetskartet ligger i Påvirkning, med Kart som standardvisning og Liste som alternativ. Objektene i kartet kan klikkes, og detaljene vises under kartet.
- «Tjenesteoversikt» og «Om demoen» ligger som lenker øverst til høyre ved «Nullstill demo». Tjenesteoversikten er det eneste stedet som viser alle tjenestene i normal drift og datadekningen samlet. Sidene har en lenke tilbake til flyten.
- Brukeren kan nullstille scenarioet og komme tilbake til en forståelig standardvisning.
- Et banner øverst på alle sider sier «Demonstrasjon med syntetiske data · Uavhengig konseptdemo». Appen nevner ingen navngitte selskaper.
- Grensesnittet finnes på norsk og engelsk, med språkvelger.
- Appen er responsiv, tilgjengelig og tåler direkte åpning av lenke og oppfrisking av siden.
- Demoen samler ikke inn besøksdata og har ingen ekte bankintegrasjoner.

Eventuelle reelle bankdata, integrasjoner, brukeradministrasjon eller interne arbeidsflyter krever separat tilgangsstyring og sikkerhetsdesign før produksjonsbruk.

### 2.2 White-label-merkevare

Demonstratoren bruker den fiktive banken **Morild Bank** som white-label-kunde. Bankens merkevare er synlig i produktgrensesnittet, mens Bank Resilience Map beskriver produktkonseptet bak løsningen. Morild Bank er oppdiktet og framstilles ikke som en faktisk bank eller kunde av noen leverandør.

Logoen består av tre blågrønne bølger med samme farge, et ravgult lyspunkt og ordmerket «MORILD BANK», der «MORILD» har bølgenes blågrønne farge og «BANK» er ravgult.

![Morild Bank-logo](morild-bank-wordmark-color.png)

## 3. Problem og begrunnelse

Banker driver stadig flere kritiske tjenester gjennom digitale systemer og eksterne leverandører. Det kan være krevende å få ett samlet bilde av avhengigheter, konsekvenser og gjenopprettingsarbeid når en komponent svikter. ECBs tilsynsprioriteringer peker blant annet på tredjeparts- og skyrisiko, hendelseshåndtering, cybersikkerhet, endringsstyring og svakheter i risikodata og rapportering.

Konseptet viser hvordan et visuelt avhengighetskart kombinert med scenarioanalyse kan gjøre dette arbeidet mer oversiktlig.

Kilder:

- [ECB – Supervisory priorities 2026–28](https://www.bankingsupervision.europa.eu/framework/priorities/html/ssm.supervisory_priorities202511.en.html)
- [ECB – Supervisory priorities 2025–27](https://www.bankingsupervision.europa.eu/framework/priorities/html/ssm.supervisory_priorities202412~6f69ad032f.en.html)

## 4. Produktmål

Demonstratoren skal:

1. Gjøre avhengigheter mellom banktjenester, systemer og leverandører forståelige.
2. La brukeren velge en simulert hendelse og se mulige konsekvenser på tvers av avhengighetskjeden.
3. Samle hendelsesstatus, beslutninger, ansvar og oppgaver i én kortfattet, oversiktlig, konkret og lesbar arbeidsflate.
4. Vise hvor datagrunnlag eller dokumentasjon mangler, uten å late som usikkerhet er bekreftet risiko.
5. Være selvforklarende, slik at den kan forstås uten presentatør.

## 5. Utenfor omfang

Demonstratoren skal ikke:

- kobles til reelle banker, kontoer, produksjonssystemer eller leverandør-API-er
- inneholde ekte kunde-, transaksjons-, sikkerhets- eller personopplysninger
- foreta automatisk risikoklassifisering eller hevde DORA-etterlevelse
- erstatte bankens beredskaps-, CMDB-, GRC-, overvåkings- eller hendelsessystemer
- utføre endringer, omstart eller failover i faktiske systemer
- la brukeren endre avhengighetskartet

## 6. Brukere og hovedoppgaver

**Primær bruker:** Operativ risiko- eller teknologimedarbeider som undersøker en mulig driftsforstyrrelse.

**Sekundære brukere:** Beredskapsleder, tjenesteeier, leverandøransvarlig eller leder som trenger et raskt konsekvensbilde.

Hovedoppgaver:

- finne en kritisk tjeneste og forstå hva den er avhengig av
- velge en hendelse, for eksempel bortfall hos skyleverandør eller feil etter systemendring
- undersøke hvilke tjenester og kanaler som kan rammes
- følge anbefalte kontrollspørsmål og registrere beslutninger
- se hvem som har ansvar for oppfølging, og hva som gjenstår
- lage en kort rapport med scenario, antakelser, påvirkning og tiltak

## 7. Demonstratorflyt

1. Brukeren åpner introsiden og går til demoen.
2. Brukeren velger scenario: **Svikt hos leverandør** (hovedscenario) eller **Feil etter systemendring**, og hvilken leverandør eller hvilket system som feiler. Berørte land er forhåndsbestemt av leverandøren.
3. Brukeren velger alvorlighet og varighet og beregner påvirkningen.
4. Påvirkning viser sammendrag og kartet, der direkte og indirekte avhengigheter er farget etter tilstand. Påvirkningen forklares som en beregnet demonstrasjon basert på oppgitte relasjoner.
5. Brukeren åpner et objekt for å se avhengighetskjede, eier, gjenopprettingsmål og datamangler.
6. Hendelsesrommet viser status, oppgaver, beslutningslogg, konsekvenser, kontrollspørsmål og tidslinje.
7. Brukeren kan vise og skrive ut en demonstrasjonsrapport.

## 8. Produktkrav

«Målbilde» viser hvilken del av brukeropplevelsen i §2 kravet støtter. «Demonstratorens bevis» viser hvordan demonstratoren oppfyller det.

| ID | Sluttproduktkrav | Målbilde | Demonstratorens bevis | Prioritet |
|---|---|---|---|---|
| P-01 | Tjenester, systemer, team og leverandører skal ha synlig eier og kritikalitet | 1–2 | Syntetisk tjeneste- og avhengighetsregister | Må |
| P-02 | Avhengigheter skal kunne utforskes begge veier og vise kilde og aktualitet | 2 | Navigerbart kart med relasjonsmetadata | Må |
| P-03 | Analyse skal vise direkte og indirekte påvirkning på tjenester og kanaler | 3–4 | Forklarbar grafberegning for to scenarioer | Må |
| P-04 | Resultatet skal skille fakta fra antakelser, mangler og usikre relasjoner | 4 | Merking av syntetiske, antatte og manglende data | Må |
| P-05 | Hendelser og planlagte endringer skal kunne følges gjennom status og tidslinje | 3, 5 | Simulert hendelsesrom | Må |
| P-06 | Oppfølging skal ha ansvarlig rolle, frist, status og beslutningsgrunnlag | 5 | Oppgaver i demoen, uten ekstern arbeidsflytintegrasjon | Bør |
| P-07 | Beslutninger og endringer i vurderingen skal kunne etterprøves | 5–6 | Tidsstemplet demonstrasjonslogg | Bør |
| P-08 | Rapport skal oppsummere omfang, påvirkning, datagrunnlag, usikkerhet og tiltak | 6 | Utskrivbar rapport | Bør |
| P-09 | Data skal komme fra autoritative kilder med eierskap, tilgang og oppdateringsstatus | Sluttproduktfundament | Arkitekturkrav; ikke ekte integrasjon i demoen | Senere |
| P-10 | Tilgang til informasjon og handlinger skal styres etter rolle og minste privilegium | Alle | Krav før produksjonsbruk | Senere |
| P-11 | Brukeren skal kunne sammenligne scenarioer og tiltak | 4, 6 | Enkel scenario-sammenligning | Kan |
| P-12 | Besøkende skal kunne forstå og fullføre hoveddemoen uten presentatør eller konto | 2.1 | Selvforklarende start og guidet scenarioflyt | Må |
| P-13 | Demoen skal tydelig vise at konseptet er selvstendig, uten å nevne navngitte selskaper, og bruke bare syntetiske data | 2.1 | Synlig konsept-/syntetisk-data-merking | Må |
| P-14 | Lenken skal fungere ved direkte åpning, oppfrisking og mobilvisning | 2.1 | Responsiv demonstrator | Må |
| P-15 | Besøksdata skal ikke samles inn uten nødvendig formål og synlig informasjon | 2.1 | Ingen analyse- eller sporingsverktøy | Må |
| P-16 | Grensesnitt og innhold skal tilbys på norsk og engelsk | 2.1 | Språkvelger, med all tekst i språkfiler og oversatte tekstfelt i datasettet | Bør |

### 8.1 Demonstratorkrav

| ID | Demonstratorkrav | Knytning |
|---|---|---|
| D-01 | Bruke kun syntetiske bank-, system-, leverandør- og hendelsesdata | P-01, P-04 |
| D-02 | Vise minst 6 tjenester, 10 systemer og 4 leverandører | P-01, P-02 |
| D-03 | La brukeren følge relasjoner fra tjeneste til underliggende systemer og leverandører | P-02 |
| D-04 | Tilby scenario for leverandørsvikt og mislykket systemendring | P-03 |
| D-05 | Forklare påvirkning med relasjonssti, antakelser og datamangler | P-03, P-04 |
| D-06 | Vise hendelsesstatus, tidslinje og oppgaver samlet | P-05, P-06, P-07 |
| D-07 | Lage utskrivbar oppsummering av scenarioet | P-08 |
| D-08 | Merke alle data og beregninger som demonstrasjonsinnhold | P-04 |
| D-09 | Starte uten konto og tilby en synlig eksempelbank og scenarioflyt | P-12 |
| D-10 | Ha en kort selvforklarende introduksjon og kunne nullstille demonstrasjonen | P-12 |
| D-11 | Merke løsningen som selvstendig konsept og data som syntetiske | P-13 |
| D-12 | Unngå unødvendig innsamling av besøksdata | P-15 |
| D-13 | Vise grensesnittet på norsk og engelsk via språkvelger, med tekst samlet i språkfiler og datasettets tekstfelt strukturert per språk (`{ no: "…", en: "…" }`) | P-16 |

## 9. Funksjonelle krav

| ID | Krav | Prioritet |
|---|---|---|
| F-01 | Vise fiktive kritiske banktjenester, interne systemer og eksterne leverandører | Må |
| F-02 | Vise relasjoner som et navigerbart avhengighetskart | Må |
| F-03 | Tilby minst to scenarioer: leverandør-/skysvikt og mislykket systemendring | Må |
| F-04 | Beregne og forklare direkte og indirekte påvirkning ut fra registrerte relasjoner | Må |
| F-05 | Skille tydelig mellom bekreftede demo-inputs, antakelser og manglende informasjon | Må |
| F-06 | Vise hendelsesstatus, tidslinje, ansvarlig rolle og oppgaver | Må |
| F-07 | Tillate justering av scenarioets omfang og varighet | Bør |
| F-08 | Eksportere en kort rapport med scenario, påvirkning, antakelser og tiltak | Bør |
| F-09 | Filtrere kartet etter tjeneste, leverandør, kritikalitet og status | Bør |
| F-10 | Vise sammenligning mellom to scenarioer | Kan |

## 10. Ikke-funksjonelle krav

- **Sikkerhet:** Ingen hemmeligheter eller sensitive opplysninger i klientkode eller demo-data.
- **Personvern:** Ingen innlogging; ingen brukerdata samles inn. Valg lagres bare i nettleserfanen (sessionStorage).
- **Tilgjengelighet:** Tastaturnavigasjon, synlige fokusmarkører (også på knapper med skygge), kontrast minst 4.5:1 for tekst og tekstalternativer til fargekoding.
- **Responsivitet:** Brukbar fra 360 px mobil til stor skjerm uten at siden ruller sideveis; kartet har en alternativ liste-/detaljvisning på små skjermer, og brede tabeller ruller inne i kortet.
- **Inndata:** Alle fritekstfelt har grenser og tegnfilter. Søk i kartet: maks 60 tegn, bokstaver, tall, mellomrom og enkle skilletegn. Beslutning: 3–500 tegn, bokstaver (alle språk), tall, linjeskift og vanlig tegnsetting; kontrolltegn, emoji og markup fjernes også ved innliming. Tekst vises alltid som ren tekst. Lagret tilstand valideres felt for felt ved innlasting, slik at gammel eller ødelagt lagring aldri krasjer appen.
- **Bufring:** Produksjonsbygget gir filnavn med innholdshash, slik at nye versjoner alltid lastes etter publisering. Biblioteker ligger i egne filer som kan gjenbrukes fra nettleserens cache når bare appkoden endres.
- **Sporbarhet:** Påvirkningsberegningen skal kunne forklares gjennom synlige relasjoner og regler.
- **Forståelighet:** Scenario og alle verdier er merket som syntetiske, også på utskrift av rapporten. Samme begreper brukes på alle sider (Bortfall, Redusert, Mulig bortfall, Over gjenopprettingsmål).
- **Språk:** Ingen brukerrettet tekst skrives direkte i komponentkoden; datoer og tall formateres etter valgt språk.
- **Robusthet:** Tomme, manglende eller motstridende relasjoner vises som datamangler og skjules ikke. Ukjente lenker og objekter gir en forståelig side, ikke en feil.
- **Navngitte selskaper:** Ingen virkelige selskaper nevnes i grensesnitt, data, dokumentasjon eller sidemetadata.

## 11. Data og demonstrasjonsmodell

Objekter:

- **Tjeneste:** navn, kritikalitet, tjenesteeier, kanaler, gjenopprettingsmål
- **System:** navn, miljø, driftsstatus, teknisk eier
- **Leverandør:** navn, tjenestetype, land/regioner, kritikalitet, alternativer
- **Avhengighet:** fra-objekt, til-objekt, type, kritikalitet, datakilde/gyldighetsstatus, regioner
- **Scenario:** feiltype, starttid, omfang, varighet, berørte komponenter
- **Hendelse:** status, tidslinje, beslutninger, oppgaver og ansvarlig rolle

Datasettet for Morild Bank har 4 kanaler, 8 tjenester, 13 systemer, 6 leverandører, 45 relasjoner og 2 scenarioer. Kjernebanksystemet leveres og driftes av en kjernebankleverandør, slik det er vanlig i norske banker, og innlogging går via en felles eID-løsning, som er et tydelig enkeltpunkt for svikt. Oppgaven om rapportering bruker DORA-begrepet «alvorlig IKT-relatert hendelse».

Alle poster merkes `synthetic: true`. Brukerrettede tekstfelt (navn, beskrivelser, scenario- og oppgavetekster) lagres per språk (`no` og `en`). Demonstrasjonsrapporten gjentar at dataene er oppdiktede.

## 12. Skjermer

1. **Tjenesteoversikt:** tjenestestatus og indikatorer for datakvalitet.
2. **Scenario:** valg av feiltype, komponent, alvorlighet og varighet.
3. **Påvirkning:** sammendrag, avhengighetskart med filter og søk (eller liste), detaljer og usikkerheter i datagrunnlaget.
4. **Hendelsesrom:** status, oppgaver, beslutningslogg, konsekvenser, kontrollspørsmål og tidslinje.
5. **Rapport:** kort, utskrivbar oppsummering av simuleringen.

## 13. Teknisk løsning

Statisk webapp med et lite JSON-datasett og beregning av påvirkning i nettleseren.

- **Rammeverk:** React, Vite og TypeScript.
- **Graf:** React Flow (`@xyflow/react`) med et eget båndoppsett: én kolonne per objekttype (leverandører → systemer → tjenester → kanaler). Rekkefølgen velges for å gi færrest kryssende piler, oppsettet strekkes til kartrammens høyde, og hver boks flyttes dit færrest mulig streker går gjennom bokser. Nodene er vanlige DOM-elementer, noe som gir tastaturfokus, skjermleserstøtte, språkfiler og egen styling.
- **Ruting:** Hash-baserte URL-er, slik at direkte lenker og oppfrisking fungerer på statisk hosting.
- **Språk:** i18n-oppsett med norsk og engelsk språkfil.
- **Hosting:** Statisk hosting på Cloudflare Pages.
- **Tester:** Enhetstester for påvirkningsberegningen.

Et produksjonsprodukt kan utvides med API, database, tilgangsstyring, import av kundens tjeneste- og leverandørregistre, revisjonsspor og integrasjoner.

## 14. Akseptansekriterier

1. Brukeren kan gå fra scenario til berørte tjenester uten hjelp.
2. Hver markert påvirkning kan spores gjennom synlige avhengigheter.
3. Manglende data og antakelser er synlige og påvirker ikke resultatet stilltiende.
4. Brukeren kan følge hendelsens tidslinje og se ansvar og oppgaver.
5. Rapporten viser scenario, påvirkede tjenester, antakelser og syntetisk datamerking.
6. Hovedflyten fungerer på mobil og med tastatur.
