'use client'

import { NAV_LINKS } from '@/constants';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react'

const Footer = () => {
  const pathname = usePathname();

  return (
    <footer className='flex flex-col gap-4 h-auto p-4 border-t-2 border-gray-300 w-full items-start justify-between'>
      <div className='flex flex-col sm:flex-row gap-4 items-start justify-between w-full'>
      <section className='flex flex-col gap-3 items-start p-4 sm:w-1/2'>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-text">
      KdramaVibe
    </h1>
    <p className="text-base text-text sm:text-xl font-medium opacity-90">
      K-Drama Dreams, K-Actor Gleams 💫
    </p>
      
      </section>
      <section className='flex flex-col gap-3 p-4 items-start sm:w-1/3'>
        <h2 className='text-xl font-semibold text-text'>
          Quick links
        </h2>
         <ul className="flex flex-col gap-2 items-start w-full">
                  {NAV_LINKS.map((link, index) => {
                    const isActive: boolean = link.href === pathname;
                    return (
                      <li key={index} className="border-text border-b">
                        <Link
                          href={link.href}
                          className={`font-medium transition-colors duration-300 ${
                            isActive
                              ? "text-primary"
                              : "text-text hover:text-primary"
                          }`}
                        >
                          {link.name}
                        </Link>
                      </li>
                    );
                  })}
                 <li className="border-text border-b">
                        <Link
                        target="_blank" rel="noopener noreferrer"
                          href="https://www.florakamau.tech/#contact"
                          className="font-medium transition-colors duration-300 text-text hover:text-primary"
                        >
                          Contact me
                        </Link>
                        </li>
                </ul>
      </section>
      </div>
      <section className='self-center'>
        <p className="text-primary">
          &copy; 2025 KDramaVibe. All rights reserved.
        </p>
        <p className="text-sm ">
  Data and text content on this site are sourced from
  <Link
    href="https://www.wikipedia.org/"
    target="_blank"
    rel="noopener noreferrer"
    className="underline hover:text-pink-600"
  >
{" "}Wikipedia
  </Link>, available under the 
  <Link
    href="https://creativecommons.org/licenses/by-sa/3.0/"
    target="_blank"
    rel="noopener noreferrer"
    className="underline hover:text-pink-600"
  >
    {" "}Creative Commons Attribution-ShareAlike License
  </Link>.
</p>

        </section>
    </footer>
  )
}

export default Footer
