import { KactorDetail } from '@/interfaces';
import React from 'react';
import Link from 'next/link';
import KactorDramasDetails from './KactorDramasDetails';
import ImageWithFallback from '../kdramas/ImageWithFallback';
import DisplayList from '../kdramas/DisplayList';
import { FaEye } from 'react-icons/fa';

interface KactorDetailsProps {
  kactor: KactorDetail; // Kactor detailed data
}

const KactorDetails: React.FC<KactorDetailsProps> = ({ kactor }) => {
  return (
    <div className="flex flex-col gap-6 items-center justify-center w-full">
      {/* Main container for kactor details */}
      <div className="rounded-2xl border border-border bg-background/60 shadow-sm 
                      text-text p-6 lg:w-3/4 w-full flex flex-col gap-6">

        {/* Votes by Dramabeans */}
        {(kactor.no_of_votes && kactor.dramabeans_url) && (
          <div className="flex flex-wrap justify-between gap-1 items-center border border-accent/30 rounded-xl px-3 py-2 mt-2">
            <p className="text-sm text-purple-300 italic font-semibold tracking-wide">
              By <Link
                href={kactor?.dramabeans_url}
                target="_blank"
                rel="noreferrer noopener"
                className="text-accent not-italic hover:underline hover:text-pink-600 transition-colors duration-200"
              >
                Dramabeans
              </Link>
            </p>

            {/* Display number of votes */}
            {kactor.no_of_votes && (
              <span className="inline-flex items-center gap-1 text-sm font-medium">
                <FaEye className="text-gray-400" size={14} />
                <span>{parseInt(kactor.no_of_votes).toLocaleString()}</span>
              </span>
            )}
          </div>
        )}

        {/* Title + Age */}
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="font-extrabold text-3xl text-primary">{kactor.name}</h1>
          <div className='flex flex-wrap gap-2 self-end'>
            {kactor.age && (
              <p className='text-right font-semibold text-lg text-accent'>{kactor.age} years</p>
            )}
          </div>
        </div>

        {/* Images and Description */}
        <div className="flex flex-col gap-6">
          <div className='flex flex-col sm:flex-row gap-2 justify-between w-full'>
            {kactor.image_url && (<ImageWithFallback
              alt={kactor.name}
              imageSrc={kactor.image_url}
              containerStyles={'w-[300px] h-full'}
              gender={kactor.gender ? kactor.gender : null}
              className="object-contain self-start bg-gray-100 rounded-xl shadow-md"
            />)}
            {kactor.dramabeans_image_url && (
              <ImageWithFallback
                alt={kactor.name}
                imageSrc={kactor.dramabeans_image_url}
                containerStyles={'w-[300px] h-full'}
                gender={kactor.gender ? kactor.gender : null}
                className="object-contain self-start bg-gray-100 rounded-xl shadow-md"
              />
            )}
          </div>

          <div className="flex flex-col gap-5 flex-1">
            {/* Description */}
            {kactor.description && (
              <div className="text-base leading-relaxed overflow-y-auto custom-scrollbar max-h-96">
                <p className="whitespace-pre-line">{kactor.description}</p>
              </div>
            )}

            {/* Info fields */}
            <div className="flex flex-col gap-2 text-sm sm:text-base">

              {/* Alternate Names */}
              {Array.isArray(kactor.alternate_names) && kactor.alternate_names.length > 0 && (
                <InfoRow title="Also Known As" items={kactor.alternate_names} />
              )}

              {kactor.birthday && <InfoField label="Born" value={kactor.birthday} />}
              {kactor.birthplace && <InfoField label="Place of Birth" value={kactor.birthplace} />}
              {kactor.gender && <InfoField label="Gender" value={kactor.gender === 'female' ? 'Woman' : kactor.gender === "male" ? "Man" : ''} />}

              {/* Occupations */}
              {Array.isArray(kactor.occupations) && kactor.occupations.length > 0 && (
                <InfoRow
                  title={kactor.occupations.length === 1 ? "Occupation" : "Occupations"}
                  items={kactor.occupations}
                />
              )}
              {kactor.years_active && <InfoField label="Years Active" value={kactor.years_active} />}
              {Array.isArray(kactor.agents) && kactor.agents.length > 0 && (
                <InfoRow
                  title={kactor.agents.length === 1 ? "Agent" : "Agents"}
                  items={kactor.agents}
                />
              )}
              {kactor.partner_or_spouse && <InfoField label="Partner or Spouse" value={kactor.partner_or_spouse} />}
              {Array.isArray(kactor.children) && kactor.children.length > 0 && (
                <InfoRow
                  title="Children"
                  items={kactor.children}
                />
              )}
              {kactor.height && <InfoField label="Height" value={kactor.height} />}

            </div>
          </div>
        </div>
      </div>

      {/* Source / External Links */}
      <div className="flex items-center justify-between flex-wrap gap-3 pt-3 border-t border-border mt-2">
        {kactor.wikipedia_url && (
          <Link
            href={kactor.wikipedia_url}
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

      {/* Kdramas of the Kactor */}
      {kactor.kdramas && <KactorDramasDetails kdramas={kactor.kdramas} />}
    </div>
  )
};

export default KactorDetails;

/* Helper Components for displaying info fields */
const InfoField = ({ label, value }: { label: string; value: string | number }) => (
  <div className="flex flex-wrap gap-1">
    <h3 className="font-bold">{label}:</h3>
    <p>{value}</p>
  </div>
)

const InfoRow = ({ title, items }: { title: string; items: (string | number)[] }) => (
  <div className="flex flex-wrap gap-1">
    <h3 className="font-bold">{title}:</h3>
    <DisplayList items={items} />
  </div>
)
