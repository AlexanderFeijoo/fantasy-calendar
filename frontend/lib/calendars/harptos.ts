export const HARPTOS_MONTHS = [
  'Hammer',
  'Alturiak',
  'Ches',
  'Tarsakh',
  'Mirtul',
  'Kythorn',
  'Flamerule',
  'Eleasis',
  'Eleint',
  'Marpenoth',
  'Uktar',
  'Nightal',
] as const

export type HarptosMonth = typeof HARPTOS_MONTHS[number]
