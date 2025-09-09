import React from "react";
import { useNavigate } from "react-router-dom";

interface PlanListProps {
  plan: PlanInterface[];
}
const PlanShortComponent = ({ type, uuid, title }: { type: Number; uuid: string; title: string }) => {
  const navigate = useNavigate();
  const color = (type === 1 ? "bg-green-500" : type === 2 ? "bg-amber-500" : "bg-red-500")


  return (
    <div  onClick={() => navigate(`/view-plan/${uuid}`)}
    className="cursor-default important-type-area flex items-center gap-2 bg-gray-300 px-3 py-1 rounded w-fit hover:bg-gray-400 hover:scale-110 transition duration-300">
      <div className={`w-3 h-3 rounded-full ${color}`}></div>
      <p className="text-sm text-gray-800">{title}</p>
    </div>
  );
};

const PlanList: React.FC<PlanListProps> = ({ plan }) => {
    const showPlans = () => {
        if(plan.length === 0) return <h1>No Plans</h1>
        else{
            return plan.map((p, i)=><div key={i}><PlanShortComponent type={p.type} uuid={p.uuid} title={p.title}/></div>)
        }
    }
    return(
        <div className="w-full h-full flex items-center justify-center">
            <div className="w-3/4 h-fit flex flex-col">
                <div className="bg-zinc-500 w-full h-fit min-h-10 rounded-t-lg gap-2 flex items-center justify-center">
                    <div className="bg-lime-500 w-4 h-4 rounded-full"></div>
                    <h1 className="title-area text-xl font-semibold text-center text-white">
                      Plans You Have Seen Before
                    </h1>
                </div>
                <div className="bg-zinc-100 w-full h-full min-h-40 flex flex-row flex-wrap gap-x-5 gap-y-5 rounded-b-lg py-10 px-10">
                    {showPlans()}
                </div>
            </div>
        </div>
    );
}

export default PlanList;