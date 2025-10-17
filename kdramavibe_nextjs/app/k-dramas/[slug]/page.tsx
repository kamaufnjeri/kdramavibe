import KdramaDetails from "@/components/kdramas/KdramaDetails";
import getSingleKdrama from "@/lib/getSingleKdrama";

interface PageProps {
    params: {
        slug: string;
    }
}

export default async function SingleKdramaPage ({ params }: PageProps) {
    const { slug } = params; 

    const kdrama = await getSingleKdrama(slug);

    return (
        <div className="flex justify-center m-4 p-4">
                    <KdramaDetails kdrama={kdrama}/>

        </div>
    )
}