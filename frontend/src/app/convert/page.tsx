'use client'

import * as Select from '@radix-ui/react-select'
import { useState } from 'react'
import { ChevronDownIcon } from '@radix-ui/react-icons'
import type { paths } from '@shared/types/api'

type ConvertRequest = paths['/convert-date']['post']['requestBody']['content']['application/json']
type ConvertResponse = paths['/convert-date']['post']['responses']['200']['content']['application/json']

const HARPTOS_MONTHS = [
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

export default function ConvertPage() {
  const [harptosInput, setHarptosInput] = useState<ConvertRequest>({
    year: null,
    month: null,
    day: null,
    calendar: 'harptos',
    gregorian: null,
  })

  const [gregorianInput, setGregorianInput] = useState('')
  const [gregorianResult, setGregorianResult] = useState<string | null>(null)
  const [harptosResult, setHarptosResult] = useState<ConvertResponse['calendar_date'] | null>(null)

  const convertFromHarptos = async () => {
    const body: ConvertRequest = {
      ...harptosInput,
      gregorian: null,
      calendar: 'harptos',
    }

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/convert-date`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    const data: ConvertResponse = await res.json()
    setGregorianResult(data?.gregorian_date ?? null)
  }

  const convertFromGregorian = async () => {
    const body: ConvertRequest = {
      gregorian: gregorianInput,
      calendar: 'harptos',
      year: null,
      month: null,
      day: null,
    }

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/convert-date`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    const data: ConvertResponse = await res.json()
    setHarptosResult(data?.calendar_date ?? null)
  }

  return (
    <main className="max-w-xl mx-auto p-6 space-y-12">
      <h1 className="text-3xl font-bold text-white text-center">Harptos ↔ Gregorian Converter</h1>

      {/* Harptos → Gregorian */}
      <section className="bg-gray-900 text-white border border-gray-700 rounded-lg p-6 space-y-4">
        <h2 className="text-xl font-semibold">Harptos → Gregorian</h2>

        <input
          className="w-full bg-gray-800 p-2 rounded border border-gray-600 text-white placeholder-gray-400"
          type="number"
          placeholder="Year"
          value={harptosInput.year ?? ''}
          onChange={(e) =>
            setHarptosInput({ ...harptosInput, year: Number(e.target.value) || null })
          }
        />

        <Select.Root
          value={harptosInput.month ?? ''}
          onValueChange={(value) =>
            setHarptosInput({ ...harptosInput, month: value as ConvertRequest['month'] })
          }
        >
          <Select.Trigger className="w-full bg-gray-800 p-2 rounded border border-gray-600 flex justify-between items-center text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
            <Select.Value placeholder="Select Month" />
            <ChevronDownIcon />
          </Select.Trigger>
          <Select.Content className="bg-gray-900 border border-gray-700 rounded shadow-lg text-white z-50">
            {HARPTOS_MONTHS.map((month) => (
              <Select.Item
                key={month}
                value={month}
                className="px-4 py-2 hover:bg-gray-700 cursor-pointer text-white"
              >
                <Select.ItemText>{month}</Select.ItemText>
              </Select.Item>
            ))}
          </Select.Content>
        </Select.Root>

        <input
          className="w-full bg-gray-800 p-2 rounded border border-gray-600 text-white placeholder-gray-400"
          type="number"
          placeholder="Day"
          value={harptosInput.day ?? ''}
          onChange={(e) =>
            setHarptosInput({ ...harptosInput, day: Number(e.target.value) || null })
          }
        />

        <button
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
          onClick={convertFromHarptos}
        >
          Convert to Gregorian
        </button>

        {gregorianResult && (
          <p className="text-green-400 font-mono mt-2">Gregorian Date: {gregorianResult}</p>
        )}
      </section>

      {/* Gregorian → Harptos */}
      <section className="bg-gray-900 text-white border border-gray-700 rounded-lg p-6 space-y-4">
        <h2 className="text-xl font-semibold">Gregorian → Harptos</h2>

        <input
          type="date"
          className="w-full bg-gray-800 p-2 rounded border border-gray-600 text-white"
          value={gregorianInput}
          onChange={(e) => setGregorianInput(e.target.value)}
        />

        <button
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
          onClick={convertFromGregorian}
        >
          Convert to Harptos
        </button>

        {harptosResult && (
          <p className="text-green-400 font-mono mt-2">
            Harptos Date: {harptosResult.month} {harptosResult.day}, Year {harptosResult.year}
          </p>
        )}
      </section>
    </main>
  )
}
