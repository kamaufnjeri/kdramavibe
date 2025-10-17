import { KactorDetail } from '@/interfaces'
import React from 'react'
import Link from 'next/link'
import KactorDramasDetails from './KactorDramasDetails'
import ImageWithFallback from '../kdramas/ImageWithFallback'
import DisplayList from '../kdramas/DisplayList'

interface KactorDetailsProps {
  kactor: KactorDetail
}

const KactorDetails: React.FC<KactorDetailsProps> = ({ kactor }) => {
  return (
    <div className="flex flex-col gap-6 items-center justify-center w-full">
      <div className="rounded-2xl border border-border bg-background/60 shadow-sm 
                      text-text p-6 lg:w-3/4 w-full flex flex-col gap-6">
        
        {/* 🏷️ Title + Years */}
        <div className="flex flex-wrap items-end justify-between gap-3">
          <h1 className="font-extrabold text-3xl text-primary">{kactor.name}</h1>
          <div className='flex flex-wrap gap-2 self-end'>
            {kactor.age && (
            
                
                <p className='text-right font-semibold text-lg text-accent'>{kactor.age} years</p>
            
          )}
          </div>
          
        </div>

        {/* 📺 Image + Info */}
        <div className="flex flex-col-reverse lg:flex-row gap-6">
          

          <div className="flex flex-col gap-5 flex-1">
            
            {/* 🧾 Plot / Description */}
            {kactor.description && (
              <div className="text-base leading-relaxed overflow-y-auto custom-scrollbar max-h-96">
                <p className="whitespace-pre-line">{kactor.description}</p>
              </div>
            )}

            {/* 🎭 Info Fields */}
            <div className="flex flex-col gap-2 text-sm sm:text-base">
              
             

              {/* Alternate Titles */}
              {Array.isArray(kactor.alternate_names) && kactor.alternate_names.length > 0 && (
                <InfoRow title="Also Known As" items={kactor.alternate_names} />
              )}
            {kactor.birthday && <InfoField label="Born" value={kactor.birthday} />}
            {kactor.birthplace && <InfoField label="Place of Birth" value={kactor.birthplace} />}
                        {kactor.gender && <InfoField label="Gender" value={kactor.gender === 'female' ? 'Woman' : kactor.gender === "male" ? "Man" : ''} />}



              {/* Directors */}
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
                  title={"Children"}
                  items={kactor.children}
                />
              )}
            {kactor.height && <InfoField label="Height" value={kactor.height} />}

             

           
          </div>
          
        </div>
        <ImageWithFallback
            alt={kactor.name}
            imageSrc={kactor.image_url}
            gender={kactor.gender ? kactor.gender : null}
            className="object-contain self-start bg-gray-100 rounded-xl shadow-md"
          />

      </div>
       {/* 🔗 Source + Link */}
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
    </div>
    
         {kactor.kdramas && <KactorDramasDetails kdramas={kactor.kdramas}/>}

    </div>
  )
};

export default KactorDetails

/* Helper Components */
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
