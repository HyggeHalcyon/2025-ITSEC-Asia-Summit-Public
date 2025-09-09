import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";

interface PlanData {
  uuid: string;
  title: string;
  description: any;
  important_type: number;
}

const ImportantType = ({ type }: { type: number }) => {
  const tag = {
    color: type === 1 ? "bg-green-500" : type === 2 ? "bg-amber-500" : "bg-red-500",
    info: type === 1 ? "Not Important" : type === 2 ? "Important" : "Very Important",
  };

  return (
    <div className="important-type-area flex items-center gap-2 bg-gray-300 px-3 py-1 rounded w-fit">
      <div className={`w-3 h-3 rounded-full ${tag.color}`}></div>
      <p className="text-sm text-gray-800">{tag.info}</p>
    </div>
  );
};

const ViewPlan = () => {
  const { uuid } = useParams();
  const [planData, setPlanData] = useState<PlanData | null>(null);
  const [error, setError] = useState("");
  const descriptionBox = useRef<HTMLParagraphElement>(null);
  const titleBox = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    const fetchPlan = async () => {
      try {
        const res = await fetch(`http://13.250.64.232:5599/get-plan/${uuid}`);
        if (!res.ok) throw new Error("Plan not found");
        const data = await res.json();
        setPlanData(data.plan);
      } catch (err: any) {
        setError(err.message || "Error fetching plan");
      }
    };
    fetchPlan();
  }, [uuid]);

  useEffect(() => {
    if (descriptionBox.current && planData?.description) {
      descriptionBox.current.innerHTML = planData.description;
    }
  }, [planData]); 

  if (error) return <p className="text-red-500">{error}</p>;
  if (!planData) return <p>Loading...</p>;

  return (
    <div className="w-full h-full flex items-center justify-center">
        <div className="h-3/4 w-3/4 flex flex-col">
          <div className="bg-zinc-500 w-full h-fit min-h-10 rounded-t-lg gap-2 flex items-center justify-center">
            <div className="bg-lime-500 w-4 h-4 rounded-full"></div>
            <h1 className="title-area text-xl font-semibold text-center text-white">
              {planData.title}
            </h1>
          </div>
          <div className="bg-zinc-100 w-full h-full flex flex-col gap-y-2 rounded-b-lg py-10 px-10">
            <ImportantType type={planData.important_type} />
            <div className="h-3/4 w-full justify-items-start">
              <p id="description-container" className="description-area text-4sm text-center" ref={descriptionBox}></p>
            </div>
          </div>
        </div>
    </div>
  );
};

export default ViewPlan;
