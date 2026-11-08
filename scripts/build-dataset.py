"""Genererer src/data/morild-bank.json. Kjøres ved endringer i datasettet.
All data er oppdiktet (syntetisk)."""
import json, pathlib

# Engelske oversettelser ligger i translations-en.json (norsk tekst -> engelsk tekst).
EN = json.loads((pathlib.Path(__file__).resolve().parent/"translations-en.json").read_text(encoding="utf-8"))
MISSING = []
def T(s):
    if s not in EN: MISSING.append(s)
    return {"no": s, "en": EN.get(s, s)}

nodes = []
def node(id, kind, name, desc, crit, owner, status="operational", gaps=None, **extra):
    n = {"id": id, "kind": kind, "name": T(name), "description": T(desc), "criticality": crit,
         "owner": T(owner), "status": status}
    if gaps: n["dataGaps"] = [T(g) for g in gaps]
    n.update(extra); n["synthetic"] = True
    nodes.append(n)

# Kanaler
node("ch-mobile","channel","Mobilbank","Bankens app for privatkunder.","critical","Leder digitale kanaler")
node("ch-web","channel","Nettbank","Nettleserbasert bank for privat- og småbedriftskunder.","critical","Leder digitale kanaler")
node("ch-contact","channel","Kundesenter","Telefon og chat med rådgivere.","high","Leder kundesenter")
node("ch-pos","channel","Kort i butikk og på nett","Kortbetaling hos brukersteder.","critical","Tjenesteeier kort")

# Tjenester
def svc(id,name,desc,crit,owner,rto,rpo,**kw): node(id,"service",name,desc,crit,owner,rtoMinutes=rto,rpoMinutes=rpo,**kw)
svc("svc-accounts","Kontooversikt og saldo","Viser kontoer, saldo og bevegelser.","critical","Tjenesteeier dagligbank",240,15)
svc("svc-payments","Innenlands betaling","Regningsbetaling og overføringer mellom kontoer.","critical","Tjenesteeier betaling",120,0)
svc("svc-cards","Kortbetaling","Autorisasjon av kortkjøp i butikk og på nett.","critical","Tjenesteeier kort",60,0)
svc("svc-login","Innlogging og identifisering","Sikker innlogging for kunder i digitale kanaler.","critical","Leder identitet og tilgang",60,0)
svc("svc-loans","Lånesøknad","Søknad og kredittvurdering for forbrukslån og boliglån.","high","Tjenesteeier kreditt",1440,60)
svc("svc-support","Kundehenvendelser","Saksbehandling av henvendelser fra kunder.","medium","Leder kundesenter",480,60)
svc("svc-notify","Varsler og meldinger","SMS- og push-varsler om betalinger, innlogging og mistenkelig aktivitet.","medium","Tjenesteeier kundekommunikasjon",720,60,status="degraded",
    gaps=["Varslingstjenesten har meldt forsinkede SMS-er siste døgn; årsak er ikke registrert."])
svc("svc-aml","Transaksjonsovervåking (AML)","Overvåking av transaksjoner for hvitvasking og svindel.","high","Leder hvitvaskingskontroll",1440,240)

# Systemer
def sys_(id,name,desc,crit,owner,env,**kw): node(id,"system",name,desc,crit,owner,environment=env,**kw)
sys_("sys-core","Kjernebanksystem","Konti, saldo og posteringer. Leveres og driftes av kjernebankleverandøren.","critical","Forvaltning kjernebank","managed")
sys_("sys-pay","Betalingsmotor","Behandler og sender betalinger til avregning.","critical","Betalingsteamet","onPrem")
sys_("sys-card","Kortplattform","Kobler bankens kort mot kortprosessøren.","critical","Kortteamet","saas")
sys_("sys-api","Integrasjonsplattform (API)","Felles API-lag mellom kanaler og bakenforliggende systemer.","critical","Integrasjonsteamet","cloud",
     gaps=["Flytting til Sverige ved bortfall er planlagt, men ikke etablert."])
sys_("sys-iam","Identitetsplattform","Innlogging, sesjoner og tilgangskontroll for kunder.","critical","IAM-teamet","cloud")
sys_("sys-mob","Mobilbank-backend","Serverlogikk for mobilappen.","critical","Mobilteamet","cloud")
sys_("sys-web","Nettbankplattform","Webapplikasjon for nettbanken.","critical","Nettbankteamet","cloud")
sys_("sys-loan","Lånemotor","Søknadsbehandling og saksflyt for lån.","high","Kredittteamet","cloud")
sys_("sys-credit","Kredittvurdering","Henter kredittopplysninger og beregner betjeningsevne.","high","Kredittteamet","cloud")
sys_("sys-crm","Kundesaksbehandling (CRM)","Saksbehandlingsverktøy for kundesenteret, levert som SaaS.","medium","CRM-forvalter","saas")
sys_("sys-notify","Varslingstjeneste","Sender SMS- og push-varsler.","medium","Kommunikasjonsteamet","cloud",status="degraded")
sys_("sys-aml","Overvåkingsmotor (AML)","Regelmotor for mistenkelige transaksjoner.","high","Analyseteamet","onPrem")
sys_("sys-dwh","Datavarehus","Samler transaksjonsdata for analyse og rapportering.","high","Analyseteamet","cloud")

# Leverandører
def prv(id,name,desc,crit,owner,stype,regions,alt,**kw): node(id,"provider",name,desc,crit,owner,serviceType=T(stype),regions=regions,alternatives=T(alt),**kw)
prv("prv-nimbus","Nimbus Sky","Skyplattform for bankens skybaserte systemer.","critical","Leverandøransvarlig sky","Skyplattform (IaaS/PaaS)",["no","se","dk","fi"],
    "Datasentre i andre nordiske land hos samme leverandør. Ingen avtale med alternativ skyleverandør.")
prv("prv-kortnord","KortNord Prosessering","Prosesserer kortautorisasjoner for flere nordiske banker.","critical","Tjenesteeier kort","Kortprosessering",["no","dk"],
    "Stand-in-autorisasjon med reservegrenser i inntil 4 timer.")
prv("prv-clearing","Avregningssentralen","Felles infrastruktur for avregning av betalinger.","critical","Tjenesteeier betaling","Betalingsinfrastruktur",["no"],
    "Ingen alternativ leverandør. Manuell beredskapsrutine for hastebetalinger.")
prv("prv-saksflyt","Saksflyt AS","Leverer saksbehandlingsverktøyet for kundesenteret.","medium","CRM-forvalter","SaaS – saksbehandling",["no"],
    "Kundesenteret kan registrere saker i regneark midlertidig.",
    gaps=["Leverandøren har ikke oppgitt hvilken skyleverandør og hvilket land tjenesten kjører i."])
prv("prv-kredittdata","Kredittdata Norden","Leverer kredittopplysninger.","high","Tjenesteeier kreditt","Kredittopplysning",["no","se","fi"],
    "Manuell kredittvurdering for prioriterte søknader.")
prv("prv-smslinje","SMS-Linje","SMS-gateway for utsending av varsler.","medium","Tjenesteeier kundekommunikasjon","SMS-gateway",["se","dk"],
    "Push-varsler i mobilbanken.")

prv("prv-kjerne","Kjernedrift Nord","Leverer og drifter kjernebanksystemet for Morild Bank og flere andre banker.","critical","Leverandøransvarlig kjernebank","Kjernebank som driftet tjeneste",["no"],
    "Ingen alternativ leverandør på kort sikt. Bytte av kjernebankleverandør er et flerårig prosjekt.")
prv("prv-eid","Bankfelles eID","Felles elektronisk identifisering som mange banker bruker til innlogging og signering.","critical","Leder identitet og tilgang","Elektronisk identifisering (eID)",["no"],
    "Ingen fullgod reserveløsning. Kundesenteret kan hjelpe kunder, men digital innlogging stopper.")
deps = []
def dep(f, t, type="uses", strength="hard", source="Tjenestekatalog", confirmed="2026-08-20", validity="confirmed", regions=None, note=None):
    d = {"id": f"{f}__{t}", "from": f, "to": t, "type": type, "strength": strength}
    if regions is not None: d["regions"] = regions
    d.update({"source": T(source), "lastConfirmed": confirmed, "validity": validity})
    if note: d["note"] = T(note)
    d["synthetic"] = True
    deps.append(d)

CMDB, TK, LR = "CMDB", "Tjenestekatalog", "Leverandørregister"
# Kanaler
dep("ch-mobile","sys-mob",source=CMDB,confirmed="2026-09-12")
dep("ch-mobile","svc-login")
dep("ch-mobile","svc-accounts",strength="soft")
dep("ch-mobile","svc-payments",strength="soft")
dep("ch-mobile","svc-notify",strength="soft")
dep("ch-web","sys-web",source=CMDB,confirmed="2026-09-12")
dep("ch-web","svc-login")
dep("ch-web","svc-accounts",strength="soft")
dep("ch-web","svc-payments",strength="soft")
dep("ch-web","svc-loans",strength="soft")
dep("ch-contact","svc-support",confirmed="2026-06-02")
dep("ch-contact","svc-accounts",strength="soft",confirmed="2026-06-02")
dep("ch-pos","svc-cards",confirmed="2026-10-01")
# Tjenester
dep("svc-accounts","sys-core",confirmed="2026-10-10")
dep("svc-accounts","sys-api",confirmed="2026-10-10")
dep("svc-payments","sys-pay",confirmed="2026-10-10")
dep("svc-payments","sys-api",confirmed="2026-10-10")
dep("svc-cards","sys-card",confirmed="2026-10-01")
dep("svc-login","sys-iam",confirmed="2026-09-30")
dep("svc-loans","sys-loan",source="Workshop med tjenesteeier",confirmed="2026-03-14")
dep("svc-loans","sys-credit",source="Workshop med tjenesteeier",confirmed="2026-03-14")
dep("svc-support","sys-crm",confirmed="2026-06-02")
dep("svc-support","sys-core",strength="soft",confirmed="2026-06-02",note="Rådgivere kan svare på generelle spørsmål uten kontoinformasjon.")
dep("svc-notify","sys-notify",confirmed="2025-05-20")
dep("svc-aml","sys-aml",confirmed="2026-07-01")
# Systemer
dep("sys-pay","sys-core",source=CMDB,confirmed="2026-09-12")
dep("sys-core","prv-kjerne",type="runsOn",source=LR,confirmed="2026-04-30",regions=["no"],note="Driftes i leverandørens to datasentre i Norge.")
dep("sys-iam","prv-eid",source=LR,confirmed="2026-04-30",regions=["no"],note="Kundene logger inn med felles eID. Bankens egen plattform håndterer sesjoner og tilganger.")
dep("sys-pay","prv-clearing",source=LR,confirmed="2026-04-30",regions=["no"])
dep("sys-card","prv-kortnord",source=LR,confirmed="2026-04-30",regions=["no","dk"],note="Aktiv-aktiv i Norge og Danmark.")
dep("sys-card","sys-core",strength="soft",source=CMDB,confirmed="2026-09-12",note="Kortautorisasjon kan kjøre med reservegrenser (stand-in) uten kjernebanken.")
dep("sys-api","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["no"],note="Kjører bare i Norge.")
dep("sys-iam","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["no","se"],note="Aktiv-aktiv i Norge og Sverige.")
dep("sys-mob","sys-api",source=CMDB,confirmed="2026-09-12")
dep("sys-mob","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["no"])
dep("sys-web","sys-api",source=CMDB,confirmed="2026-09-12")
dep("sys-web","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["no","se"])
dep("sys-loan","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["no"])
dep("sys-loan","sys-core",source=CMDB,confirmed="2026-09-12")
dep("sys-credit","prv-kredittdata",source=LR,confirmed="2026-04-30",regions=["no"])
dep("sys-credit","sys-api",type="dataFeed",source="Antatt ut fra integrasjonsoppsett",confirmed=None,validity="assumed",
    note="Ikke bekreftet i arkitekturdokumentasjonen.")
dep("sys-crm","prv-saksflyt",type="runsOn",source=LR,confirmed="2026-04-30",regions=["no"])
dep("sys-notify","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-02-11",note="Land er ikke registrert i CMDB.")
dep("sys-notify","prv-smslinje",source=LR,confirmed="2026-04-30",regions=["se"],note="Bruker bare SMS-Linjes plattform i Sverige.")
dep("sys-aml","sys-dwh",type="dataFeed",source="Arkitekturdokumentasjon",confirmed="2025-01-15")
dep("sys-dwh","prv-nimbus",type="runsOn",source=CMDB,confirmed="2026-09-12",regions=["se"])
# Fjerdepartsavhengighet
dep("prv-saksflyt","prv-nimbus",type="subcontractor",source="Leverandørens egenerklæring",confirmed=None,validity="assumed",
    note="Saksflyt oppgir å bruke «en nordisk skyleverandør». Antatt Nimbus Sky; land ukjent.")

def L(xs): return [T(x) for x in xs]
scenarios = [
 {"id":"sky-region","title":T("Svikt hos leverandør"),
  "summary":T("En leverandør melder om bortfall. Hvilke tjenester og kanaler kan rammes, og hvor er bildet usikkert?"),
  "failureType":"regionalProviderOutage",
  "defaults":{"targetId":"prv-nimbus","regions":["no","se","dk","fi"],"severity":"outage","durationMinutes":240},
  "durationOptions":[60,240,720,1440],"startTime":"2026-11-03T07:42:00",
  "assumptions":L(["Leverandørens statusside er eneste kilde til omfanget den første halvtimen.",
     "Systemer som kjører i flere land, flytter trafikken automatisk til landet som virker, men med redusert kapasitet.",
     "Kjernebanksystemet og systemene i Morilds eget datasenter kjører ikke hos skyleverandøren og er ikke direkte berørt."]),
  "controlQuestions":L(["Har leverandøren bekreftet omfang og forventet gjenopprettingstid?",
     "Finnes det reserveløsninger eller alternative leverandører for de berørte tjenestene?",
     "Må kunder informeres i kanalene som fortsatt virker?",
     "Skal hendelsen vurderes for rapportering etter bankens rutiner for IKT-hendelser? (Vurderes av ansvarlig rolle, ikke av verktøyet.)"]),
  "timeline":[{"offsetMinutes":o,"text":T(t)} for o,t in [
     (0,"Overvåkingen varsler feil i tjenester som bruker leverandøren."),
     (6,"Leverandøren bekrefter en hendelse med redusert tilgjengelighet."),
     (15,"Beredskapsleder åpner hendelsesrom og kaller inn berørte team."),
     (30,"Første konsekvensbilde deles med ledelsen."),
     (45,"Kundesenteret får standardsvar om innloggings- og betalingsproblemer.")]],
  "tasks":[{"id":f"sky-t{i}","title":T(t),"role":T(r),"dueMinutes":d} for i,(t,r,d) in enumerate([
     ("Bekreft omfang og forventet gjenoppretting med leverandøren","Leverandøransvarlig",30),
     ("Vurder om berørte systemer kan flyttes eller kjøres på en reserveløsning","Teknisk hendelsesleder",60),
     ("Publiser driftsmelding i kanalene som virker","Kommunikasjonsansvarlig",45),
     ("Informer kundesenteret om berørte tjenester","Beredskapsleder",45),
     ("Vurder om hendelsen skal rapporteres som alvorlig IKT-relatert hendelse","Operasjonell risiko",120)],1)],
  "decisions":[dict({"offsetMinutes":o,"text":T(t),"role":T(r)}, **({"taskId":k} if k else {})) for o,t,r,k in [
     (20,"Hendelsen klassifiseres foreløpig som alvorlig. Hendelsesrom etableres.","Beredskapsleder",None),
     (40,"Ingen manuell flytting før leverandøren har bekreftet omfanget.","Teknisk hendelsesleder","sky-t2")]],
  "synthetic":True},
 {"id":"failed-change","title":T("Feil etter systemendring"),
  "summary":T("En planlagt oppgradering (endring CHG-2026-114) gir feil i produksjon. Hva avhenger av komponenten som ble endret?"),
  "failureType":"failedChange",
  "defaults":{"targetId":"sys-api","regions":[],"severity":"outage","durationMinutes":120},
  "durationOptions":[30,120,240,480],"startTime":"2026-11-04T22:15:00",
  "assumptions":L(["Endringen ble satt i produksjon i et planlagt vedlikeholdsvindu.",
     "Tilbakerulling er mulig, men ikke testet for denne versjonen.",
     "Feilen gjelder bare komponenten som ble endret."]),
  "controlQuestions":L(["Kan endringen rulles tilbake, og hvor lang tid tar det?",
     "Ble avhengige tjenester identifisert i endringsvurderingen?",
     "Må transaksjoner etterbehandles når komponenten virker igjen?",
     "Hvilke forbedringer i endringsprosessen bør registreres etter hendelsen?"]),
  "timeline":[{"offsetMinutes":o,"text":T(t)} for o,t in [
     (0,"Endring CHG-2026-114 settes i produksjon."),
     (8,"Automatiske tester feiler for den endrede komponenten."),
     (14,"Vaktansvarlig eskalerer til endringsansvarlig."),
     (25,"Hendelsesrom åpnes. Tilbakerulling vurderes.")]],
  "tasks":[{"id":f"chg-t{i}","title":T(t),"role":T(r),"dueMinutes":d} for i,(t,r,d) in enumerate([
     ("Vurder tilbakerulling av endringen","Endringsansvarlig",30),
     ("Informer kundesenteret om berørte tjenester","Beredskapsleder",45),
     ("Kontroller transaksjoner som feilet under hendelsen","Betalingsteamet",120),
     ("Registrer forbedringstiltak i endringsprosessen","Operasjonell risiko",1440)],1)],
  "decisions":[{"offsetMinutes":20,"text":T("Endringsfrys for berørte systemer til årsaken er kjent."),"role":T("Endringsansvarlig"),"taskId":"chg-t1"}],
  "synthetic":True},
]

data = {"bank":{"name":"Morild Bank","description":T("Morild Bank er en oppdiktet nordisk bank laget for denne demonstrasjonen."),"synthetic":True},
        "asOf":"2026-11-01",
        "regionNames":{"no":T("Norge"),"se":T("Sverige"),"dk":T("Danmark"),"fi":T("Finland")},"staleAfterDays":365,"nodes":nodes,"dependencies":deps,"scenarios":scenarios}
out = pathlib.Path(__file__).resolve().parent.parent/"src/data/morild-bank.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
from collections import Counter
print(Counter(n["kind"] for n in nodes), len(deps), "avhengigheter")
ids={n["id"] for n in nodes}
assert all(d["from"] in ids and d["to"] in ids for d in deps)
assert not MISSING, f"Mangler engelsk oversettelse: {MISSING}"
