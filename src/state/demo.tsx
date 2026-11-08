import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { dataset, nodesById, scenariosById } from '../data';
import type { LocalizedText, ScenarioParams } from '../data/types';
import { computeImpact, type ImpactResult } from '../engine/impact';

/**
 * Demo-tilstand. Lagres bare i sessionStorage i denne fanen, slik at oppfrisking
 * beholder valgene, men ingenting sendes noe sted (SPEC P-15).
 */
export type IncidentStatus = 'investigating' | 'mitigating' | 'monitoring' | 'closed';
export type TaskStatus = 'todo' | 'doing' | 'done';

export interface CustomTask {
  id: string;
  title: LocalizedText;
  role: LocalizedText;
  fromGap: string;
}

export interface LogEntry {
  id: string;
  /** Faktisk tidspunkt brukeren gjorde endringen (ISO). */
  at: string;
  kind: 'decision' | 'status';
  text: string;
  role?: string;
  /** Oppgaven en beslutning gjelder; mangler den, gjelder den hele hendelsen. */
  taskId?: string;
}

export interface DemoState {
  scenarioId: string | null;
  params: ScenarioParams | null;
  /** Når scenarioet ble startet (ISO). Tidslinje og frister regnes fra dette. */
  startedAt: string | null;
  incidentStatus: IncidentStatus;
  taskStatus: Record<string, TaskStatus>;
  customTasks: CustomTask[];
  log: LogEntry[];
  guide: boolean;
}

const initial: DemoState = {
  scenarioId: null,
  params: null,
  startedAt: null,
  incidentStatus: 'investigating',
  taskStatus: {},
  customTasks: [],
  log: [],
  guide: false,
};

const KEY = 'brm-demo-v3';

const STATUSES: IncidentStatus[] = ['investigating', 'mitigating', 'monitoring', 'closed'];
const TASK_STATUSES: TaskStatus[] = ['todo', 'doing', 'done'];
const isObj = (x: unknown): x is Record<string, unknown> => typeof x === 'object' && x !== null && !Array.isArray(x);
const str = (x: unknown, max = 500): string | undefined => (typeof x === 'string' ? x.slice(0, max) : undefined);

/**
 * Leser lagret tilstand og godtar bare felter med riktig form. Gammel, ødelagt eller manipulert
 * lagring gir aldri krasj: ugyldige felter faller tilbake til startverdiene.
 */
export function sanitize(raw: unknown): DemoState {
  if (!isObj(raw)) return initial;
  const scenarioId = typeof raw.scenarioId === 'string' && scenariosById[raw.scenarioId] ? raw.scenarioId : null;
  if (!scenarioId) return { ...initial, guide: raw.guide === true };
  const p = raw.params;
  const params =
    isObj(p) && typeof p.targetId === 'string' && nodesById[p.targetId] && Array.isArray(p.regions) &&
    (p.severity === 'outage' || p.severity === 'degraded') && typeof p.durationMinutes === 'number' && p.durationMinutes > 0
      ? ({ ...p, regions: p.regions.filter((r) => typeof r === 'string') } as ScenarioParams)
      : null;
  const startedAt = typeof raw.startedAt === 'string' && !Number.isNaN(Date.parse(raw.startedAt)) ? raw.startedAt : null;
  const taskStatus: Record<string, TaskStatus> = {};
  if (isObj(raw.taskStatus))
    for (const [k, v] of Object.entries(raw.taskStatus)) if (TASK_STATUSES.includes(v as TaskStatus)) taskStatus[k] = v as TaskStatus;
  const customTasks = Array.isArray(raw.customTasks)
    ? raw.customTasks.filter((t): t is CustomTask => isObj(t) && typeof t.id === 'string' && isObj(t.title) && isObj(t.role))
    : [];
  const log = Array.isArray(raw.log)
    ? raw.log.flatMap((e): LogEntry[] => {
        if (!isObj(e) || (e.kind !== 'decision' && e.kind !== 'status')) return [];
        const text = str(e.text);
        const at = str(e.at, 40);
        if (!text || !at || Number.isNaN(Date.parse(at))) return [];
        return [{ id: str(e.id, 40) ?? Math.random().toString(36).slice(2, 10), at, kind: e.kind, text, role: str(e.role, 80), taskId: str(e.taskId, 80) }];
      })
    : [];
  return {
    scenarioId,
    params,
    startedAt,
    incidentStatus: STATUSES.includes(raw.incidentStatus as IncidentStatus) ? (raw.incidentStatus as IncidentStatus) : 'investigating',
    taskStatus,
    customTasks,
    log,
    guide: raw.guide === true,
  };
}

function load(): DemoState {
  try {
    const s = sessionStorage.getItem(KEY);
    return s ? sanitize(JSON.parse(s)) : initial;
  } catch {
    return initial;
  }
}

interface DemoApi {
  state: DemoState;
  result: ImpactResult | null;
  /** Starter eller oppdaterer scenario. Ny scenariotype nullstiller hendelsesrommet. */
  runScenario: (scenarioId: string, params: ScenarioParams) => void;
  setIncidentStatus: (s: IncidentStatus, logText: string) => void;
  setTaskStatus: (id: string, s: TaskStatus) => void;
  addCustomTask: (t: CustomTask) => void;
  addDecision: (text: string, role: string, taskId?: string) => void;
  setGuide: (on: boolean) => void;
  reset: () => void;
}

const DemoContext = createContext<DemoApi | null>(null);

const uid = () => Math.random().toString(36).slice(2, 10);

export function DemoProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<DemoState>(load);

  useEffect(() => {
    try {
      sessionStorage.setItem(KEY, JSON.stringify(state));
    } catch {
      /* lagring er en bekvemmelighet; demoen virker uten */
    }
  }, [state]);

  const result = useMemo(() => {
    if (!state.params) return null;
    try {
      return computeImpact(dataset, state.params);
    } catch {
      return null;
    }
  }, [state.params]);

  const runScenario = useCallback((scenarioId: string, params: ScenarioParams) => {
    setState((s) =>
      s.scenarioId === scenarioId
        ? { ...s, params }
        : { ...initial, guide: s.guide, scenarioId, params, startedAt: scenarioStartFromNow(scenarioId).toISOString() },
    );
  }, []);

  const api: DemoApi = {
    state,
    result,
    runScenario,
    setIncidentStatus: (incidentStatus, text) =>
      setState((s) => ({
        ...s,
        incidentStatus,
        log: [...s.log, { id: uid(), at: new Date().toISOString(), kind: 'status', text }],
      })),
    setTaskStatus: (id, st) => setState((s) => ({ ...s, taskStatus: { ...s.taskStatus, [id]: st } })),
    addCustomTask: (t) =>
      setState((s) => (s.customTasks.some((c) => c.id === t.id) ? s : { ...s, customTasks: [...s.customTasks, t] })),
    addDecision: (text, role, taskId) =>
      setState((s) => ({
        ...s,
        log: [...s.log, { id: uid(), at: new Date().toISOString(), kind: 'decision', text, role, taskId }],
      })),
    setGuide: (guide) => setState((s) => ({ ...s, guide })),
    reset: () => setState(initial),
  };

  return <DemoContext.Provider value={api}>{children}</DemoContext.Provider>;
}

/**
 * Scenarioets ferdige hendelser og beslutninger skal ligge i fortiden når brukeren åpner det,
 * slik at det brukeren selv legger inn alltid er nyest. Starttiden settes derfor så langt tilbake
 * som den siste forhåndsutfylte hendelsen, pluss noen minutter.
 */
export function historyMinutes(scenarioId: string): number {
  const sc = scenariosById[scenarioId];
  if (!sc) return 0;
  const offsets = [...sc.timeline, ...sc.decisions].map((e) => e.offsetMinutes);
  return Math.max(0, ...offsets) + 5;
}
export const scenarioStartFromNow = (scenarioId: string): Date =>
  new Date(Date.now() - historyMinutes(scenarioId) * 60000);

/** Starttidspunkt for aktivt scenario (nå, hvis det mangler). */
export const scenarioStart = (s: DemoState): Date => (s.startedAt ? new Date(s.startedAt) : new Date());

export function useDemo(): DemoApi {
  const ctx = useContext(DemoContext);
  if (!ctx) throw new Error('useDemo må brukes inne i DemoProvider');
  return ctx;
}
