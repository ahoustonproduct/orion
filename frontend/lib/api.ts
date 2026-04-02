const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api";

export async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`);
  return res.json();
}

export async function streamPost(
  path: string,
  body: unknown,
  onChunk: (text: string) => void
): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Stream ${path} failed: ${res.status}`);
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    onChunk(decoder.decode(value, { stream: true }));
  }
}

// ── Curriculum ──────────────────────────────────────────────────────────────
export const fetchModules = () => get<Module[]>("/curriculum/modules");
export const fetchModule = (id: string) => get<Module>(`/curriculum/modules/${id}`);
export const fetchLesson = (id: string) => get<Lesson>(`/curriculum/lessons/${id}`);
export const fetchGlossary = () => get<GlossaryEntry[]>("/curriculum/glossary");

// ── Progress ─────────────────────────────────────────────────────────────────
export const fetchProgress = (userKey: string) =>
  get<ProgressData>(`/progress/${userKey}`);

export const saveProgress = (userKey: string, data: ProgressUpdate) =>
  post<{ success: boolean; stars: number }>(`/progress/${userKey}/lesson`, data);

export const toggleFlag = (userKey: string, lessonId: string, flagged: boolean) =>
  post<{ success: boolean }>(`/progress/${userKey}/flag`, { lesson_id: lessonId, flagged });

export const fetchNote = (userKey: string) =>
  get<{ content: string }>(`/progress/${userKey}/note`);

export const saveNote = (userKey: string, content: string) =>
  post<{ success: boolean }>(`/progress/${userKey}/note`, { content });

export const saveBookmark = (userKey: string, data: BookmarkUpdate) =>
  post<{ success: boolean }>(`/progress/${userKey}/bookmark`, data);

export const fetchBookmark = (userKey: string, lessonId: string) =>
  get<BookmarkData>(`/progress/${userKey}/bookmark/${lessonId}`);

export const saveConfidence = (userKey: string, lessonId: string, rating: number) =>
  post<{ success: boolean }>(`/progress/${userKey}/confidence`, {
    lesson_id: lessonId, rating
  });

export const saveAnalogy = (userKey: string, lessonId: string, analogy: string) =>
  post<{ success: boolean }>(`/progress/${userKey}/analogy`, {
    lesson_id: lessonId, analogy
  });

export const fetchWeekData = (userKey: string) =>
  get<WeekData>(`/progress/${userKey}/week-review`);

// ── Quiz ──────────────────────────────────────────────────────────────────────
export const fetchQuiz = (userKey: string) =>
  get<QuizData>(`/quiz/${userKey}`);

// ── Orion AI (streaming) ──────────────────────────────────────────────────────
export const streamExplain = (userKey: string, lesson: Lesson, onChunk: (t: string) => void) =>
  streamPost("/orion/explain", { user_key: userKey, lesson }, onChunk);

export const streamFeedback = (
  userKey: string, lesson: Lesson, studentCode: string,
  actualOutput: string, expectedOutput: string, attempts: number,
  onChunk: (t: string) => void
) => streamPost("/orion/feedback", {
  user_key: userKey, lesson, student_code: studentCode,
  actual_output: actualOutput, expected_output: expectedOutput, attempts
}, onChunk);

export const streamHint = (
  lesson: Lesson, studentCode: string, hintNumber: number, onChunk: (t: string) => void
) => streamPost("/orion/hint", { lesson, student_code: studentCode, hint_number: hintNumber }, onChunk);

export const streamRecap = (
  userKey: string, lesson: Lesson, stars: number,
  attempts: number, studentCode: string, onChunk: (t: string) => void
) => streamPost("/orion/recap", {
  user_key: userKey, lesson, stars, attempts, student_code: studentCode
}, onChunk);

export const streamChallenge = (
  userKey: string, lesson: Lesson, variationIndex: number, onChunk: (t: string) => void
) => streamPost("/orion/generate-challenge", {
  user_key: userKey, lesson, variation_index: variationIndex
}, onChunk);

export const streamExplainAnswer = (
  lesson: Lesson, question: Question, chosenOption: string,
  studentReasoning: string, onChunk: (t: string) => void
) => streamPost("/orion/explain-your-answer", {
  lesson, question, chosen_option: chosenOption, student_reasoning: studentReasoning
}, onChunk);

export const streamStudyPlan = (
  userKey: string, progressData: ProgressData,
  daysUntilStart: number, onChunk: (t: string) => void
) => streamPost("/orion/study-plan", {
  user_key: userKey, progress_data: progressData, days_until_start: daysUntilStart
}, onChunk);

export const streamWeekReview = (
  userKey: string, weekData: WeekData, onChunk: (t: string) => void
) => streamPost("/orion/week-review", { user_key: userKey, week_data: weekData }, onChunk);

export const streamWhatNext = (
  userKey: string, progressData: ProgressData, onChunk: (t: string) => void
) => streamPost("/orion/what-next", { user_key: userKey, progress_data: progressData }, onChunk);

// ── Types ─────────────────────────────────────────────────────────────────────
export interface Module {
  id: string;
  title: string;
  description: string;
  course: string;
  order: number;
  locked: boolean;
  lesson_count: number;
  lessons?: LessonSummary[];
}

export interface LessonSummary {
  id: string;
  title: string;
  order: number;
  duration_min: number;
}

export interface Lesson {
  id: string;
  title: string;
  order: number;
  duration_min: number;
  concept: string;
  module_title: string;
  real_world_context?: string;
  worked_example?: WorkedExample;
  difficulty?: "beginner" | "intermediate" | "advanced";
  challenge_variations?: string[];
  is_capstone?: boolean;
  reference: { key_syntax: string[]; notes: string };
  questions: Question[];
  challenge: Challenge;
}

export interface WorkedExample {
  description: string;
  code: string;
  explanation: string;
}

export interface Question {
  type: "multiple_choice" | "true_false" | "fill_blank" | "code_ordering" | "debug";
  question: string;
  options?: string[];
  lines?: string[];
  template?: string;
  broken_code?: string;
  answer: boolean | number | number[] | string;
  explanation: string;
}

export interface Challenge {
  instructions: string;
  starter_code: string;
  tests: { type: string; value?: string | number }[];
  solution: string;
}

export interface ProgressData {
  lessons: LessonProgress[];
  module_status: Record<string, ModuleStatus>;
  streak: number;
  study_log: Record<string, number>;
  weak_topics: string[];
  mastered_concepts: string[];
  preferred_analogies: Record<string, string>;
  topic_confidence: Record<string, number>;
  study_plan: Record<string, unknown>;
}

export interface LessonProgress {
  lesson_id: string;
  stars: number;
  attempts: number;
  completed: boolean;
  flagged: boolean;
  last_accessed: string | null;
}

export interface ModuleStatus {
  completed_count: number;
  total: number;
  mastery_pct: number;
  unlocked: boolean;
}

export interface ProgressUpdate {
  lesson_id: string;
  stars: number;
  attempts: number;
  hints_used: number;
  completed: boolean;
  time_spent_minutes?: number;
}

export interface BookmarkUpdate {
  lesson_id: string;
  step_index: number;
  sub_step?: number;
  saved_code?: string;
}

export interface BookmarkData {
  found: boolean;
  step_index: number;
  sub_step: number;
  saved_code: string;
}

export interface WeekData {
  study_log: Record<string, number>;
  lessons_completed: string[];
  stars_earned: Record<string, number>;
  streak: number;
  days_studied: number;
  total_minutes: number;
}

export interface GlossaryEntry {
  term: string;
  definition: string;
  module: string;
}

export interface QuizData {
  questions: Question[];
  lesson_ids?: string[];
  message?: string;
}

// ── FinTech Lesson Block Types ─────────────────────────────────────────────────

export interface FinTechLesson {
  id: string;
  module_id: string;
  title: string;
  order: number;
  duration_min: number;
  difficulty: string;
  concept_tags: string[];
  learning_objectives: string[];
  status?: string;
  blocks: LessonBlock[];
}

export type LessonBlock =
  | ConceptBlock | DecisionContextBlock | GuidedAnalysisBlock
  | DecisionBlock | TechnicalExerciseBlock | QuizBlock2
  | SolutionDebriefBlock | StubNoticeBlock;

export interface ConceptBlock {
  type: "concept_block";
  fintech_hook: string;
  explanation: string;
  code_example: { language: string; code: string; output: string };
}

export interface DecisionContextBlock {
  type: "decision_context_block";
  company: string;
  role: string;
  scenario: string;
  constraints: string[];
  stakeholder_pressures: { stakeholder: string; pressure: string }[];
}

export interface GuidedAnalysisBlock {
  type: "guided_analysis_block";
  dataset_table: string;
  intro: string;
  steps: { step: number; instruction: string; code: string; output: string; business_implication: string }[];
}

export type DecisionType = "numeric_threshold" | "policy_choice" | "budget_allocation" | "approval_matrix" | "written_justification";

export interface DecisionBlock {
  type: "decision_block";
  decision_type: DecisionType;
  prompt: string;
  slider_min?: number; slider_max?: number; slider_step?: number; default_value?: number;
  outcome_function?: string; optimal_value?: number; worst_value?: number; outcome_explanation?: string;
  options?: { id: string; label: string; description: string; risk_level?: string }[];
  optimal_option?: string; worst_option?: string;
  budget_total?: number;
  categories?: { id: string; label: string; description: string }[];
  optimal_allocation?: Record<string, number>;
  segments?: { id: string; label: string; fraud_rate?: string; avg_amount?: number }[];
  options_per_segment?: string[]; optimal_matrix?: Record<string, string>;
  key_concepts_required?: string[]; sample_answer?: string;
}

export interface TechnicalExerciseBlock {
  type: "technical_exercise_block";
  language: "python" | "sql";
  standard: { instructions: string; starter_code: string; solution: string; hint: string; expected_output?: string };
  challenge: { instructions: string; starter_code: string; solution: string; hint: string };
}

export interface QuizQuestion2 {
  id: string;
  concept_tags: string[];
  type: "multiple_choice" | "short_answer" | "what_would_you_do" | "true_false";
  question: string;
  options?: string[];
  correct_index?: number;
  explanation: string;
  accepted_answers?: string[];
  sample_answer?: string;
  key_concepts?: string[];
}

export interface QuizBlock2 {
  type: "quiz_block";
  questions: QuizQuestion2[];
}

export interface SolutionDebriefBlock {
  type: "solution_debrief_block";
  optimal_decision: string;
  decision_rationale: string;
  pl_comparison: { label: string; approval_rate?: string; default_rate?: string; monthly_profit?: string; verdict: string }[];
  stakeholder_communication: string;
  key_takeaway: string;
  next_lessons?: string[];
}

export interface StubNoticeBlock {
  type: "stub_notice";
  message: string;
  available_date: string;
}

export interface DecisionEvaluateResponse {
  user_outcome: number; optimal_outcome: number; worst_outcome: number;
  score: number; pl_delta: number; explanation: string;
}

export interface MasteryData {
  tags: Record<string, number>;
  focus_areas: { tag: string; mastery: number }[];
  heatmap_data: { tag: string; mastery: number; attempts: number }[];
}

export interface ReviewQueue {
  questions: ReviewQuestion[];
  total_due: number;
}

export interface ReviewQuestion {
  id: number; question_id: string; lesson_id: string;
  wrong_count: number; question: QuizQuestion2;
}

export interface ExecuteResult {
  output: string; error: string | null; duration_ms: number;
}

export interface SQLResult {
  columns: string[]; rows: unknown[][]; row_count: number; duration_ms: number; error: string | null;
}

// ── New API Functions ─────────────────────────────────────────────────────────

export const fetchFinTechLesson = (id: string) => get<FinTechLesson>(`/curriculum/lessons/${id}`);
export const executePython = (code: string) => post<ExecuteResult>("/execute/python", { code });
export const executeSQL = (query: string) => post<SQLResult>("/execute/sql", { query });

export const evaluateDecision = (lessonId: string, blockId: string, decisionType: string, userValue: unknown) =>
  post<DecisionEvaluateResponse>("/decision/evaluate", { lesson_id: lessonId, block_id: blockId, decision_type: decisionType, user_value: userValue });

export const fetchMastery = (userKey: string) => get<MasteryData>(`/mastery/${userKey}`);
export const recordMastery = (userKey: string, conceptTag: string, correct: boolean) =>
  post<{ ok: boolean }>(`/mastery/${userKey}/record`, { concept_tag: conceptTag, correct });

export const fetchReviewQueue = (userKey: string) => get<ReviewQueue>(`/review/${userKey}/queue`);
export const recordReview = (userKey: string, questionId: string, correct: boolean) =>
  post<{ ok: boolean }>(`/review/${userKey}/record`, { question_id: questionId, correct });

export const addToReviewQueue = (userKey: string, questionId: string, lessonId: string, questionJson: string) =>
  post<{ ok: boolean }>(`/review/${userKey}/add`, { question_id: questionId, lesson_id: lessonId, question_json: questionJson });

export const streamEvaluateDecision = (lessonId: string, decisionValue: unknown, scenario: string, onChunk: (t: string) => void) =>
  streamPost("/orion/evaluate-decision", { lesson_id: lessonId, decision_value: decisionValue, scenario }, onChunk);
