import React, { useState, useEffect, useRef, useMemo } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  Clock,
  ShieldCheck,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Maximize,
  Minimize,
  Calculator as CalcIcon,
  HelpCircle,
  FileText,
  AlertTriangle,
  RotateCcw,
  Bookmark,
  Languages,
  Type,
  CloudCheck,
  Wifi,
  WifiOff,
  User,
  ArrowRight,
  X,
  Check,
  ShieldAlert,
  Camera,
  Lock,
} from "lucide-react";

interface QuestionOption {
  id: string;
  label: string;
  content: string;
  hi_content?: string;
}

interface ExamQuestion {
  id: string;
  number: number;
  section: string;
  type: "MCQ" | "NUMERICAL" | "MULTI_SELECT";
  content: string;
  hi_content?: string;
  options: QuestionOption[];
  marks: number;
  negativeMarks: number;
}

type QuestionStatus =
  | "NOT_VISITED"
  | "NOT_ANSWERED"
  | "ANSWERED"
  | "MARKED_FOR_REVIEW"
  | "ANSWERED_AND_MARKED_FOR_REVIEW";

interface CandidateAnswerRecord {
  selectedOptions: string[];
  textAnswer: string;
  isMarkedForReview: boolean;
  status: QuestionStatus;
  timeSpentSeconds: number;
}

export const CandidateExamInterfacePage: React.FC = () => {
  const navigate = useNavigate();
  const { sessionId } = useParams<{ sessionId?: string }>();

  // Exam Global State
  const [activeLang, setActiveLang] = useState<"en" | "hi">("en");
  const [fontSize, setFontSize] = useState<"sm" | "md" | "lg">("md");
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [isCalculatorOpen, setIsCalculatorOpen] = useState<boolean>(false);
  const [isSubmitModalOpen, setIsSubmitModalOpen] = useState<boolean>(false);
  const [isInstructionsOpen, setIsInstructionsOpen] = useState<boolean>(false);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
  const [finalScore, setFinalScore] = useState<number | null>(null);

  // Security & Proctoring State (Phase 3 Module 8)
  const [warningsCount, setWarningsCount] = useState<number>(0);
  const [isSecurityWarningOpen, setIsSecurityWarningOpen] = useState<boolean>(false);
  const [securityModalTitle, setSecurityModalTitle] = useState<string>("");
  const [securityModalDesc, setSecurityModalDesc] = useState<string>("");
  const [isDisqualified, setIsDisqualified] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Connection & Sync
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [syncStatus, setSyncStatus] = useState<"SAVED" | "SAVING" | "RECONNECTED">("SAVED");
  const [lastSyncTime, setLastSyncTime] = useState<string>("Just now");

  // Timer State (3 Hours = 10800s, default set to 10740s)
  const [secondsRemaining, setSecondsRemaining] = useState<number>(10740);

  // Sections & Navigation
  const [currentIdx, setCurrentIdx] = useState<number>(0);
  const [currentSection, setCurrentSection] = useState<string>("Section A: General Aptitude");

  // Questions Database
  const questions: ExamQuestion[] = useMemo(
    () => [
      {
        id: "q-1",
        number: 1,
        section: "Section A: General Aptitude",
        type: "MCQ",
        content:
          "A train passes a standing pole in 15 seconds while traveling at a uniform velocity of 60 km/h. What is the length of the train in meters?",
        hi_content:
          "एक रेलगाड़ी 60 किमी/घंटा की एकसमान गति से यात्रा करते हुए एक खड़े खंभे को 15 सेकंड में पार करती है। रेलगाड़ी की लंबाई मीटर में क्या है?",
        options: [
          { id: "A", label: "A", content: "250 meters", hi_content: "250 मीटर" },
          { id: "B", label: "B", content: "150 meters", hi_content: "150 मीटर" },
          { id: "C", label: "C", content: "200 meters", hi_content: "200 मीटर" },
          { id: "D", label: "D", content: "300 meters", hi_content: "300 मीटर" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-2",
        number: 2,
        section: "Section A: General Aptitude",
        type: "MCQ",
        content:
          "Find the missing term in the sequence: 3, 7, 15, 31, 63, [ ? ]",
        hi_content:
          "दी गई श्रृंखला में लुप्त पद ज्ञात कीजिए: 3, 7, 15, 31, 63, [ ? ]",
        options: [
          { id: "A", label: "A", content: "95", hi_content: "95" },
          { id: "B", label: "B", content: "127", hi_content: "127" },
          { id: "C", label: "C", content: "115", hi_content: "115" },
          { id: "D", label: "D", content: "128", hi_content: "128" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-3",
        number: 3,
        section: "Section A: General Aptitude",
        type: "MCQ",
        content:
          "If in a certain code language, 'ROSE' is written as 'TQUG', how will 'BISCUIT' be coded in that same schema?",
        hi_content:
          "यदि किसी सांकेतिक भाषा में 'ROSE' को 'TQUG' लिखा जाता है, तो उसी नियम के अनुसार 'BISCUIT' को क्या लिखा जाएगा?",
        options: [
          { id: "A", label: "A", content: "DKUEWKV", hi_content: "DKUEWKV" },
          { id: "B", label: "B", content: "DKUEXKW", hi_content: "DKUEXKW" },
          { id: "C", label: "C", content: "CJTDVJU", hi_content: "CJTDVJU" },
          { id: "D", label: "D", content: "DKTEWKV", hi_content: "DKTEWKV" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-4",
        number: 4,
        section: "Section B: Computer Science",
        type: "MCQ",
        content:
          "In an ACID-compliant Relational Database Management System (RDBMS), which specific property guarantees that concurrent execution of transactions produces a system state equivalent to serial execution?",
        hi_content:
          "ACID आज्ञाकारी संबंधपरक डेटाबेस प्रबंधन प्रणाली (RDBMS) में, कौन सा विशिष्ट गुण यह सुनिश्चित करता है कि समवर्ती लेन-देन निष्पादन क्रमिक निष्पादन के समकक्ष परिणाम देता है?",
        options: [
          { id: "A", label: "A", content: "Atomicity", hi_content: "परमाणुकता (Atomicity)" },
          { id: "B", label: "B", content: "Consistency", hi_content: "संगति (Consistency)" },
          { id: "C", label: "C", content: "Isolation", hi_content: "अलगाव (Isolation)" },
          { id: "D", label: "D", content: "Durability", hi_content: "स्थायित्व (Durability)" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-5",
        number: 5,
        section: "Section B: Computer Science",
        type: "MCQ",
        content:
          "What is the worst-case time complexity of searching for an element in an AVL self-balancing binary search tree containing n keys?",
        hi_content:
          "n कुंजियों वाले AVL स्व-संतुलित बाइनरी सर्च ट्री में किसी तत्व को खोजने की सबसे खराब समय जटिलता क्या है?",
        options: [
          { id: "A", label: "A", content: "O(1)", hi_content: "O(1)" },
          { id: "B", label: "B", content: "O(log n)", hi_content: "O(log n)" },
          { id: "C", label: "C", content: "O(n)", hi_content: "O(n)" },
          { id: "D", label: "D", content: "O(n log n)", hi_content: "O(n log n)" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-6",
        number: 6,
        section: "Section B: Computer Science",
        type: "MCQ",
        content:
          "Which CPU scheduling algorithm gives minimum average waiting time for a given set of non-preemptive processes?",
        hi_content:
          "गैर-प्रीएम्प्टिव प्रक्रियाओं के दिए गए सेट के लिए कौन सा सीपीयू शेड्यूलिंग एल्गोरिदम न्यूनतम औसत प्रतीक्षा समय प्रदान करता है?",
        options: [
          { id: "A", label: "A", content: "First-Come First-Served (FCFS)", hi_content: "पहले आओ पहले पाओ (FCFS)" },
          { id: "B", label: "B", content: "Shortest Job First (SJF)", hi_content: "शॉर्टेस्ट जॉब फर्स्ट (SJF)" },
          { id: "C", label: "C", content: "Round Robin with large quantum", hi_content: "राउंड रॉबिन (Round Robin)" },
          { id: "D", label: "D", content: "Priority Scheduling", hi_content: "प्राथमिकता शेड्यूलिंग (Priority Scheduling)" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-7",
        number: 7,
        section: "Section C: Mathematics",
        type: "MCQ",
        content:
          "Evaluate the determinant of the 2x2 matrix M = [[4, 3], [2, 5]].",
        hi_content:
          "2x2 आव्यूह M = [[4, 3], [2, 5]] के सारणिक (Determinant) का मान ज्ञात कीजिए।",
        options: [
          { id: "A", label: "A", content: "14", hi_content: "14" },
          { id: "B", label: "B", content: "26", hi_content: "26" },
          { id: "C", label: "C", content: "10", hi_content: "10" },
          { id: "D", label: "D", content: "20", hi_content: "20" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
      {
        id: "q-8",
        number: 8,
        section: "Section C: Mathematics",
        type: "MCQ",
        content:
          "If eigenvalues of a 2x2 matrix are 3 and 7, what is the trace and determinant of that matrix?",
        hi_content:
          "यदि किसी 2x2 आव्यूह के आइगेनवैल्यू 3 और 7 हैं, तो उस आव्यूह का ट्रेस और सारणिक क्या होगा?",
        options: [
          { id: "A", label: "A", content: "Trace = 10, Det = 21", hi_content: "ट्रेस = 10, सारणिक = 21" },
          { id: "B", label: "B", content: "Trace = 21, Det = 10", hi_content: "ट्रेस = 21, सारणिक = 10" },
          { id: "C", label: "C", content: "Trace = 4, Det = 10", hi_content: "ट्रेस = 4, सारणिक = 10" },
          { id: "D", label: "D", content: "Trace = 10, Det = 4", hi_content: "ट्रेस = 10, सारणिक = 4" },
        ],
        marks: 2.0,
        negativeMarks: 0.5,
      },
    ],
    []
  );

  // In-Memory Answer Ledger (Strict Zero Client-Side Storage)
  const [answers, setAnswers] = useState<Record<string, CandidateAnswerRecord>>(() => {
    const init: Record<string, CandidateAnswerRecord> = {};
    questions.forEach((q, idx) => {
      init[q.id] = {
        selectedOptions: [],
        textAnswer: "",
        isMarkedForReview: false,
        status: idx === 0 ? "NOT_ANSWERED" : "NOT_VISITED",
        timeSpentSeconds: 0,
      };
    });
    return init;
  });

  const activeQuestion = questions[currentIdx];
  const activeAnswer = answers[activeQuestion.id] || {
    selectedOptions: [],
    textAnswer: "",
    isMarkedForReview: false,
    status: "NOT_VISITED",
    timeSpentSeconds: 0,
  };

  // Synchronize section tab on question index change
  useEffect(() => {
    if (activeQuestion) {
      setCurrentSection(activeQuestion.section);
      setAnswers((prev) => {
        const cur = prev[activeQuestion.id];
        if (cur && cur.status === "NOT_VISITED") {
          return {
            ...prev,
            [activeQuestion.id]: {
              ...cur,
              status: "NOT_ANSWERED",
            },
          };
        }
        return prev;
      });
    }
  }, [currentIdx, activeQuestion]);

  // Toast Notification Helper
  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  // Security Violation Handler
  const handleSecurityStrike = (type: string, desc: string) => {
    if (isSubmitted || isDisqualified) return;

    setWarningsCount((prev) => {
      const nextCount = prev + 1;
      if (nextCount >= 3) {
        setIsDisqualified(true);
        setIsSecurityWarningOpen(false);
      } else {
        setSecurityModalTitle("Security Violation Detected: " + type);
        setSecurityModalDesc(
          desc + " (Strike " + nextCount + "/3). Accumulating 3 strikes terminates this test immediately."
        );
        setIsSecurityWarningOpen(true);
      }
      return nextCount;
    });
  };

  // Security Event Listeners (Tab Switch, Fullscreen, Clipboard, ContextMenu, Keydown)
  useEffect(() => {
    if (isSubmitted || isDisqualified) return;

    // 1. Tab switch / Window blur
    const handleVisibilityChange = () => {
      if (document.hidden) {
        handleSecurityStrike(
          "Tab Switch / Window Blur",
          "Navigating away from the active examination window is strictly prohibited."
        );
      }
    };

    // 2. Fullscreen change
    const handleFullscreenChange = () => {
      const inFullscreen = !!document.fullscreenElement;
      setIsFullscreen(inFullscreen);
      if (!inFullscreen) {
        handleSecurityStrike(
          "Fullscreen Exit",
          "Exiting fullscreen lockdown mode violates national testing regulations."
        );
      }
    };

    // 3. Clipboard restrictions
    const handleCopy = (e: ClipboardEvent) => {
      e.preventDefault();
      showToast("Clipboard operations (Copy) are disabled during examination.");
    };
    const handleCut = (e: ClipboardEvent) => {
      e.preventDefault();
      showToast("Clipboard operations (Cut) are disabled during examination.");
    };
    const handlePaste = (e: ClipboardEvent) => {
      e.preventDefault();
      showToast("Clipboard operations (Paste) are disabled during examination.");
    };

    // 4. Right-click context menu disable
    const handleContextMenu = (e: MouseEvent) => {
      e.preventDefault();
      showToast("Right-click context menu is restricted.");
    };

    // 5. DevTools and navigation shortcuts
    const handleKeyDown = (e: KeyboardEvent) => {
      if (
        e.key === "F12" ||
        (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "i" || e.key === "C" || e.key === "c")) ||
        (e.ctrlKey && (e.key === "U" || e.key === "u"))
      ) {
        e.preventDefault();
        handleSecurityStrike(
          "Developer Tools Shortcut",
          "Inspection tools, console devtools, and view-source shortcuts are prohibited."
        );
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    document.addEventListener("copy", handleCopy);
    document.addEventListener("cut", handleCut);
    document.addEventListener("paste", handlePaste);
    document.addEventListener("contextmenu", handleContextMenu);
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
      document.removeEventListener("copy", handleCopy);
      document.removeEventListener("cut", handleCut);
      document.removeEventListener("paste", handlePaste);
      document.removeEventListener("contextmenu", handleContextMenu);
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [isSubmitted, isDisqualified]);

  // Server Countdown Timer & 3s Autosave Heartbeat
  useEffect(() => {
    if (isSubmitted || isDisqualified) return;

    const timer = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleAutoSubmitOnExpiry();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isSubmitted, isDisqualified]);

  // Periodic 3-second heartbeat to simulate backend synchronization
  useEffect(() => {
    if (isSubmitted || isDisqualified) return;

    const heartbeat = setInterval(() => {
      setSyncStatus("SAVING");
      setTimeout(() => {
        setSyncStatus("SAVED");
        const now = new Date();
        setLastSyncTime(
          now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })
        );
      }, 350);
    }, 3000);

    return () => clearInterval(heartbeat);
  }, [isSubmitted, isDisqualified]);

  // Fullscreen management
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {});
    } else {
      document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {});
    }
  };

  const reenterFullscreen = () => {
    document.documentElement.requestFullscreen().then(() => {
      setIsFullscreen(true);
      setIsSecurityWarningOpen(false);
    }).catch(() => {
      setIsSecurityWarningOpen(false);
    });
  };

  // Timer format (HH:MM:SS)
  const formatTimer = (totalSeconds: number) => {
    const hrs = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;
    return `${hrs.toString().padStart(2, "0")}:${mins.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  // Option Selection
  const handleSelectOption = (optionId: string) => {
    setAnswers((prev) => {
      const cur = prev[activeQuestion.id];
      const isSelected = cur.selectedOptions.includes(optionId);
      const updatedOpts = isSelected ? [] : [optionId];
      return {
        ...prev,
        [activeQuestion.id]: {
          ...cur,
          selectedOptions: updatedOpts,
        },
      };
    });
  };

  // Actions: Save & Next
  const handleSaveAndNext = () => {
    setAnswers((prev) => {
      const cur = prev[activeQuestion.id];
      const hasAnswer = cur.selectedOptions.length > 0;
      let newStatus: QuestionStatus = "NOT_ANSWERED";

      if (hasAnswer && cur.isMarkedForReview) {
        newStatus = "ANSWERED_AND_MARKED_FOR_REVIEW";
      } else if (hasAnswer) {
        newStatus = "ANSWERED";
      } else if (cur.isMarkedForReview) {
        newStatus = "MARKED_FOR_REVIEW";
      }

      return {
        ...prev,
        [activeQuestion.id]: {
          ...cur,
          status: newStatus,
        },
      };
    });

    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    }
  };

  // Actions: Save & Mark for Review
  const handleSaveAndMarkForReview = () => {
    setAnswers((prev) => {
      const cur = prev[activeQuestion.id];
      const hasAnswer = cur.selectedOptions.length > 0;
      const newStatus: QuestionStatus = hasAnswer
        ? "ANSWERED_AND_MARKED_FOR_REVIEW"
        : "MARKED_FOR_REVIEW";

      return {
        ...prev,
        [activeQuestion.id]: {
          ...cur,
          isMarkedForReview: true,
          status: newStatus,
        },
      };
    });

    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    }
  };

  // Actions: Clear Response
  const handleClearResponse = () => {
    setAnswers((prev) => ({
      ...prev,
      [activeQuestion.id]: {
        ...prev[activeQuestion.id],
        selectedOptions: [],
        textAnswer: "",
        status: "NOT_ANSWERED",
      },
    }));
  };

  // Actions: Mark for Review & Next (without answer)
  const handleMarkForReviewAndNext = () => {
    setAnswers((prev) => {
      const cur = prev[activeQuestion.id];
      const hasAnswer = cur.selectedOptions.length > 0;
      const newStatus: QuestionStatus = hasAnswer
        ? "ANSWERED_AND_MARKED_FOR_REVIEW"
        : "MARKED_FOR_REVIEW";

      return {
        ...prev,
        [activeQuestion.id]: {
          ...cur,
          isMarkedForReview: true,
          status: newStatus,
        },
      };
    });

    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    }
  };

  const handleJumpToQuestion = (targetIdx: number) => {
    setCurrentIdx(targetIdx);
  };

  const handleAutoSubmitOnExpiry = () => {
    computeScoreAndFinish();
  };

  const handleFinalSubmit = () => {
    setIsSubmitModalOpen(false);
    computeScoreAndFinish();
  };

  const computeScoreAndFinish = () => {
    let score = 0;
    questions.forEach((q) => {
      const ans = answers[q.id];
      if (ans && ans.selectedOptions.length > 0) {
        score += q.marks;
      }
    });

    setFinalScore(score);
    setIsSubmitted(true);
  };

  // Statistics Summary
  const stats = useMemo(() => {
    let answered = 0;
    let notAnswered = 0;
    let notVisited = 0;
    let markedForReview = 0;
    let answeredAndMarked = 0;

    Object.values(answers).forEach((a) => {
      if (a.status === "ANSWERED") answered++;
      else if (a.status === "NOT_ANSWERED") notAnswered++;
      else if (a.status === "NOT_VISITED") notVisited++;
      else if (a.status === "MARKED_FOR_REVIEW") markedForReview++;
      else if (a.status === "ANSWERED_AND_MARKED_FOR_REVIEW") answeredAndMarked++;
    });

    return {
      total: questions.length,
      answered,
      notAnswered,
      notVisited,
      markedForReview,
      answeredAndMarked,
    };
  }, [answers, questions.length]);

  const sections = useMemo(() => {
    return Array.from(new Set(questions.map((q) => q.section)));
  }, [questions]);

  // Calculator State
  const [calcInput, setCalcInput] = useState<string>("");
  const [calcResult, setCalcResult] = useState<string>("");

  const handleCalcClick = (val: string) => {
    if (val === "C") {
      setCalcInput("");
      setCalcResult("");
    } else if (val === "DEL") {
      setCalcInput((prev) => prev.slice(0, -1));
    } else if (val === "=") {
      try {
        const sanitized = calcInput
          .replace(/sin/g, "Math.sin")
          .replace(/cos/g, "Math.cos")
          .replace(/tan/g, "Math.tan")
          .replace(/sqrt/g, "Math.sqrt")
          .replace(/pi/g, "Math.PI")
          .replace(/\^/g, "**");
        // eslint-disable-next-line no-eval
        const res = Function(`"use strict"; return (${sanitized})`)();
        setCalcResult(String(Number(res).toFixed(4)));
      } catch (e) {
        setCalcResult("Error");
      }
    } else {
      setCalcInput((prev) => prev + val);
    }
  };

  // 1. DISQUALIFICATION SCREEN (3 STRIKES EXCEEDED)
  if (isDisqualified) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
        <div className="max-w-lg w-full bg-slate-900 border-2 border-rose-600 rounded-2xl p-8 text-center text-white shadow-2xl">
          <div className="h-20 w-20 bg-rose-600/20 text-rose-500 rounded-full flex items-center justify-center mx-auto mb-6 ring-8 ring-rose-600/10 animate-bounce">
            <Lock className="h-10 w-10" />
          </div>
          <h1 className="text-2xl font-bold text-rose-400 mb-2">Examination Terminated — Workstation Locked</h1>
          <p className="text-sm text-slate-300 mb-6 leading-relaxed">
            You have accumulated <strong>3 security strikes</strong> for unauthorized browser navigation, tab switching, or clipboard violations. This workstation has been locked and your exam is terminated.
          </p>

          <div className="bg-slate-950 p-4 rounded-xl border border-rose-900/60 mb-6 text-left text-xs font-mono space-y-1.5 text-slate-400">
            <div>Candidate: Aarav Sharma (MEI-2026-84920)</div>
            <div>Terminal ID: LAB1-WS-42 (IP: 192.168.10.42)</div>
            <div>Reason: AUTO_DISQUALIFIED (3/3 Strikes Reached)</div>
            <div>Timestamp: {new Date().toLocaleTimeString()} IST</div>
          </div>

          <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-xs text-amber-300 mb-6">
            Please remain seated and immediately notify the Lab Center Supervisor for formal incident clearance.
          </div>

          <Link
            to="/admin/cbt"
            className="inline-block w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // 2. EXAM SUBMISSION SCREEN
  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="max-w-xl w-full bg-slate-800 border border-slate-700 rounded-2xl p-8 text-center text-white shadow-2xl">
          <div className="h-20 w-20 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-6 ring-8 ring-emerald-500/10">
            <CheckCircle2 className="h-10 w-10" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Examination Submitted Successfully</h1>
          <p className="text-sm text-slate-300 mb-6">
            Your computer-based test responses have been securely frozen, encrypted, and recorded in
            the National Examination Ledger.
          </p>

          <div className="grid grid-cols-3 gap-3 bg-slate-900/80 p-4 rounded-xl border border-slate-700/60 mb-6">
            <div className="text-center">
              <span className="text-xs text-slate-400">Total Questions</span>
              <p className="text-xl font-bold text-white mt-1">{stats.total}</p>
            </div>
            <div className="text-center border-x border-slate-700">
              <span className="text-xs text-slate-400">Answered</span>
              <p className="text-xl font-bold text-emerald-400 mt-1">
                {stats.answered + stats.answeredAndMarked}
              </p>
            </div>
            <div className="text-center">
              <span className="text-xs text-slate-400">Preliminary Score</span>
              <p className="text-xl font-bold text-cyan-400 mt-1">{finalScore} / 16.00</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              to="/admin/cbt"
              className="flex-1 px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-sm transition"
            >
              Return to CBT Control Hub
            </Link>
            <Link
              to="/admin/cbt/reports"
              className="flex-1 px-4 py-2.5 rounded-xl bg-slate-700 hover:bg-slate-600 text-white font-semibold text-sm transition"
            >
              View Detailed Scorecard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`min-h-screen flex flex-col bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100 select-none ${
        fontSize === "sm" ? "text-sm" : fontSize === "lg" ? "text-lg" : "text-base"
      }`}
    >
      {/* Toast Alert for Blocked Operations */}
      {toastMessage && (
        <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 bg-rose-600 text-white text-xs font-semibold px-4 py-2 rounded-xl shadow-xl flex items-center gap-2 animate-fade-in">
          <AlertTriangle className="h-4 w-4" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* 1. National Exam System Header */}
      <header className="bg-slate-900 border-b border-slate-800 text-white px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-md">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg bg-cyan-600/30 border border-cyan-500/50 flex items-center justify-center text-cyan-400 font-bold text-lg">
            MEI
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-tight text-white flex items-center gap-2">
              MEI-CBT National Entrance Examination 2026
              <span className="rounded bg-emerald-500/20 text-emerald-400 px-1.5 py-0.5 text-xs font-mono">
                LIVE
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Shift 1 • Center: TC-IND-01 (Flagship Indore Campus) • Lab 01 Terminal #42
            </p>
          </div>
        </div>

        {/* Candidate Information & Live Server Countdown Timer */}
        <div className="flex items-center gap-4">
          {/* Strikes Counter */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-xs">
            <ShieldAlert className={`h-3.5 w-3.5 ${warningsCount > 0 ? "text-amber-400" : "text-emerald-400"}`} />
            <span className="text-slate-300 font-mono text-[11px]">
              Strikes: <strong className={warningsCount > 0 ? "text-amber-400" : "text-emerald-400"}>{warningsCount}/3</strong>
            </span>
          </div>

          {/* AI Face & Webcam Badge */}
          <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-xs text-slate-300">
            <Camera className="h-3.5 w-3.5 text-cyan-400" />
            <span className="text-[11px] font-mono">Webcam AI: Verified</span>
          </div>

          {/* Heartbeat Sync Badge */}
          <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-xs">
            {syncStatus === "SAVING" ? (
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
              </span>
            ) : (
              <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
            )}
            <span className="text-slate-300 font-mono text-[11px]">
              {syncStatus === "SAVING" ? "Syncing..." : `Auto-saved ${lastSyncTime}`}
            </span>
          </div>

          {/* Time Remaining Clock */}
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border font-mono font-bold text-sm tracking-wider shadow-inner ${
              secondsRemaining < 300
                ? "bg-rose-500/20 border-rose-500 text-rose-300 animate-pulse"
                : secondsRemaining < 900
                ? "bg-amber-500/20 border-amber-500 text-amber-300"
                : "bg-cyan-950/70 border-cyan-600 text-cyan-300"
            }`}
          >
            <Clock className="h-4 w-4" />
            <span>Time Left: {formatTimer(secondsRemaining)}</span>
          </div>

          {/* Utility Tools */}
          <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-lg border border-slate-700">
            <button
              onClick={() => setActiveLang((l) => (l === "en" ? "hi" : "en"))}
              className="px-2 py-1 rounded text-xs font-semibold hover:bg-slate-700 text-slate-200 flex items-center gap-1 transition"
              title="Toggle Language"
            >
              <Languages className="h-3.5 w-3.5 text-cyan-400" />
              {activeLang === "en" ? "EN" : "हिन्दी"}
            </button>

            <div className="flex items-center border-l border-slate-700 pl-1 text-xs text-slate-300">
              <button
                onClick={() => setFontSize("sm")}
                className={`px-1.5 py-0.5 rounded ${fontSize === "sm" ? "bg-cyan-600 text-white font-bold" : "hover:bg-slate-700"}`}
              >
                A-
              </button>
              <button
                onClick={() => setFontSize("md")}
                className={`px-1.5 py-0.5 rounded ${fontSize === "md" ? "bg-cyan-600 text-white font-bold" : "hover:bg-slate-700"}`}
              >
                A
              </button>
              <button
                onClick={() => setFontSize("lg")}
                className={`px-1.5 py-0.5 rounded ${fontSize === "lg" ? "bg-cyan-600 text-white font-bold" : "hover:bg-slate-700"}`}
              >
                A+
              </button>
            </div>

            <button
              onClick={() => setIsCalculatorOpen(true)}
              className="p-1.5 rounded hover:bg-slate-700 text-slate-300 transition"
              title="Scientific Calculator"
            >
              <CalcIcon className="h-4 w-4 text-cyan-400" />
            </button>

            <button
              onClick={toggleFullscreen}
              className="p-1.5 rounded hover:bg-slate-700 text-slate-300 transition"
              title="Fullscreen Mode"
            >
              {isFullscreen ? <Minimize className="h-4 w-4" /> : <Maximize className="h-4 w-4" />}
            </button>
          </div>

          {/* Candidate Profile Avatar */}
          <div className="hidden lg:flex items-center gap-2 border-l border-slate-800 pl-3">
            <div className="h-8 w-8 rounded-full bg-cyan-700 border border-cyan-400 flex items-center justify-center text-xs font-bold text-white">
              AS
            </div>
            <div className="text-left text-xs leading-tight">
              <div className="font-semibold text-white">Aarav Sharma</div>
              <div className="text-slate-400 font-mono text-[10px]">Roll: MEI-2026-84920</div>
            </div>
          </div>
        </div>
      </header>

      {/* 2. Section Selector Banner */}
      <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 py-2 flex items-center justify-between gap-2 overflow-x-auto shadow-xs">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Sections:</span>
          {sections.map((sec) => (
            <button
              key={sec}
              onClick={() => {
                const target = questions.findIndex((q) => q.section === sec);
                if (target !== -1) setCurrentIdx(target);
              }}
              className={`px-3 py-1 rounded-md text-xs font-medium transition ${
                currentSection === sec
                  ? "bg-cyan-600 text-white shadow-xs font-semibold"
                  : "bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
              }`}
            >
              {sec}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 text-xs">
          <button
            onClick={() => setIsInstructionsOpen(true)}
            className="flex items-center gap-1 text-cyan-600 dark:text-cyan-400 hover:underline font-medium"
          >
            <HelpCircle className="h-3.5 w-3.5" /> Instructions
          </button>
        </div>
      </div>

      {/* 3. Main Examination Delivery Stage */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        {/* Left Question Area */}
        <main className="flex-1 flex flex-col justify-between bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 p-6 overflow-y-auto">
          <div>
            {/* Question Header Meta */}
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <span className="text-base font-bold text-slate-900 dark:text-white">
                  Question No. {activeQuestion.number}
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                  {activeQuestion.type}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs font-medium">
                <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                  +{activeQuestion.marks.toFixed(2)} Marks
                </span>
                <span className="text-rose-500 font-semibold">
                  -{activeQuestion.negativeMarks.toFixed(2)} Negative
                </span>
              </div>
            </div>

            {/* Question Text */}
            <div className="prose dark:prose-invert max-w-none mb-6">
              <p className="text-slate-800 dark:text-slate-200 font-medium leading-relaxed">
                {activeLang === "hi" && activeQuestion.hi_content
                  ? activeQuestion.hi_content
                  : activeQuestion.content}
              </p>
            </div>

            {/* Options List */}
            <div className="space-y-3">
              {activeQuestion.options.map((opt) => {
                const isSelected = activeAnswer.selectedOptions.includes(opt.id);
                return (
                  <button
                    key={opt.id}
                    onClick={() => handleSelectOption(opt.id)}
                    className={`w-full text-left p-4 rounded-xl border flex items-center gap-3.5 transition ${
                      isSelected
                        ? "border-cyan-600 bg-cyan-50/70 dark:bg-cyan-950/40 text-cyan-950 dark:text-cyan-100 ring-2 ring-cyan-500/20"
                        : "border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50/50 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300"
                    }`}
                  >
                    <div
                      className={`h-7 w-7 rounded-full flex items-center justify-center font-bold text-xs border transition ${
                        isSelected
                          ? "bg-cyan-600 text-white border-cyan-600"
                          : "border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-600 dark:text-slate-300"
                      }`}
                    >
                      {opt.label}
                    </div>
                    <span className="flex-1 text-sm font-medium">
                      {activeLang === "hi" && opt.hi_content ? opt.hi_content : opt.content}
                    </span>
                    {isSelected && <Check className="h-4 w-4 text-cyan-600 dark:text-cyan-400" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Bottom Action Control Bar */}
          <div className="mt-8 pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={handleSaveAndNext}
                className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs tracking-wide shadow-xs transition flex items-center gap-1.5"
              >
                <Check className="h-3.5 w-3.5" /> Save & Next
              </button>

              <button
                onClick={handleSaveAndMarkForReview}
                className="px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs tracking-wide shadow-xs transition flex items-center gap-1.5"
              >
                <Bookmark className="h-3.5 w-3.5" /> Save & Mark for Review
              </button>

              <button
                onClick={handleClearResponse}
                className="px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold transition"
              >
                Clear Response
              </button>

              <button
                onClick={handleMarkForReviewAndNext}
                className="px-3 py-2 rounded-lg border border-indigo-500/50 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 text-xs font-semibold transition"
              >
                Mark for Review & Next
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button
                disabled={currentIdx === 0}
                onClick={() => setCurrentIdx((i) => Math.max(0, i - 1))}
                className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold disabled:opacity-40 transition flex items-center gap-1"
              >
                <ChevronLeft className="h-4 w-4" /> Previous
              </button>
              <button
                disabled={currentIdx === questions.length - 1}
                onClick={() => setCurrentIdx((i) => Math.min(questions.length - 1, i + 1))}
                className="px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold disabled:opacity-40 transition flex items-center gap-1"
              >
                Next <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </main>

        {/* Right Sidebar: National Testing Question Palette */}
        <aside className="w-full lg:w-80 bg-slate-50 dark:bg-slate-900/80 border-t lg:border-t-0 lg:border-l border-slate-200 dark:border-slate-800 p-4 flex flex-col justify-between overflow-y-auto">
          <div>
            {/* Status Legend */}
            <div className="mb-4">
              <h2 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-2">
                Question Palette Legend
              </h2>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="flex items-center gap-2">
                  <span className="h-5 w-5 rounded bg-emerald-600 text-white font-bold flex items-center justify-center text-[10px]">
                    {stats.answered}
                  </span>
                  <span className="text-slate-600 dark:text-slate-400">Answered</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-5 w-5 rounded bg-rose-600 text-white font-bold flex items-center justify-center text-[10px]">
                    {stats.notAnswered}
                  </span>
                  <span className="text-slate-600 dark:text-slate-400">Not Answered</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-5 w-5 rounded bg-slate-300 dark:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold flex items-center justify-center text-[10px]">
                    {stats.notVisited}
                  </span>
                  <span className="text-slate-600 dark:text-slate-400">Not Visited</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="h-5 w-5 rounded bg-purple-600 text-white font-bold flex items-center justify-center text-[10px]">
                    {stats.markedForReview}
                  </span>
                  <span className="text-slate-600 dark:text-slate-400">Marked for Review</span>
                </div>
                <div className="col-span-2 flex items-center gap-2">
                  <span className="relative h-5 w-5 rounded bg-purple-600 text-white font-bold flex items-center justify-center text-[10px]">
                    {stats.answeredAndMarked}
                    <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-emerald-400 ring-1 ring-white"></span>
                  </span>
                  <span className="text-slate-600 dark:text-slate-400 text-[10px]">
                    Answered & Marked for Review
                  </span>
                </div>
              </div>
            </div>

            {/* Current Section Filter & Grid of Questions */}
            <div className="border-t border-slate-200 dark:border-slate-800 pt-3 mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                  {currentSection}
                </span>
                <span className="text-[11px] text-slate-500 font-mono">
                  {questions.filter((q) => q.section === currentSection).length} Questions
                </span>
              </div>

              <div className="grid grid-cols-4 sm:grid-cols-5 gap-2 max-h-64 overflow-y-auto p-1">
                {questions.map((q, idx) => {
                  const ans = answers[q.id];
                  const st = ans ? ans.status : "NOT_VISITED";
                  const isCurrent = idx === currentIdx;

                  let colorClass =
                    "bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-300";
                  if (st === "ANSWERED") {
                    colorClass = "bg-emerald-600 text-white hover:bg-emerald-500";
                  } else if (st === "NOT_ANSWERED") {
                    colorClass = "bg-rose-600 text-white hover:bg-rose-500";
                  } else if (st === "MARKED_FOR_REVIEW") {
                    colorClass = "bg-purple-600 text-white hover:bg-purple-500";
                  } else if (st === "ANSWERED_AND_MARKED_FOR_REVIEW") {
                    colorClass = "bg-purple-600 text-white hover:bg-purple-500 ring-2 ring-emerald-400";
                  }

                  return (
                    <button
                      key={q.id}
                      onClick={() => handleJumpToQuestion(idx)}
                      className={`h-9 w-9 rounded-lg font-bold text-xs flex items-center justify-center transition relative ${colorClass} ${
                        isCurrent ? "ring-2 ring-cyan-500 ring-offset-2 dark:ring-offset-slate-900" : ""
                      }`}
                    >
                      {q.number}
                      {st === "ANSWERED_AND_MARKED_FOR_REVIEW" && (
                        <span className="absolute -top-1 -right-1 h-2.5 w-2.5 rounded-full bg-emerald-400 border border-white"></span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Submit Test Button */}
          <div className="border-t border-slate-200 dark:border-slate-800 pt-4">
            <button
              onClick={() => setIsSubmitModalOpen(true)}
              className="w-full py-2.5 px-4 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-sm tracking-wide shadow-md transition flex items-center justify-center gap-2"
            >
              Submit Examination <ArrowRight className="h-4 w-4" />
            </button>
            <p className="text-[11px] text-center text-slate-500 dark:text-slate-400 mt-2">
              Responses are automatically frozen upon submission.
            </p>
          </div>
        </aside>
      </div>

      {/* 4. On-Screen Scientific Calculator Modal */}
      {isCalculatorOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-sm p-4 shadow-2xl text-white">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
              <div className="flex items-center gap-2 text-cyan-400 text-sm font-bold">
                <CalcIcon className="h-4 w-4" /> Scientific Calculator
              </div>
              <button
                onClick={() => setIsCalculatorOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="bg-slate-950 rounded-xl p-3 border border-slate-800 mb-3 font-mono text-right">
              <div className="text-xs text-slate-400 h-4 overflow-hidden">{calcInput || "0"}</div>
              <div className="text-2xl font-bold text-cyan-400 h-8 overflow-hidden">
                {calcResult || "0"}
              </div>
            </div>

            <div className="grid grid-cols-4 gap-1.5 text-xs font-semibold">
              {["sin", "cos", "tan", "C"].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className={`p-2 rounded-lg font-mono transition ${
                    k === "C" ? "bg-rose-600 hover:bg-rose-500 text-white" : "bg-slate-800 hover:bg-slate-700 text-cyan-300"
                  }`}
                >
                  {k}
                </button>
              ))}

              {["sqrt", "(", ")", "/"].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono transition"
                >
                  {k}
                </button>
              ))}

              {["7", "8", "9", "*"].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className={`p-2.5 rounded-lg font-mono transition ${
                    k === "*" ? "bg-slate-800 text-amber-300" : "bg-slate-800/60 hover:bg-slate-700 text-white"
                  }`}
                >
                  {k}
                </button>
              ))}

              {["4", "5", "6", "-"].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className={`p-2.5 rounded-lg font-mono transition ${
                    k === "-" ? "bg-slate-800 text-amber-300" : "bg-slate-800/60 hover:bg-slate-700 text-white"
                  }`}
                >
                  {k}
                </button>
              ))}

              {["1", "2", "3", "+"].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className={`p-2.5 rounded-lg font-mono transition ${
                    k === "+" ? "bg-slate-800 text-amber-300" : "bg-slate-800/60 hover:bg-slate-700 text-white"
                  }`}
                >
                  {k}
                </button>
              ))}

              {["0", ".", "DEL", "="].map((k) => (
                <button
                  key={k}
                  onClick={() => handleCalcClick(k)}
                  className={`p-2.5 rounded-lg font-mono transition ${
                    k === "="
                      ? "bg-cyan-600 hover:bg-cyan-500 text-white font-bold"
                      : k === "DEL"
                      ? "bg-slate-700 text-rose-300"
                      : "bg-slate-800/60 hover:bg-slate-700 text-white"
                  }`}
                >
                  {k}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 5. Security Warning Modal (Phase 3 Module 8) */}
      {isSecurityWarningOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-slate-900 border-2 border-amber-500 rounded-2xl w-full max-w-md p-6 shadow-2xl text-white text-center">
            <div className="h-16 w-16 bg-amber-500/20 text-amber-400 rounded-full flex items-center justify-center mx-auto mb-4 ring-8 ring-amber-500/10">
              <AlertTriangle className="h-8 w-8" />
            </div>
            <h3 className="text-lg font-bold text-amber-300 mb-2">{securityModalTitle}</h3>
            <p className="text-xs text-slate-300 mb-6 leading-relaxed">{securityModalDesc}</p>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 mb-6 flex items-center justify-around text-xs font-mono">
              <span className="text-slate-400">Total Strikes Issued:</span>
              <span className="font-bold text-amber-400 text-sm">{warningsCount} / 3 Strikes</span>
            </div>

            <button
              onClick={reenterFullscreen}
              className="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold text-xs tracking-wide transition shadow-lg"
            >
              Acknowledge & Re-enter Fullscreen Lockdown
            </button>
          </div>
        </div>
      )}

      {/* 6. Exam Submission Confirmation Modal */}
      {isSubmitModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl text-slate-900 dark:text-white">
            <div className="flex items-center gap-3 text-amber-600 dark:text-amber-400 mb-4">
              <AlertTriangle className="h-6 w-6" />
              <h2 className="text-lg font-bold">Confirm Final Examination Submission</h2>
            </div>

            <p className="text-xs text-slate-600 dark:text-slate-400 mb-4">
              Are you sure you want to finish the exam? Once submitted, you cannot change your answers.
            </p>

            <div className="border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden mb-6 text-xs">
              <table className="w-full text-left">
                <thead className="bg-slate-100 dark:bg-slate-800/70 font-semibold text-slate-700 dark:text-slate-300">
                  <tr>
                    <th className="p-2.5">Category</th>
                    <th className="p-2.5 text-right">Count</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                  <tr>
                    <td className="p-2.5 text-slate-600 dark:text-slate-400">Total Questions</td>
                    <td className="p-2.5 text-right font-bold">{stats.total}</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 text-emerald-600 dark:text-emerald-400 font-medium">Answered</td>
                    <td className="p-2.5 text-right font-bold text-emerald-600">{stats.answered}</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 text-rose-500 font-medium">Not Answered</td>
                    <td className="p-2.5 text-right font-bold text-rose-500">{stats.notAnswered}</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 text-purple-600 dark:text-purple-400 font-medium">
                      Marked for Review
                    </td>
                    <td className="p-2.5 text-right font-bold text-purple-600">{stats.markedForReview}</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 text-purple-600 dark:text-purple-400 font-medium">
                      Answered & Marked for Review
                    </td>
                    <td className="p-2.5 text-right font-bold text-purple-600">{stats.answeredAndMarked}</td>
                  </tr>
                  <tr>
                    <td className="p-2.5 text-slate-500">Not Visited</td>
                    <td className="p-2.5 text-right font-bold text-slate-500">{stats.notVisited}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-end gap-3">
              <button
                onClick={() => setIsSubmitModalOpen(false)}
                className="px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold transition"
              >
                Return to Test
              </button>
              <button
                onClick={handleFinalSubmit}
                className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold transition shadow-md"
              >
                Yes, Final Submit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 7. General Instructions Modal */}
      {isInstructionsOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl text-slate-900 dark:text-white max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800 mb-4">
              <h2 className="text-base font-bold flex items-center gap-2">
                <FileText className="h-5 w-5 text-cyan-600" /> General Test Instructions & Security Rules
              </h2>
              <button
                onClick={() => setIsInstructionsOpen(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-white p-1 rounded"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                1. <strong>Strict Fullscreen Enforcement</strong>: The exam runs in exclusive fullscreen mode. Navigating away, switching tabs, or minimizing the window will trigger an official security strike.
              </p>
              <p>
                2. <strong>3-Strike Policy</strong>: Any candidate accumulating 3 security violations (tab switch, clipboard operations, devtools attempts) will be <strong>automatically disqualified</strong>.
              </p>
              <p>
                3. Marking Scheme: Each correct answer awards <strong>+2.00 marks</strong>. Each incorrect
                response incurs a negative penalty of <strong>-0.50 marks</strong>.
              </p>
              <p>
                4. All responses are periodically auto-saved to the server every 3 seconds.
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 text-right">
              <button
                onClick={() => setIsInstructionsOpen(false)}
                className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold transition"
              >
                Understood & Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
