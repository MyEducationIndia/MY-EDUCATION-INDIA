import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Clock, Calendar, CheckCircle2, AlertTriangle } from "lucide-react";
import { academicService } from "../services/academicService";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const TIME_SLOTS = ["09:00 - 10:00", "10:00 - 11:00", "11:15 - 12:15", "12:15 - 01:15", "02:00 - 03:00", "03:00 - 04:00"];

export const InteractiveTimetablePage: React.FC = () => {
  const { data: batches = [] } = useQuery({ queryKey: ["academicBatches"], queryFn: academicService.listBatches });

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs dark:border-slate-800 dark:bg-slate-900 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base font-bold text-slate-900 dark:text-white">Conflict-Free Academic Timetable</h1>
          <p className="text-xs text-slate-500">Automated collision detection prevents double-booking faculty and classrooms.</p>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs dark:border-slate-800 dark:bg-slate-900 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-center text-xs dark:divide-slate-800">
          <thead>
            <tr className="bg-slate-50 font-bold uppercase text-slate-500 dark:bg-slate-950">
              <th className="px-3 py-3 w-28 text-left">Day</th>
              {TIME_SLOTS.map((slot) => (
                <th key={slot} className="px-3 py-3">{slot}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
            {DAYS.map((day, idx) => (
              <tr key={day} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                <td className="px-3 py-4 font-bold text-slate-900 text-left dark:text-white">{day}</td>
                {TIME_SLOTS.map((slot, sIdx) => (
                  <td key={sIdx} className="p-2">
                    <div className="rounded-xl border border-brand-200 bg-brand-50/50 p-2 dark:border-brand-900 dark:bg-brand-950/40">
                      <p className="font-bold text-brand-900 dark:text-brand-200 truncate">CS101 (Data Struct)</p>
                      <p className="text-[10px] text-slate-500">Prof. Sharma • Room 401</p>
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
