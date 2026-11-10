import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  BookOpen,
  Code,
  Sigma,
  Plus,
  Trash2,
  Edit2,
  CheckCircle2,
  Search,
  Filter,
  Layers,
  Sparkles,
  Volume2,
  FileCode,
  CheckSquare,
  HelpCircle,
  Tag,
  Languages,
  Eye,
  X,
  Save,
} from "lucide-react";
import { httpClient } from "@/api/httpClient";

interface QuestionItem {
  id: string;
  topic_id: string;
  question_code: string;
  question_type: "MCQ" | "MSQ" | "NUMERICAL" | "PROGRAMMING" | "AUDIO_COMPREHENSION" | "TRUE_FALSE";
  difficulty_level: "EASY" | "MEDIUM" | "HARD" | "EXPERT";
  bloom_level: string;
  language: string;
  question_text: string;
  latex_equations_json: string[];
  programming_metadata_json: Record<string, any>;
  options_json: Array<{ key: string; text: string }>;
  correct_answers_json: any[];
  explanation?: string;
  tags_json: string[];
  default_marks: number;
  negative_marks: number;
  approval_status: string;
  is_active: boolean;
  created_at: string;
}

interface QuestionBank {
  id: string;
  code: string;
  name: string;
  description?: string;
}

export const QuestionBankManagerPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedBankId, setSelectedBankId] = useState<string>("");
  const [difficultyFilter, setDifficultyFilter] = useState<string>("ALL");
  const [typeFilter, setTypeFilter] = useState<string>("ALL");
  const [languageFilter, setLanguageFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Modal State
  const [showModal, setShowModal] = useState(false);
  const [formType, setFormType] = useState<"MCQ" | "NUMERICAL" | "PROGRAMMING" | "AUDIO_COMPREHENSION">("MCQ");
  const [activeTab, setActiveTab] = useState<"PROMPT" | "OPTIONS" | "CODE" | "LATEX" | "TAGS">("PROMPT");

  // Form State
  const [questionCode, setQuestionCode] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [difficulty, setDifficulty] = useState<"EASY" | "MEDIUM" | "HARD" | "EXPERT">("MEDIUM");
  const [language, setLanguage] = useState("English");
  const [defaultMarks, setDefaultMarks] = useState(2.0);
  const [negativeMarks, setNegativeMarks] = useState(0.5);
  const [explanation, setExplanation] = useState("");
  const [latexInput, setLatexInput] = useState("\\int_0^\\infty e^{-x} dx = 1");
  const [latexList, setLatexList] = useState<string[]>(["\\int_0^\\infty e^{-x} dx = 1"]);
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>(["CALCULUS", "ENGINEERING_MATH"]);
  
  // Options state for MCQ
  const [options, setOptions] = useState([
    { key: "A", text: "1" },
    { key: "B", text: "0" },
    { key: "C", text: "\\infty" },
    { key: "D", text: "e" },
  ]);
  const [correctAnswer, setCorrectAnswer] = useState("A");

  // Programming question state
  const [progLang, setProgLang] = useState("Python 3");
  const [starterCode, setStarterCode] = useState("def solve(n: int) -> int:\n    # Write your solution here\n    pass\n");
  const [sampleInput, setSampleInput] = useState("5\n1 2 3 4 5");
  const [sampleOutput, setSampleOutput] = useState("15");

  // Queries
  const { data: banks = [] } = useQuery({
    queryKey: ["cbtQuestionBanks"],
    queryFn: async () => {
      const res = await httpClient.get<QuestionBank[]>("/cbt/question-bank", {
        params: { institute_id: "00000000-0000-0000-0000-000000000001" },
      });
      return res.data;
    },
  });

  const { data: questions = [], refetch: refetchQuestions, isLoading: questionsLoading } = useQuery({
    queryKey: ["cbtQuestions", difficultyFilter, typeFilter, languageFilter, searchQuery],
    queryFn: async () => {
      const params: Record<string, any> = {};
      if (difficultyFilter !== "ALL") params.difficulty_level = difficultyFilter;
      if (typeFilter !== "ALL") params.question_type = typeFilter;
      if (languageFilter !== "ALL") params.language = languageFilter;
      if (searchQuery) params.search = searchQuery;
      const res = await httpClient.get<QuestionItem[]>("/cbt/questions", { params });
      return res.data;
    },
  });

  // Mutations
  const createQuestionMutation = useMutation({
    mutationFn: async (payload: any) => {
      const res = await httpClient.post("/cbt/questions", payload);
      return res.data;
    },
    onSuccess: () => {
      refetchQuestions();
      setShowModal(false);
      resetForm();
    },
  });

  const deleteQuestionMutation = useMutation({
    mutationFn: async (questionId: string) => {
      await httpClient.delete(`/cbt/questions/${questionId}`);
    },
    onSuccess: () => {
      refetchQuestions();
    },
  });

  const resetForm = () => {
    setQuestionCode(`Q-${Math.floor(1000 + Math.random() * 9000)}`);
    setQuestionText("");
    setExplanation("");
    setOptions([
      { key: "A", text: "" },
      { key: "B", text: "" },
      { key: "C", text: "" },
      { key: "D", text: "" },
    ]);
    setCorrectAnswer("A");
  };

  const handleOpenCreate = () => {
    resetForm();
    setShowModal(true);
  };

  const handleSaveQuestion = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      topic_id: "00000000-0000-0000-0000-000000000001", // fallback default topic
      question_code: questionCode,
      question_type: formType,
      difficulty_level: difficulty,
      bloom_level: "UNDERSTAND",
      language: language,
      question_text: questionText,
      latex_equations: latexList,
      programming_metadata:
        formType === "PROGRAMMING"
          ? {
              language: progLang,
              starter_code: starterCode,
              sample_input: sampleInput,
              sample_output: sampleOutput,
            }
          : {},
      options: options,
      correct_answers: [correctAnswer],
      explanation: explanation,
      tags: tags,
      default_marks: defaultMarks,
      negative_marks: negativeMarks,
    };
    createQuestionMutation.mutate(payload);
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 rounded-2xl shadow-xl">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/30 text-blue-200 border border-blue-400/30">
              Phase 3 Module 2: Question Bank
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/30 text-emerald-200 border border-emerald-400/30">
              LaTeX & Programming Engine
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight">Institutional Question Bank & Item Authoring Studio</h1>
          <p className="text-sm text-blue-200/80">
            Author multi-language questions, LaTeX mathematical formulas, coding challenges with test cases, and audio/video comprehension items.
          </p>
        </div>

        <button
          onClick={handleOpenCreate}
          className="flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-xl shadow-lg transition"
        >
          <Plus className="w-4 h-4" /> Author New Question
        </button>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm flex flex-wrap items-center gap-4">
        <div className="flex-1 min-w-[220px] relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search questions by text or code..."
            className="w-full pl-9 pr-3 py-2 text-sm rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 font-medium"
          >
            <option value="ALL">All Question Types</option>
            <option value="MCQ">Multiple Choice (MCQ)</option>
            <option value="MSQ">Multiple Select (MSQ)</option>
            <option value="NUMERICAL">Numerical Answer</option>
            <option value="PROGRAMMING">Coding Challenge</option>
            <option value="AUDIO_COMPREHENSION">Audio Passage</option>
          </select>

          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
            className="text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 font-medium"
          >
            <option value="ALL">All Difficulties</option>
            <option value="EASY">EASY</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HARD">HARD</option>
            <option value="EXPERT">EXPERT</option>
          </select>

          <select
            value={languageFilter}
            onChange={(e) => setLanguageFilter(e.target.value)}
            className="text-xs px-3 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 font-medium"
          >
            <option value="ALL">All Languages</option>
            <option value="English">English</option>
            <option value="Hindi">Hindi (हिंदी)</option>
          </select>
        </div>
      </div>

      {/* Questions Table */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between">
          <h3 className="font-bold text-sm text-gray-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-blue-600" /> Catalogued Questions ({questions.length})
          </h3>
          <span className="text-xs text-gray-400">Reuses ERP media and subject taxonomy</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 dark:bg-gray-900/50 text-xs uppercase font-semibold text-gray-500 border-b border-gray-100 dark:border-gray-800">
              <tr>
                <th className="px-4 py-3">Code</th>
                <th className="px-4 py-3">Question Prompt</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Difficulty</th>
                <th className="px-4 py-3">Language</th>
                <th className="px-4 py-3">Marks</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
              {questions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-400 text-xs">
                    No questions found matching your filter criteria. Click "Author New Question" to add one!
                  </td>
                </tr>
              ) : (
                questions.map((q) => (
                  <tr key={q.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
                    <td className="px-4 py-3 font-mono text-xs font-semibold text-blue-600 dark:text-blue-400">
                      {q.question_code}
                    </td>
                    <td className="px-4 py-3 max-w-md">
                      <div className="font-medium text-gray-900 dark:text-white line-clamp-2">{q.question_text}</div>
                      {q.latex_equations_json && q.latex_equations_json.length > 0 && (
                        <div className="mt-1 flex items-center gap-1 font-mono text-2xs bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-2 py-0.5 rounded w-fit">
                          <Sigma className="w-3 h-3" /> LaTeX Formula Attached
                        </div>
                      )}
                      {q.programming_metadata_json && q.programming_metadata_json.language && (
                        <div className="mt-1 flex items-center gap-1 font-mono text-2xs bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 px-2 py-0.5 rounded w-fit">
                          <Code className="w-3 h-3" /> Code Problem: {q.programming_metadata_json.language}
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                        {q.question_type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                          q.difficulty_level === "EASY"
                            ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
                            : q.difficulty_level === "MEDIUM"
                            ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                            : q.difficulty_level === "HARD"
                            ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300"
                            : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                        }`}
                      >
                        {q.difficulty_level}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-xs text-gray-500">{q.language}</td>
                    <td className="px-4 py-3 text-xs font-semibold text-gray-800 dark:text-gray-200">
                      +{q.default_marks} / -{q.negative_marks}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => {
                          if (confirm(`Deactivate question ${q.question_code}?`)) {
                            deleteQuestionMutation.mutate(q.id);
                          }
                        }}
                        className="p-1 hover:text-red-600 text-gray-400"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* AUTHORING STUDIO MODAL */}
      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-gray-100 dark:border-gray-700 p-6 space-y-5">
            <div className="flex items-center justify-between border-b border-gray-100 dark:border-gray-700 pb-3">
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">Author New Examination Item</h3>
                <p className="text-xs text-gray-500">Supports LaTeX Math, Code Test Cases, and Multi-language Translation</p>
              </div>
              <button onClick={() => setShowModal(false)} className="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
                <X className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            <form onSubmit={handleSaveQuestion} className="space-y-4">
              {/* Type and Difficulty bar */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div>
                  <label className="text-xs font-semibold text-gray-500">Question Type</label>
                  <select
                    value={formType}
                    onChange={(e) => setFormType(e.target.value as any)}
                    className="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                  >
                    <option value="MCQ">Multiple Choice (MCQ)</option>
                    <option value="NUMERICAL">Numerical Integer/Float</option>
                    <option value="PROGRAMMING">Programming Challenge</option>
                    <option value="AUDIO_COMPREHENSION">Audio Passage</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-500">Difficulty Level</label>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(e.target.value as any)}
                    className="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                  >
                    <option value="EASY">EASY</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HARD">HARD</option>
                    <option value="EXPERT">EXPERT</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-500">Language</label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                  >
                    <option value="English">English</option>
                    <option value="Hindi">Hindi (हिंदी)</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-500">Marks (+ / -)</label>
                  <div className="flex items-center gap-1 mt-1">
                    <input
                      type="number"
                      step="0.5"
                      value={defaultMarks}
                      onChange={(e) => setDefaultMarks(parseFloat(e.target.value) || 1)}
                      className="w-1/2 px-2 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                    />
                    <input
                      type="number"
                      step="0.25"
                      value={negativeMarks}
                      onChange={(e) => setNegativeMarks(parseFloat(e.target.value) || 0)}
                      className="w-1/2 px-2 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                    />
                  </div>
                </div>
              </div>

              {/* Navigation Tabs inside modal */}
              <div className="flex border-b border-gray-200 dark:border-gray-700 space-x-4 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => setActiveTab("PROMPT")}
                  className={`pb-2 border-b-2 transition ${activeTab === "PROMPT" ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500"}`}
                >
                  Question Prompt
                </button>
                {formType === "MCQ" && (
                  <button
                    type="button"
                    onClick={() => setActiveTab("OPTIONS")}
                    className={`pb-2 border-b-2 transition ${activeTab === "OPTIONS" ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500"}`}
                  >
                    Options & Answer
                  </button>
                )}
                {formType === "PROGRAMMING" && (
                  <button
                    type="button"
                    onClick={() => setActiveTab("CODE")}
                    className={`pb-2 border-b-2 transition ${activeTab === "CODE" ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500"}`}
                  >
                    Starter Code & Tests
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => setActiveTab("LATEX")}
                  className={`pb-2 border-b-2 transition ${activeTab === "LATEX" ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500"}`}
                >
                  LaTeX Equations ({latexList.length})
                </button>
                <button
                  type="button"
                  onClick={() => setActiveTab("TAGS")}
                  className={`pb-2 border-b-2 transition ${activeTab === "TAGS" ? "border-blue-600 text-blue-600" : "border-transparent text-gray-500"}`}
                >
                  Tags & Taxonomy
                </button>
              </div>

              {/* Tab 1: PROMPT */}
              {activeTab === "PROMPT" && (
                <div className="space-y-3">
                  <div>
                    <label className="text-xs font-semibold text-gray-500">Question Statement</label>
                    <textarea
                      rows={4}
                      required
                      value={questionText}
                      onChange={(e) => setQuestionText(e.target.value)}
                      placeholder="Enter the full question text or problem description here..."
                      className="w-full mt-1 p-3 text-sm rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-semibold text-gray-500">Detailed Explanation / Solution</label>
                    <textarea
                      rows={2}
                      value={explanation}
                      onChange={(e) => setExplanation(e.target.value)}
                      placeholder="Optional step-by-step solution shown after exam submission"
                      className="w-full mt-1 p-2.5 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                    />
                  </div>
                </div>
              )}

              {/* Tab 2: OPTIONS (MCQ) */}
              {activeTab === "OPTIONS" && (
                <div className="space-y-3">
                  <span className="text-xs font-semibold text-gray-500">Multiple Choice Options (Select Correct Option)</span>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {options.map((opt, idx) => (
                      <div key={opt.key} className="flex items-center gap-2 p-2.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
                        <input
                          type="radio"
                          name="correct_opt"
                          checked={correctAnswer === opt.key}
                          onChange={() => setCorrectAnswer(opt.key)}
                          className="w-4 h-4 text-blue-600"
                        />
                        <span className="font-bold text-xs">{opt.key}.</span>
                        <input
                          type="text"
                          value={opt.text}
                          onChange={(e) => {
                            const newOpts = [...options];
                            newOpts[idx].text = e.target.value;
                            setOptions(newOpts);
                          }}
                          placeholder={`Option ${opt.key} text`}
                          className="flex-1 px-2.5 py-1 text-xs rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tab 3: CODE (PROGRAMMING) */}
              {activeTab === "CODE" && (
                <div className="space-y-3">
                  <div className="flex items-center gap-4">
                    <div className="w-1/3">
                      <label className="text-xs font-semibold text-gray-500">Language Runner</label>
                      <select
                        value={progLang}
                        onChange={(e) => setProgLang(e.target.value)}
                        className="w-full mt-1 px-2.5 py-1.5 text-xs rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                      >
                        <option value="Python 3">Python 3 (3.11)</option>
                        <option value="Java">Java (OpenJDK 17)</option>
                        <option value="C++">C++ (GCC 12)</option>
                        <option value="TypeScript">TypeScript (Node 20)</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-gray-500">Starter Code Template</label>
                    <textarea
                      rows={5}
                      value={starterCode}
                      onChange={(e) => setStarterCode(e.target.value)}
                      className="w-full mt-1 p-2.5 font-mono text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-900 text-emerald-400"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-semibold text-gray-500">Sample Test Input (stdin)</label>
                      <textarea
                        rows={2}
                        value={sampleInput}
                        onChange={(e) => setSampleInput(e.target.value)}
                        className="w-full mt-1 p-2 font-mono text-xs rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                      />
                    </div>
                    <div>
                      <label className="text-xs font-semibold text-gray-500">Expected Output (stdout)</label>
                      <textarea
                        rows={2}
                        value={sampleOutput}
                        onChange={(e) => setSampleOutput(e.target.value)}
                        className="w-full mt-1 p-2 font-mono text-xs rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Tab 4: LATEX EQUATIONS */}
              {activeTab === "LATEX" && (
                <div className="space-y-3">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={latexInput}
                      onChange={(e) => setLatexInput(e.target.value)}
                      placeholder="Enter raw LaTeX formula, e.g. \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"
                      className="flex-1 px-3 py-2 text-xs font-mono rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (latexInput.trim()) {
                          setLatexList([...latexList, latexInput.trim()]);
                          setLatexInput("");
                        }
                      }}
                      className="px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold rounded-xl"
                    >
                      Add Equation
                    </button>
                  </div>

                  {/* Equation List & Preview */}
                  <div className="space-y-2">
                    {latexList.map((eq, i) => (
                      <div key={i} className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-xl border border-purple-200 dark:border-purple-800 flex items-center justify-between">
                        <div>
                          <span className="text-2xs uppercase font-bold text-purple-600 block">LaTeX Equation #{i + 1}</span>
                          <code className="text-xs font-mono text-purple-900 dark:text-purple-200">{eq}</code>
                        </div>
                        <button
                          type="button"
                          onClick={() => setLatexList(latexList.filter((_, idx) => idx !== i))}
                          className="text-red-500 hover:text-red-700 text-xs p-1"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Tab 5: TAGS */}
              {activeTab === "TAGS" && (
                <div className="space-y-3">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={tagInput}
                      onChange={(e) => setTagInput(e.target.value.toUpperCase())}
                      placeholder="Add tag e.g. GATE_2026, ALGORITHMS"
                      className="flex-1 px-3 py-2 text-xs rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 font-mono"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        if (tagInput.trim() && !tags.includes(tagInput.trim())) {
                          setTags([...tags, tagInput.trim()]);
                          setTagInput("");
                        }
                      }}
                      className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-xl"
                    >
                      Attach Tag
                    </button>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {tags.map((t) => (
                      <span key={t} className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                        <Tag className="w-3 h-3" />
                        <span>{t}</span>
                        <button
                          type="button"
                          onClick={() => setTags(tags.filter((tag) => tag !== t))}
                          className="hover:text-red-500 ml-1"
                        >
                          &times;
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Submit Buttons */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-100 dark:border-gray-700">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createQuestionMutation.isPending}
                  className="flex items-center gap-1.5 px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-xl shadow-sm"
                >
                  <Save className="w-4 h-4" />
                  <span>{createQuestionMutation.isPending ? "Cataloging..." : "Save Question to Bank"}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
export default QuestionBankManagerPage;
