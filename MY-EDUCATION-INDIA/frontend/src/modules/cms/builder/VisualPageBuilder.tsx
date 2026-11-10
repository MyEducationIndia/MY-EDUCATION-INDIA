import React, { useState } from "react";
import { Plus, Trash2, ArrowUp, ArrowDown, Save, Eye } from "lucide-react";
import { PageSectionItem } from "../types/cms.types";

interface VisualPageBuilderProps {
  initialSections: PageSectionItem[];
  onSave: (sections: PageSectionItem[]) => Promise<void>;
  onClose: () => void;
}

export const VisualPageBuilder: React.FC<VisualPageBuilderProps> = ({
  initialSections,
  onSave,
  onClose,
}) => {
  const [sections, setSections] = useState<PageSectionItem[]>(initialSections || []);
  const [isSaving, setIsSaving] = useState(false);

  const addBlock = (blockType: string) => {
    const newSec: PageSectionItem = {
      section_key: `section_${Date.now()}`,
      block_type: blockType,
      display_order: sections.length,
      is_visible: true,
      container_width: "BOXED",
      padding_top: 40,
      padding_bottom: 40,
      content_payload: {
        heading: `New ${blockType} Content Block`,
        subheading: "Configure text, images, and buttons in properties.",
      },
    };
    setSections([...sections, newSec]);
  };

  const removeBlock = (index: number) => {
    setSections(sections.filter((_, i) => i !== index));
  };

  const moveBlock = (index: number, direction: "UP" | "DOWN") => {
    const target = direction === "UP" ? index - 1 : index + 1;
    if (target < 0 || target >= sections.length) return;
    const reordered = [...sections];
    const temp = reordered[index];
    reordered[index] = reordered[target];
    reordered[target] = temp;
    setSections(reordered);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(sections);
      onClose();
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-xs">
      <div className="flex h-[90vh] w-full max-w-5xl flex-col rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-6 dark:border-slate-800">
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white">Visual Block Page Builder</h2>
            <p className="text-xs text-slate-500">Configure content blocks, hero banners, counters, courses, and forms.</p>
          </div>
          <div className="flex items-center gap-2">
            <button type="button" onClick={onClose} className="rounded-lg px-3 py-1.5 text-xs text-slate-500 hover:bg-slate-100">
              Cancel
            </button>
            <button
              type="button"
              disabled={isSaving}
              onClick={handleSave}
              className="inline-flex items-center gap-1.5 rounded-xl bg-brand-600 px-4 py-2 text-xs font-bold text-white shadow-md hover:bg-brand-500"
            >
              <Save className="h-4 w-4" />
              <span>{isSaving ? "Saving Layout..." : "Publish Revisions"}</span>
            </button>
          </div>
        </div>

        {/* Builder Canvas & Palette */}
        <div className="flex flex-1 overflow-hidden">
          {/* Blocks Palette */}
          <div className="w-64 border-r border-slate-200 p-4 overflow-y-auto dark:border-slate-800">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Available Reusable Blocks</h3>
            <div className="mt-3 space-y-2">
              {["HERO", "COUNTER", "COURSE_LIST", "ADMISSION_FORM", "GALLERY", "TESTIMONIAL", "DOWNLOADS", "HTML"].map((b) => (
                <button
                  key={b}
                  type="button"
                  onClick={() => addBlock(b)}
                  className="flex w-full items-center justify-between rounded-xl border border-slate-200 p-2.5 text-xs font-semibold text-slate-700 hover:border-brand-500 hover:bg-brand-50/50 dark:border-slate-800 dark:text-slate-300 dark:hover:bg-slate-800"
                >
                  <span>+ {b.replace("_", " ")}</span>
                  <Plus className="h-3.5 w-3.5 text-brand-600" />
                </button>
              ))}
            </div>
          </div>

          {/* Canvas Stacking */}
          <div className="flex-1 overflow-y-auto p-6 bg-slate-50 dark:bg-slate-950 space-y-4">
            {sections.length === 0 ? (
              <div className="rounded-2xl border-2 border-dashed border-slate-300 p-12 text-center text-xs text-slate-500 dark:border-slate-800">
                Click a block on the left palette to add content sections.
              </div>
            ) : (
              sections.map((sec, idx) => (
                <div key={idx} className="rounded-xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2 dark:border-slate-800">
                    <span className="font-mono text-xs font-bold text-brand-600">Block #{idx + 1}: {sec.block_type}</span>
                    <div className="flex items-center gap-1">
                      <button type="button" onClick={() => moveBlock(idx, "UP")} className="p-1 hover:text-brand-600"><ArrowUp className="h-3.5 w-3.5" /></button>
                      <button type="button" onClick={() => moveBlock(idx, "DOWN")} className="p-1 hover:text-brand-600"><ArrowDown className="h-3.5 w-3.5" /></button>
                      <button type="button" onClick={() => removeBlock(idx)} className="p-1 text-rose-600 hover:text-rose-500"><Trash2 className="h-3.5 w-3.5" /></button>
                    </div>
                  </div>
                  <div className="mt-3">
                    <label className="block text-[11px] font-semibold text-slate-500">Heading Text</label>
                    <input
                      type="text"
                      value={sec.content_payload.heading || ""}
                      onChange={(e) => {
                        const updated = [...sections];
                        updated[idx].content_payload.heading = e.target.value;
                        setSections(updated);
                      }}
                      className="mt-1 block w-full rounded-lg border border-slate-200 px-3 py-1.5 text-xs dark:border-slate-700 dark:bg-slate-950"
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
