import { KdramaDetail } from '@/interfaces'
import React from 'react'
import ImageWithFallback from './ImageWithFallback'
import Link from 'next/link'
import DisplayList from './DisplayList'
import KdramaCastsDetails from './KdramaCastsDetails'

interface KdramaDetailsProps {
  kdrama: KdramaDetail
}

const KdramaDetails: React.FC<KdramaDetailsProps> = ({ kdrama }) => {
  return (
    <div className="flex flex-col gap-6 items-center justify-center w-full">
      <div className="rounded-2xl border border-border bg-background/60 shadow-sm 
                      text-text p-6 lg:w-3/4 w-full flex flex-col gap-6">
        
        {/* 🏷️ Title + Years */}
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="font-extrabold text-3xl text-primary">{kdrama.title}</h1>
          {kdrama.start_year && (
            <div className="text-right font-semibold text-lg text-accent">
              {kdrama.start_year}
              {kdrama.end_year && kdrama.end_year !== kdrama.start_year && (
                <> – {kdrama.end_year}</>
              )}
            </div>
          )}
        </div>

        {/* 📺 Image + Info */}
        <div className="flex flex-col lg:flex-row gap-6">
          <ImageWithFallback
            alt={kdrama.title}
            imageSrc={kdrama.image_url}
            className="object-contain self-start bg-gray-100 rounded-xl shadow-md"
          />

          <div className="flex flex-col gap-5 flex-1">
            
            {/* 🧾 Plot / Description */}
            {kdrama.plot && (
              <div className="text-base leading-relaxed overflow-y-auto custom-scrollbar max-h-96">
                <p className="whitespace-pre-line">{kdrama.plot}</p>
              </div>
            )}

            {/* 🎭 Info Fields */}
            <div className="flex flex-col gap-2 text-sm sm:text-base">
              
              {/* Genres */}
              {Array.isArray(kdrama.genres) && kdrama.genres.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  <h3 className="font-bold">Genres:</h3>
                  <ul className="flex flex-wrap gap-1">
                    {kdrama.genres.map((genre) => (
                      <li key={genre}>
                        <Link
                          href={`/?genre=${genre}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-secondary text-text px-2 py-1 rounded-md hover:bg-primary hover:text-white transition"
                        >
                          {genre}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Alternate Titles */}
              {Array.isArray(kdrama.alternate_titles) && kdrama.alternate_titles.length > 0 && (
                <InfoRow title="Also Known As" items={kdrama.alternate_titles} />
              )}

              {/* Directors */}
              {Array.isArray(kdrama.directors) && kdrama.directors.length > 0 && (
                <InfoRow
                  title={kdrama.directors.length === 1 ? "Director" : "Directors"}
                  items={kdrama.directors}
                />
              )}

              {/* Writers */}
              {Array.isArray(kdrama.writers) && kdrama.writers.length > 0 && (
                <InfoRow
                  title={kdrama.writers.length === 1 ? "Writer" : "Writers"}
                  items={kdrama.writers}
                />
              )}

              {/* Numeric / String Fields */}
              {kdrama.episodes && <InfoField label="Episodes" value={kdrama.episodes} />}
              {kdrama.seasons && <InfoField label="Seasons" value={kdrama.seasons} />}
              {kdrama.running_time && <InfoField label="Running Time" value={kdrama.running_time} />}

              {/* Networks */}
              {Array.isArray(kdrama.networks) && kdrama.networks.length > 0 && (
                <InfoRow
                  title={kdrama.networks.length === 1 ? "Network" : "Networks"}
                  items={kdrama.networks}
                />
              )}

              {/* Country */}
              {kdrama.country && <InfoField label="Country of Origin" value={kdrama.country} />}

              {/* Languages */}
              {Array.isArray(kdrama.languages) && kdrama.languages.length > 0 && (
                <InfoRow
                  title={kdrama.languages.length === 1 ? "Language" : "Languages"}
                  items={kdrama.languages}
                />
              )}
            </div>

            {/* 🔗 Source + Link */}
            <div className="flex items-center justify-between flex-wrap gap-3 pt-3 border-t border-border mt-2">
              {kdrama.wikipedia_url && (
                <Link
                  href={kdrama.wikipedia_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-pink-700 transition"
                >
                  Find Out More
                </Link>
              )}

              <p className="text-xs text-gray-500">
                Source:{' '}
                <Link
                  href="https://www.wikipedia.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline hover:text-pink-600"
                >
                  Wikipedia
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
     {kdrama.kactors && <KdramaCastsDetails kactors={kdrama.kactors}/>}
    </div>
  )
}

export default KdramaDetails

/* Helper Components */
const InfoField = ({ label, value }: { label: string; value: string | number }) => (
  <div className="flex flex-wrap gap-1">
    <h3 className="font-bold">{label}:</h3>
    <p>{value}</p>
  </div>
)

const InfoRow = ({ title, items }: { title: string; items: string[] }) => (
  <div className="flex flex-wrap gap-1">
    <h3 className="font-bold">{title}:</h3>
    <DisplayList items={items} />
  </div>
)
