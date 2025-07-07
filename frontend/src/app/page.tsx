'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] text-foreground bg-background">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-4xl font-bold text-center">Fantasy Calendar</h1>
        <p className="text-center sm:text-left max-w-md text-base text-foreground/80">
          This is your campaign calendar hub. Use the converter to translate dates between Harptos and Gregorian formats.
        </p>

        <Link
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-6"
          href="/convert"
        >
          Open Date Converter
        </Link>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center text-sm text-foreground/60">
        <a
          className="hover:underline hover:underline-offset-4"
          href="https://github.com/AlexanderFeijoo/fantasy-calendar"
          target="_blank"
          rel="noopener noreferrer"
        >
          View on GitHub
        </a>
        <Link
          className="hover:underline hover:underline-offset-4"
          href="/convert"
        >
          /convert
        </Link>
      </footer>
    </div>
  )
}
