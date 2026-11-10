import React, { useState } from "react";
import { Sliders, Save, CheckCircle2 } from "lucide-react";

export const ExamBuilderPage: React.FC = () => {
  const [title, setTitle] = useState("B.Tech CSE Mid-Term Computer Based Exam 2026");
  const [duration, setDuration] = useState(90);
  const [totalMarks, setTotalMarks] = useState(100);
  const [shuffleQuestions, setShuffleQuestions] = useState(true);
  const [shuffleOptions, setShuffleOptions] = useState(true);
  const [allowCalc, setAllowCalc] = useState(false);

  return (
    <div className="space-y-6">
      <div className="border-b border-slate-200 pb-5 dark:border-slate-800">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2.5">
          <Sliders className="h-7 w-7 text-cyan-600 dark:text-cyan-400" />
          Interactive Visual CBT Exam Builder
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Configure question pools, negative marking ratios, scientific calculator access, and randomized delivery rules.
        </p>
      </div>

      <div className="max-w-3xl rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 shadow-xs space-y-5">
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
            Examination Template Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-bold text-slate-900 dark:text-white"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
              Duration (Minutes)
            </label>
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-bold"
            />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
              Total Paper Marks
            </label>
            <input
              type="number"
              value={totalMarks}
              onChange={(e) => setTotalMarks(Number(e.target.value))}
              className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 py-2 px-3 text-sm font-bold"
            />
          </div>
        </div>

        <div className="space-y-3 pt-2">
          <label className="flex items-center gap-2.5 text-sm font-semibold text-slate-800 dark:text-slate-200">
            <input
              type="checkbox"
              checked={shuffleQuestions}
              onChange={(e) => setShuffleQuestions(e.target.checked)}
              className="h-4 w-4 rounded-sm text-cyan-600 focus:ring-cyan-500"
            />
            <span>Randomize Question Sequence per Candidate (Unique Random Seed)</span>
          </label>
          <label className="flex items-center gap-2.5 text-sm font-semibold text-slate-800 dark:text-slate-200">
            <input
              type="checkbox"
              checked={shuffleOptions}
              onChange={(e) => setShuffleOptions(e.target.checked)}
              className="h-4 w-4 rounded-sm text-cyan-600 focus:ring-cyan-500"
            />
            <span>Shuffle Multiple Choice Option Alternatives</span>
          </label>
          <label className="flex items-center gap-2.5 text-sm font-semibold text-slate-800 dark:text-slate-200">
            <input
              type="checkbox"
              checked={allowCalc}
              onChange={(e) => setAllowCalc(e.target.checked)}
              className="h-4 w-4 rounded-sm text-cyan-600 focus:ring-cyan-500"
            />
            <span>Enable On-Screen Scientific Calculator in Candidate Interface</span>
          </label>
        </div>

        <button
          type="button"
          onClick={() => alert("Exam template saved successfully!")}
          className="flex items-center gap-2 rounded-lg bg-cyan-600 px-5 py-2.5 text-xs font-bold text-white shadow-xs hover:bg-cyan-700 transition"
        >
          <Save className="h-4 w-4" />
          <span>Save Examination Blueprint</span>
        </button>
      </div>
    </div>
  );
};
