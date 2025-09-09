import { useState} from "react";
import type { FormEvent } from "react";
import React from "react";
import copy from "copy-to-clipboard";
import { ToastContainer, toast } from "react-toastify";

const CreatePlan = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [importance, setImportance] = useState(1);

  const notify = (message: string, status: number, copyable = false) => {
    const toastOptions = {
      position: "bottom-right" as const,
      autoClose: 3000,
      onClick: copyable
        ? () => {
            copy(message);
            toast.success("Copied to clipboard!");
          }
        : undefined,
        className: copyable ? "cursor-copy" : "",
    };

    if (status) {
      toast.success(message, toastOptions);
    } else {
      toast.error(message, toastOptions);
    }
  };

  const importanceOptions = [
        { value: 1, label: "Not Important", color: "bg-green-500" },
        { value: 2, label: "Important", color: "bg-yellow-400" },
        { value: 3, label: "Very Important", color: "bg-red-500" },
    ];

  const selected = importanceOptions.find(opt => opt.value === importance);


  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try{
        const body = JSON.stringify({"title": title, "description": description, "important_type": importance});
        const resp = await fetch("http://13.250.98.246:5599/create-plan",{
            method: "POST",
            body: body,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if(!resp.ok) throw new Error("Error While Creating Plan");
        const json = await resp.json()
        const data: PlanInterface = {
            uuid: json.plan,
            title: title,
            type: importance
        }
        notify(`Success creating plan, click the notif below to copy the uuid`, 1);
        notify(`${data.uuid}`, 1, true);
        window.api.setCachedPlan(data);
    }catch(e: any){
        notify(e.message, 0);
    }
    
  };

  return (
    <div className="viewplan-box w-full h-full flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="h-3/4 w-3/4 flex flex-col bg-white shadow-md rounded-lg overflow-hidden"
      >
        <div className="bg-zinc-500 w-full h-10 rounded-t-lg gap-2 flex items-center justify-center px-4">
          <div className="bg-lime-500 w-4 h-4 rounded-full"></div>
          <input
            type="text"
            className="ml-3 flex-1 bg-transparent outline-none text-white placeholder-white text-xl font-semibold w-10"
            placeholder="Enter Title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="bg-zinc-100 w-full h-full flex flex-col gap-y-4 rounded-b-lg  py-6 px-6">
           <div className="flex gap-3 items-center">
            <label className="text-gray-700 font-medium">Importance:</label>
            
            <div className="relative inline-flex items-center">
            <div className={`absolute left-2 w-3 h-3 rounded-full ${selected?.color} transition-colors duration-200`} />
            
            <select
                className="appearance-none pl-6 pr-6 py-2 rounded border border-gray-300 bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 text-sm"
                value={importance}
                onChange={(e) => setImportance(Number(e.target.value))}
            >
                {importanceOptions.map(opt => (
                <option key={opt.value} value={opt.value}>
                    {opt.label}
                </option>
                ))}
            </select>
            </div>
        </div>

          <textarea
            className="description-area p-3 rounded border border-gray-300 min-h-40 max-h-100 resize-none"
            placeholder="Enter your plan description..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>

          <button
            type="submit"
            className="self-end bg-emerald-700 text-white px-4 py-2 rounded hover:bg-emerald-800 transition"
          >
            Create Plan
          </button>
        </div>
      </form>
      <ToastContainer />
    </div>
  );
};

export default CreatePlan;
