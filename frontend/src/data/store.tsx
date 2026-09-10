import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import type { Assessment, Snapshot } from './model'

const BACKEND = 'http://localhost:8000'

interface AppData {
  ready: boolean
  /** 'service' = live gateway on :8000, 'local' = engine results bundled with the console */
  source: 'service' | 'local'
  snapshot: Snapshot
  assess: (pairId: string) => Promise<Assessment>
  assessCached: (pairId: string) => Assessment | undefined
}

const Ctx = createContext<AppData | null>(null)

function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    p,
    new Promise<T>((_, rej) => setTimeout(() => rej(new Error('timeout')), ms)),
  ])
}

// resolved exactly once for the lifetime of the page — no re-probing on remount
let bootstrap: Promise<AppData> | null = null

function boot(): Promise<AppData> {
  if (bootstrap) return bootstrap
  bootstrap = (async () => {
    const snapshot: Snapshot = await fetch(`${import.meta.env.BASE_URL}snapshot.json`).then((r) => {
      if (!r.ok) throw new Error(`snapshot ${r.status}`)
      return r.json()
    })

    let source: 'service' | 'local' = 'local'
    try {
      const h = await withTimeout(fetch(`${BACKEND}/health`), 900)
      if (h.ok) source = 'service'
    } catch {
      source = 'local'
    }

    const liveCache: Record<string, Assessment> = {}
    const assess = async (pairId: string): Promise<Assessment> => {
      if (liveCache[pairId]) return liveCache[pairId]
      if (source === 'service') {
        try {
          const [a, b] = pairId.split('__')
          const res = await withTimeout(fetch(`${BACKEND}/balance_sheet/${a}/${b}`), 1500)
          if (res.ok) {
            const j = (await res.json()) as Assessment
            liveCache[pairId] = j
            return j
          }
        } catch {
          /* fall through to bundled */
        }
      }
      return snapshot.assessments[pairId]
    }

    return {
      ready: true,
      source,
      snapshot,
      assess,
      assessCached: (pid) => snapshot.assessments[pid],
    }
  })()
  return bootstrap
}

export function AppDataProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<AppData | null>(null)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    let ok = true
    boot().then(
      (d) => ok && setData(d),
      () => {
        bootstrap = null // allow a retry on reload
        if (ok) setFailed(true)
      },
    )
    return () => {
      ok = false
    }
  }, [])

  if (failed) {
    return (
      <div className="grid min-h-[100dvh] place-items-center bg-[var(--color-paper)] px-6">
        <div className="max-w-[360px] text-center">
          <div className="text-[13px] font-semibold text-[var(--color-ink)]">
            Engine data unavailable
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-[var(--color-ink-soft)]">
            The assessment set could not be loaded. Reload the page, or start the gateway with{' '}
            <span className="num">uvicorn backend.app.main:app</span>.
          </p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="grid min-h-[100dvh] place-items-center bg-[var(--color-paper)]">
        <div className="flex flex-col items-center gap-3">
          <div className="h-6 w-40 animate-pulse rounded-[var(--r)] bg-[var(--color-hairline)]" />
          <div className="h-3 w-24 animate-pulse rounded-[var(--r)] bg-[var(--color-hairline)]" />
        </div>
      </div>
    )
  }

  return <Ctx.Provider value={data}>{children}</Ctx.Provider>
}

export function useApp(): AppData {
  const v = useContext(Ctx)
  if (!v) throw new Error('useApp outside AppDataProvider')
  return v
}
