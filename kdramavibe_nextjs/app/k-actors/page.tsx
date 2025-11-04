import Banner from "@/components/common/Banner";
import KactorsFilterSection from "@/components/kactors/KactorsFilterSection";
import KactorsList from "@/components/kactors/KactorsList";
import { KactorsFilter } from "@/interfaces";
import getKactors from "@/lib/getKactors";
import React from "react";

interface PageProps {
  searchParams?: Promise<KactorsFilter>
}


export default async function KActorsPage({ searchParams }: PageProps) {
  const { name = '', age =  '', gender = '', ordering = "", page = "1" } = await searchParams ?? {};
  const kactorsResponse = await getKactors({ name, age, gender, ordering, page });

  return (
    
    <div>
      <Banner/>
     <KactorsFilterSection searchParams={{
      name,
      gender,
      age,
      ordering,
      page
     }}
  
     noOfPages={kactorsResponse.total_pages}
     />
     <KactorsList kactors={kactorsResponse?.results}/>
    </div>
  );
}
