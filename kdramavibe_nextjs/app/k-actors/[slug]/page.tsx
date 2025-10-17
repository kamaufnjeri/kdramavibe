import KactorDetails from "@/components/kactors/KactorDetails";
import getSingleKactor from "@/lib/getSingleKactor";

interface PageProps {
    params: {
        slug: string;
    }
}

export default async function SingleKactorPage ({ params }: PageProps) {
    const { slug } = params; 

    const kactor = await getSingleKactor(slug);

    return (
        <div className="flex justify-center m-4 p-4">
                    <KactorDetails kactor={kactor}/>

        </div>
    )
}