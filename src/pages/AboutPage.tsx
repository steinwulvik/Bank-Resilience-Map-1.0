import { useI18n } from '../i18n';
import { PageHeader } from '../components/ui';

export default function AboutPage() {
  const { m } = useI18n();
  return (
    <div className="page page-narrow">
      <PageHeader title={m.about.title} />
      <section className="card card-notice">
        <p>{m.concept.disclaimer}</p>
        <p>{m.concept.noAdvice}</p>
      </section>
      <section className="prose">
        <h2>{m.about.whatTitle}</h2>
        <p>{m.about.what}</p>
        <h2>{m.about.whyTitle}</h2>
        <p>{m.about.why}</p>
        <h2>{m.scenario.rulesTitle}</h2>
        <ol>
          {m.scenario.rules.map((r) => <li key={r}>{r}</li>)}
        </ol>
        <h2>{m.about.limitsTitle}</h2>
        <ul>
          {m.about.limits.map((l) => <li key={l}>{l}</li>)}
        </ul>
        <h2>{m.about.privacyTitle}</h2>
        <p>{m.about.privacy}</p>
        <h2>{m.about.techTitle}</h2>
        <p>{m.about.tech}</p>
        <h2>{m.about.sourcesTitle}</h2>
        <ul>
          <li>
            <a href="https://www.finanstilsynet.no/publikasjoner-og-analyser/risiko--og-sarbarhetsanalyse/risiko--og-sarbarhetsanalyse-2026/risiko--og-sarbarhetsanalyse-2026/risiko--og-sarbarhetsanalyse-2026" rel="noopener noreferrer" target="_blank">
              {m.about.source4}
            </a>
          </li>
          <li>
            <a href="https://eur-lex.europa.eu/eli/reg/2022/2554/oj" rel="noopener noreferrer" target="_blank">
              {m.about.source3}
            </a>
          </li>
          <li>
            <a href="https://www.bankingsupervision.europa.eu/framework/priorities/html/ssm.supervisory_priorities202511.en.html" rel="noopener noreferrer" target="_blank">
              {m.about.source1}
            </a>
          </li>
          <li>
            <a href="https://www.bankingsupervision.europa.eu/framework/priorities/html/ssm.supervisory_priorities202412~6f69ad032f.en.html" rel="noopener noreferrer" target="_blank">
              {m.about.source2}
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
