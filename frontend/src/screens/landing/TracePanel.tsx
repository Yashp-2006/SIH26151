const MONO = { fontFamily: 'var(--font-mono)' }
const INK = '#c9c6bc'
const DIM = '#6b6860'
const LINE = '#3a382f'
const ACCENT = '#c9532f'

// six inbound captures — SRC_02≈SRC_04 and SRC_05≈SRC_06 are mirrors of each other
const SRC = [
  { y: 66, mirror: false },
  { y: 108, mirror: true },
  { y: 150, mirror: false },
  { y: 192, mirror: true },
  { y: 234, mirror: true },
  { y: 276, mirror: true },
]
const CONV_X = 176
const CONV_Y = 171

const cablePath = (y: number) => `M 96 ${y} C 130 ${y}, 150 ${CONV_Y}, ${CONV_X} ${CONV_Y}`

function Box({ x, label, sub, delay }: { x: number; label: string; sub: string; delay: number }) {
  return (
    <g>
      <rect
        x={x}
        y={CONV_Y - 22}
        width="72"
        height="44"
        fill="#191811"
        stroke={LINE}
        strokeWidth="1"
        style={{ animation: `box-seal 6s ease-in-out ${delay}s infinite` }}
      />
      <text x={x + 8} y={CONV_Y - 6} fill={INK} fontSize="8.5" style={MONO}>
        {label}
      </text>
      <text x={x + 8} y={CONV_Y + 10} fill={DIM} fontSize="8" style={MONO}>
        {sub}
      </text>
    </g>
  )
}

export function TracePanel() {
  return (
    <div className="relative min-h-[360px] overflow-hidden bg-[#141310] lg:min-h-full">
      <svg
        viewBox="0 0 480 356"
        className="trace-scene absolute inset-0 h-full w-full"
        preserveAspectRatio="xMidYMid meet"
        aria-hidden
      >
        {/* registration corner marks */}
        {[
          [30, 34, 1, 1],
          [450, 34, -1, 1],
          [30, 340, 1, -1],
          [450, 340, -1, -1],
        ].map(([cx, cy, sx, sy], i) => (
          <path
            key={i}
            d={`M ${cx} ${cy + sy * 12} L ${cx} ${cy} L ${cx + sx * 12} ${cy}`}
            stroke={DIM}
            strokeWidth="1"
            fill="none"
          />
        ))}

        {/* cables */}
        {SRC.map((s, i) => (
          <path key={i} d={cablePath(s.y)} stroke={LINE} strokeWidth="1" fill="none" />
        ))}
        <line x1="248" y1={CONV_Y} x2="284" y2={CONV_Y} stroke={LINE} strokeWidth="1" />
        <line x1="356" y1={CONV_Y} x2="392" y2={CONV_Y} stroke={LINE} strokeWidth="1" />

        {/* source terminals */}
        {SRC.map((s, i) => (
          <g key={i}>
            <rect x="64" y={s.y - 6} width="32" height="12" fill="#1d1c14" stroke={LINE} strokeWidth="1" />
            <rect
              x="66"
              y={s.y - 4}
              width="8"
              height="8"
              fill={s.mirror ? DIM : INK}
              style={{ animation: `pin 6s ease-in-out ${i * 0.5}s infinite` }}
            />
            <text x="36" y={s.y + 3} fill={DIM} fontSize="7.5" style={MONO} textAnchor="end">
              SRC_{String(i + 1).padStart(2, '0')}
            </text>
          </g>
        ))}

        {/* packets travelling the cables, then collapsing */}
        {SRC.map((s, i) => (
          <rect
            key={i}
            width="5"
            height="5"
            fill={s.mirror ? DIM : ACCENT}
            style={
              {
                offsetPath: `path("${cablePath(s.y)}")`,
                offsetRotate: '0deg',
                animation: `packet 6s cubic-bezier(0.5,0,0.5,1) ${i * 0.5}s infinite`,
              } as React.CSSProperties
            }
          />
        ))}

        {/* the single artefact continuing down the chain */}
        <rect
          width="6"
          height="6"
          fill={INK}
          style={
            {
              offsetPath: `path("M ${CONV_X} ${CONV_Y} L 392 ${CONV_Y}")`,
              animation: 'artefact 6s cubic-bezier(0.4,0,0.6,1) infinite',
            } as React.CSSProperties
          }
        />

        <Box x={CONV_X} label="CANON" sub="6 -> 1" delay={0.2} />
        <Box x={284} label="WEIGH" sub="k = 2" delay={0.5} />
        <Box x={392} label="ASSESS" sub="LR 3.67" delay={0.85} />

        {/* the ledger — blocks seal in sequence */}
        {[0, 1, 2, 3, 4].map((b) => (
          <g key={b} style={{ animation: `ledger 6s ease-in-out ${1 + b * 0.28}s infinite` }}>
            <rect
              x={92 + b * 60}
              y="300"
              width="48"
              height="26"
              fill="#191811"
              stroke={b === 4 ? ACCENT : LINE}
              strokeWidth="1"
            />
            <text x={116 + b * 60} y="311" fill={DIM} fontSize="6.5" style={MONO} textAnchor="middle">
              #{String(b + 41).padStart(3, '0')}
            </text>
            <text x={116 + b * 60} y="321" fill={INK} fontSize="7" style={MONO} textAnchor="middle">
              {['9f2c', '41ab', '5c90', '7edf', 'c19d'][b]}
            </text>
            {b < 4 && (
              <line
                x1={140 + b * 60}
                y1="313"
                x2={152 + b * 60}
                y2="313"
                stroke={LINE}
                strokeWidth="1"
              />
            )}
          </g>
        ))}
        <text x="92" y="292" fill={DIM} fontSize="7" style={MONO}>
          EVIDENCE LEDGER · APPEND-ONLY · HASH-CHAINED
        </text>
      </svg>
    </div>
  )
}
