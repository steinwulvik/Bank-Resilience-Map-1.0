import { useEffect, useRef, useState } from 'react';
import logo from './assets/morild-bank-logo.png';
import { LANGS, useI18n } from './i18n';
import { href, navigate, useRoute, type RouteName } from './router';
import { useDemo } from './state/demo';
import IntroPage from './pages/IntroPage';
import OverviewPage from './pages/OverviewPage';
import MapPage from './pages/MapPage';
import ScenarioPage from './pages/ScenarioPage';
import AnalysisPage from './pages/AnalysisPage';
import IncidentPage from './pages/IncidentPage';
import ReportPage from './pages/ReportPage';
import AboutPage from './pages/AboutPage';

// Hovedflyten navigeres med trinnene 1–4 (FlowSteps). Oppslagssidene ligger øverst til høyre.
const LOOKUP: RouteName[] = ['overview', 'about'];
// Sider utenfor trinnene får en lenke tilbake til flyten.
const OFF_FLOW: RouteName[] = ['overview', 'about'];

export default function App() {
  const route = useRoute();
  const { m, lang, setLang } = useI18n();
  const { reset, state } = useDemo();
  const [announce, setAnnounce] = useState('');
  const first = useRef(true);

  // Flytt fokus til sidetittelen ved navigasjon, slik at tastatur- og skjermleserbrukere følger med.
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    window.scrollTo(0, 0);
    document.getElementById('page-title')?.focus();
  }, [route.name]);

  useEffect(() => {
    const page = route.name === 'intro' ? '' : `${m.nav[route.name]} · `;
    document.title = `${page}${m.meta.pageTitle}`;
  }, [route.name, m]);

  const onReset = () => {
    reset();
    setAnnounce(m.nav.resetConfirm);
    navigate('intro');
    window.setTimeout(() => setAnnounce(''), 4000);
  };

  const page = {
    intro: <IntroPage />,
    overview: <OverviewPage />,
    map: <MapPage query={route.query} />,
    scenario: <ScenarioPage />,
    analysis: <AnalysisPage query={route.query} />,
    incident: <IncidentPage />,
    report: <ReportPage />,
    about: <AboutPage />,
  }[route.name];

  return (
    <div className={`app route-${route.name}`}>
      <a className="skip-link" href="#main" onClick={(e) => { e.preventDefault(); document.getElementById('main')?.focus(); }}>
        {m.nav.skipToContent}
      </a>
      <section className="concept-banner" aria-label={m.concept.bannerLabel}>
        {m.concept.banner}
      </section>
      <header className="topbar">
        <div className="topbar-inner">
          <a className="brand" href={href('intro')}>
            <img src={logo} alt="Morild Bank" width={180} height={25} />
          </a>
          {route.name !== 'intro' && (
            <nav className="topnav" aria-label={m.nav.label}>
              <ul>
                {LOOKUP.map((r) => (
                  <li key={r}>
                    <a href={href(r)} aria-current={route.name === r ? 'page' : undefined}>
                      {m.nav[r]}
                    </a>
                  </li>
                ))}
                <li>
                  <button type="button" className="topnav-button" onClick={onReset}>
                    {m.nav.reset}
                  </button>
                </li>
              </ul>
            </nav>
          )}
          <div className="lang-switch" role="group" aria-label={m.lang.label}>
            {LANGS.map((l) => (
              <button
                key={l}
                type="button"
                lang={l === 'no' ? 'nb' : 'en'}
                aria-pressed={lang === l}
                title={m.lang[l]}
                onClick={() => setLang(l)}
              >
                <span aria-hidden="true">{m.lang.short[l]}</span>
                <span className="sr-only">{m.lang[l]}</span>
              </button>
            ))}
          </div>
        </div>
      </header>
      <main id="main" tabIndex={-1}>
        {OFF_FLOW.includes(route.name) && (
          <p className="back-link">
            <a href={href(state.params ? 'analysis' : 'scenario')}>
              ← {state.params ? m.nav.backToAnalysis : m.nav.backToScenario}
            </a>
          </p>
        )}
        {page}
      </main>
      {/* Bunnteksten (forfatter og kontakt) vises bare på «Om demoen». Banneret øverst merker konseptet på alle sider. */}
      {route.name === 'about' && (
        <footer className="footer">
          <p>
            {m.concept.author}
          </p>
          <p>
            {m.concept.contactLabel}: <a href={`mailto:${m.concept.contactEmail}`}>{m.concept.contactEmail}</a> ·{' '}
            <a href={`tel:${m.concept.contactPhone.replace(/\s/g, '')}`}>{m.concept.contactPhone}</a> ·{' '}
            <a href={m.concept.contactLinkedIn} rel="noopener noreferrer" target="_blank">{m.concept.linkedInLabel}</a>
          </p>
        </footer>
      )}
      <div className="sr-only" role="status" aria-live="polite">
        {announce}
      </div>
    </div>
  );
}
