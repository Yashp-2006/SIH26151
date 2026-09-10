// Clean SVG primitives — no icon library. strokeWidth 1.75, currentColor.

type P = { size?: number; className?: string }

const base = (size: number, className?: string) => ({
  width: size,
  height: size,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.75,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
  className,
  'aria-hidden': true,
})

export const ChevronDown = ({ size = 14, className }: P) => (
  <svg {...base(size, className)}>
    <path d="m6 9 6 6 6-6" />
  </svg>
)

export const ArrowRight = ({ size = 15, className }: P) => (
  <svg {...base(size, className)}>
    <path d="M5 12h14M13 6l6 6-6 6" />
  </svg>
)

export const Link2 = ({ size = 14, className }: P) => (
  <svg {...base(size, className)}>
    <path d="M9 17H7a5 5 0 0 1 0-10h2M15 7h2a5 5 0 0 1 0 10h-2M8 12h8" />
  </svg>
)

export const Check = ({ size = 14, className }: P) => (
  <svg {...base(size, className)}>
    <path d="M20 6 9 17l-5-5" />
  </svg>
)

export const Minus = ({ size = 14, className }: P) => (
  <svg {...base(size, className)}>
    <path d="M5 12h14" />
  </svg>
)

export const Lock = ({ size = 13, className }: P) => (
  <svg {...base(size, className)}>
    <rect x="5" y="11" width="14" height="10" rx="1.5" />
    <path d="M8 11V8a4 4 0 0 1 8 0v3" />
  </svg>
)

export const Search = ({ size = 14, className }: P) => (
  <svg {...base(size, className)}>
    <circle cx="11" cy="11" r="7" />
    <path d="m21 21-4.3-4.3" />
  </svg>
)
