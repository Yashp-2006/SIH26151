import { useState } from 'react'
import { Button } from '../lib/ui'
import { Lock } from '../lib/icons'

export function Login({ onIn }: { onIn: () => void }) {
  const [email, setEmail] = useState('')

  return (
    <div className="grid min-h-[100dvh] lg:grid-cols-[0.9fr_1.1fr]">
      {/* brand panel */}
      <div className="hidden flex-col justify-between bg-[var(--color-ink)] p-10 lg:flex">
        <div className="text-[13px] font-semibold tracking-[0.16em] text-[var(--color-surface)]">
          PRAMANA
        </div>
        <div>
          <p className="max-w-[24ch] text-[26px] font-semibold leading-[1.2] tracking-[-0.02em] text-[var(--color-surface)]">
            The graph is a view. The ledger is the truth.
          </p>
          <p className="mt-3 max-w-[38ch] text-[12.5px] leading-relaxed text-[#a8a8a2]">
            Evidence-accounting for dark-web attribution. Every link carries its own arithmetic,
            its counter-evidence, and the analyst who signed it.
          </p>
        </div>
        <div className="num text-[10.5px] text-[#7a7a74]">Problem Statement 26151 · NTRO</div>
      </div>

      {/* form */}
      <div className="flex items-center justify-center bg-[var(--color-paper)] px-6">
        <div className="w-full max-w-[340px]">
          <h1 className="text-[19px] font-semibold text-[var(--color-ink)]">Analyst sign-in</h1>
          <p className="mt-1 text-[12px] text-[var(--color-ink-soft)]">
            Authorised investigators only.
          </p>

          <form
            className="mt-6 flex flex-col gap-3.5"
            onSubmit={(e) => {
              e.preventDefault()
              onIn()
            }}
          >
            <label className="flex flex-col gap-1.5">
              <span className="text-[11px] font-medium uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                Agency email
              </span>
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="analyst@ntro.gov.in"
                className="rounded-[var(--r)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] px-3 py-2 text-[13px] outline-none transition-colors focus:border-[var(--color-accent)]"
              />
            </label>
            <label className="flex flex-col gap-1.5">
              <span className="text-[11px] font-medium uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                Passphrase
              </span>
              <input
                type="password"
                placeholder="••••••••"
                className="rounded-[var(--r)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] px-3 py-2 text-[13px] outline-none transition-colors focus:border-[var(--color-accent)]"
              />
            </label>
            <Button type="submit">
              <span className="flex items-center justify-center gap-1.5">
                <Lock /> Sign in
              </span>
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
