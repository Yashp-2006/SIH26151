import { useEffect, useState } from 'react'
import { AppDataProvider, useApp } from './data/store'
import type { Assessment } from './data/model'
import { Landing } from './screens/Landing'
import { Login } from './screens/Login'
import { Shell, type View } from './components/Shell'
import { CasePicker } from './components/CasePicker'
import { Overview } from './screens/Overview'
import { Case } from './screens/Case'
import { Workspace } from './screens/Workspace'
import { Evaluation } from './screens/Evaluation'
import { Review } from './screens/Review'

const DEFAULT_PAIR = 'acc_024__acc_025'

const TITLE: Record<View, string> = {
  overview: 'Overview',
  case: 'Evidence Balance Sheet',
  workspace: 'Investigation Workspace',
  evaluation: 'Evaluation',
  review: 'Assessment & Review',
}

function Portal({ onHome }: { onHome: () => void }) {
  const { assess, assessCached, snapshot } = useApp()
  const [view, setView] = useState<View>('overview')
  const [pairId, setPairId] = useState(DEFAULT_PAIR)
  const [live, setLive] = useState<Record<string, Assessment>>({})

  // cached result renders instantly; the async call upgrades it (backend, if up)
  const assessment = live[pairId] ?? assessCached(pairId)

  useEffect(() => {
    let ok = true
    assess(pairId).then((a) => {
      if (ok && a) setLive((m) => (m[pairId] === a ? m : { ...m, [pairId]: a }))
    })
    return () => {
      ok = false
    }
  }, [pairId, assess])

  const needsCase = view === 'case' || view === 'workspace' || view === 'review'

  return (
    <Shell
      view={view}
      onView={setView}
      onHome={onHome}
      title={TITLE[view]}
      topRight={needsCase ? <CasePicker pairId={pairId} onPick={setPairId} /> : undefined}
      onDownload={
        needsCase && assessment
          ? async () => {
              const { downloadReport } = await import('./lib/report')
              downloadReport(assessment, snapshot.accounts, snapshot.health)
            }
          : undefined
      }
    >
      {view === 'overview' && (
        <Overview
          onOpenCase={(pid, v) => {
            setPairId(pid)
            setView(v)
          }}
        />
      )}
      {view === 'evaluation' && <Evaluation />}
      {needsCase && !assessment && (
        <div className="flex flex-col gap-3">
          <div className="h-24 animate-pulse rounded-[var(--r-lg)] bg-[var(--color-hairline)]" />
          <div className="h-40 animate-pulse rounded-[var(--r-lg)] bg-[var(--color-hairline)]" />
        </div>
      )}
      {view === 'case' && assessment && <Case a={assessment} />}
      {view === 'workspace' && assessment && <Workspace a={assessment} />}
      {view === 'review' && assessment && <Review a={assessment} />}
    </Shell>
  )
}

export default function App() {
  const [stage, setStage] = useState<'landing' | 'login' | 'portal'>('landing')

  if (stage === 'landing') return <Landing onEnter={() => setStage('login')} />
  if (stage === 'login') return <Login onIn={() => setStage('portal')} />
  return (
    <AppDataProvider>
      <Portal onHome={() => setStage('landing')} />
    </AppDataProvider>
  )
}
