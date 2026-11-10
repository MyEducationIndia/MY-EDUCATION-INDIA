import React, { useState } from "react";
import { Calendar, Plus, Clock, MapPin, CheckCircle } from "lucide-react";

export const ExamScheduleCalendarPage: React.FC = () => {
  const [schedules] = useState([
    { id: "1", date: "2026-11-20", time: "10:00 AM - 01:00 PM", course: "B.Tech Computer Science & AI", subject: "CS101 - Data Structures & Algorithms", room: "Lecture Hall A-102", invigilator: "Dr. Vikram Sengupta" },
    { id: "2", date: "2026-11-23", time: "10:00 AM - 01:00 PM", course: "B.Tech Computer Science & AI", subject: "CS102 - Object Oriented Programming in Java", room: "Lecture Hall A-102", invigilator: "Prof. Priya Ramaswamy" },
    { id: "3", date: "2026-11-25", time: "02:00 PM - 05:00 PM", course: "MBA Executive", subject: "MBA201 - Strategic Financial Modeling", room: "Seminar Hall S-201", invigilator: "Dr. Amit Mukherjee" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-5 dark:border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
            <Calendar className="h-7 w-7 text-amber-500" />
            Institutional Examination Timetable & Seating Matrix
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Publish theory and practical exam datesheets, room allotments, and invigilator duties.
          </p>
        </div>
        <button
          type="button"
          onClick={() => alert("Schedule new exam paper")}
          className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-700 transition"
        >
          <Plus className="h-4 w-4" />
          <span>Schedule Paper</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {schedules.map((s) => (
          <div
            key={s.id}
            className="flex flex-col md:flex-row md:items-center justify-between gap-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-5 shadow-xs"
          >
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-indigo-600 bg-indigo-50 dark:bg-indigo-950 px-2 py-0.5 rounded-sm">
                  {s.date}
                </span>
                <span className="flex items-center gap-1 text-xs text-slate-500">
                  <Clock className="h-3.5 w-3.5" />
                  {s.time}
                </span>
              </div>
              <h3 className="mt-2 text-base font-bold text-slate-900 dark:text-white">{s.subject}</h3>
              <p className="text-xs text-slate-500">{s.course}</p>
            </div>
            <div className="flex flex-col md:items-end text-xs text-slate-600 dark:text-slate-300 gap-1">
              <span className="flex items-center gap-1 font-semibold text-slate-800 dark:text-slate-200">
                <MapPin className="h-3.5 w-3.5 text-amber-500" />
                {s.room}
              </span>
              <span className="text-slate-500">Invigilator: {s.invigilator}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
