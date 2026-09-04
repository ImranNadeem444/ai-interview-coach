import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // =========================================================
  // SETUP STATE
  // =========================================================

  const [resumeFile, setResumeFile] = useState(null);
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [resumeStatus, setResumeStatus] = useState("");

  const [jobDescription, setJobDescription] = useState("");
  const [jobDescriptionUploaded, setJobDescriptionUploaded] =
    useState(false);
  const [jobStatus, setJobStatus] = useState("");

  // =========================================================
  // INTERVIEW STATE
  // =========================================================

  const [interviewId, setInterviewId] = useState(null);
  const [question, setQuestion] = useState("");
  const [questionAudio, setQuestionAudio] = useState("");

  const [transcript, setTranscript] = useState("");
  const [evaluation, setEvaluation] = useState(null);

  const [status, setStatus] = useState("setup");
  const [error, setError] = useState("");

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const currentAudioRef = useRef(null);

  // =========================================================
  // CLEAN TEXT
  // =========================================================

  function cleanJobDescription(text) {
    return text
      .replace(/&nbsp;/gi, " ")
      .replace(/&amp;/gi, "&")
      .replace(/&lt;/gi, "<")
      .replace(/&gt;/gi, ">")
      .replace(/\r\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  // =========================================================
  // RESUME SELECT
  // =========================================================

  function handleResumeChange(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    const allowedExtensions = [".pdf", ".docx", ".txt"];
    const fileName = file.name.toLowerCase();

    const valid = allowedExtensions.some((extension) =>
      fileName.endsWith(extension)
    );

    if (!valid) {
      setResumeFile(null);
      setResumeUploaded(false);
      setResumeStatus("");
      setError("Please choose a PDF, DOCX, or TXT resume.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setResumeFile(null);
      setResumeUploaded(false);
      setResumeStatus("");
      setError("Resume must be smaller than 10MB.");
      return;
    }

    setError("");
    setResumeFile(file);
    setResumeUploaded(false);
    setResumeStatus("Ready to upload");
  }

  // =========================================================
  // UPLOAD RESUME
  // =========================================================

  async function uploadResume() {
    if (!resumeFile) {
      setError("Please choose your resume first.");
      return;
    }

    try {
      setError("");
      setResumeStatus("Uploading...");

      const formData = new FormData();
      formData.append("file", resumeFile);

      const response = await fetch(`${API_URL}/upload/resume`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(
          `Resume upload failed (${response.status}): ${text}`
        );
      }

      await response.json();

      setResumeUploaded(true);
      setResumeStatus("Resume uploaded successfully.");
    } catch (err) {
      console.error("Resume upload error:", err);

      setResumeUploaded(false);
      setResumeStatus("");

      setError(
        err.message || "Failed to upload your resume."
      );
    }
  }

  // =========================================================
  // JOB DESCRIPTION
  // =========================================================

  function handleJobDescriptionChange(event) {
    const cleaned = cleanJobDescription(event.target.value);

    setJobDescription(cleaned);
    setJobDescriptionUploaded(false);
    setJobStatus("");
    setError("");
  }

  // =========================================================
  // ADD JOB DESCRIPTION
  // =========================================================

  async function uploadJobDescription() {
    const cleaned = cleanJobDescription(jobDescription);

    if (!cleaned) {
      setError("Please paste the job description first.");
      return;
    }

    try {
      setError("");
      setJobStatus("Adding job description...");

      const response = await fetch(`${API_URL}/job-description`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: cleaned,
        }),
      });

      if (!response.ok) {
        const text = await response.text();

        throw new Error(
          `Job description failed (${response.status}): ${text}`
        );
      }

      await response.json();

      setJobDescriptionUploaded(true);
      setJobStatus("Job description added successfully.");
    } catch (err) {
      console.error("Job description error:", err);

      setJobDescriptionUploaded(false);
      setJobStatus("");

      setError(
        err.message ||
          "Failed to add the job description."
      );
    }
  }

  // =========================================================
  // START INTERVIEW
  // =========================================================

  async function startInterview() {
    setError("");

    if (!resumeUploaded) {
      setError(
        "Please upload your resume before starting the interview."
      );
      return;
    }

    if (!jobDescriptionUploaded) {
      setError(
        "Please add the job description before starting."
      );
      return;
    }

    try {
      setStatus("starting");

      const response = await fetch(`${API_URL}/interviews/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resume_query:
            "Candidate resume uploaded and indexed in the RAG system.",
          job_description: jobDescription,
        }),
      });

      if (!response.ok) {
        const text = await response.text();

        throw new Error(
          `Failed to start interview (${response.status}): ${text}`
        );
      }

      const data = await response.json();

      console.log("Interview started:", data);

      setInterviewId(data.interview_id);
      setQuestion(data.question || "");
      setTranscript("");
      setEvaluation(null);

      if (data.question_audio) {
        setQuestionAudio(
          `${API_URL}${data.question_audio}`
        );
      } else {
        setQuestionAudio("");
        setStatus("ready_to_answer");
      }
    } catch (err) {
      console.error("Start interview error:", err);

      setError(
        err.message ||
          "Could not start the interview."
      );

      setStatus("setup");
    }
  }

  // =========================================================
  // PLAY QUESTION
  // =========================================================

  function playQuestion(audioUrl) {
    if (!audioUrl) {
      setStatus("ready_to_answer");
      return;
    }

    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current.currentTime = 0;
    }

    const audio = new Audio(audioUrl);

    currentAudioRef.current = audio;

    audio.onplay = () => {
      setStatus("speaking");
    };

    audio.onended = () => {
      setStatus("ready_to_answer");
    };

    audio.onerror = () => {
      setError(
        "The interview question audio could not be played."
      );

      setStatus("ready_to_answer");
    };

    audio.play().catch(() => {
      setError(
        "The browser blocked the audio. Click the play button."
      );

      setStatus("ready_to_answer");
    });
  }

  // =========================================================
  // AUTO PLAY QUESTION
  // =========================================================

  useEffect(() => {
    if (questionAudio && interviewId) {
      playQuestion(questionAudio);
    }
  }, [questionAudio, interviewId]);

  // =========================================================
  // START RECORDING
  // =========================================================

  async function startRecording() {
    try {
      setError("");

      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error(
          "Your browser does not support microphone recording."
        );
      }

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      const recorder = new MediaRecorder(stream);

      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());

        const audioBlob = new Blob(
          audioChunksRef.current,
          {
            type: "audio/webm",
          }
        );

        await submitVoiceAnswer(audioBlob);
      };

      recorder.start();

      setStatus("recording");
    } catch (err) {
      console.error("Recording error:", err);

      setError(
        "Microphone permission was denied or the microphone is unavailable."
      );

      setStatus("ready_to_answer");
    }
  }

  // =========================================================
  // STOP RECORDING
  // =========================================================

  function stopRecording() {
    const recorder = mediaRecorderRef.current;

    if (
      recorder &&
      recorder.state === "recording"
    ) {
      recorder.stop();
    }
  }

  // =========================================================
  // SUBMIT VOICE ANSWER
  // =========================================================

  async function submitVoiceAnswer(audioBlob) {
    if (!interviewId) {
      setError("No active interview.");
      return;
    }

    try {
      setStatus("processing");
      setError("");

      if (!audioBlob || audioBlob.size === 0) {
        throw new Error(
          "The recorded answer is empty."
        );
      }

      const formData = new FormData();

      formData.append(
        "audio",
        audioBlob,
        "candidate-answer.webm"
      );

      const response = await fetch(
        `${API_URL}/interviews/${interviewId}/voice-answer`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const text = await response.text();

        throw new Error(
          `Voice answer failed (${response.status}): ${text}`
        );
      }

      const data = await response.json();

      console.log(
        "Voice answer response:",
        data
      );

      setTranscript(
        data.transcript || ""
      );

      setEvaluation(
        data.evaluation || null
      );

      setQuestion(
        data.next_question || ""
      );

      if (data.question_audio) {
        setQuestionAudio(
          `${API_URL}${data.question_audio}`
        );
      } else {
        setQuestionAudio("");
        setStatus("ready_to_answer");
      }
    } catch (err) {
      console.error(
        "Voice answer error:",
        err
      );

      setError(
        err.message ||
          "Could not process your answer."
      );

      setStatus("error");
    }
  }

  // =========================================================
  // RESET
  // =========================================================

  function resetInterview() {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current.currentTime = 0;
    }

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
    }

    setInterviewId(null);
    setQuestion("");
    setQuestionAudio("");
    setTranscript("");
    setEvaluation(null);
    setStatus("setup");
    setError("");
  }

  // =========================================================
  // INTERVIEW SCREEN
  // =========================================================

  if (interviewId) {
    const isSpeaking = status === "speaking";
    const isRecording = status === "recording";
    const isProcessing = status === "processing";

    return (
      <main className="interview-page">

        <header className="interview-header">
          <div className="brand">
            <div className="brand-logo">✦</div>

            <div>
              <span>AI INTERVIEW COACH</span>
              <h1>Live Interview</h1>
            </div>
          </div>

          <div className="live-pill">
            <span />
            LIVE
          </div>
        </header>

        <section className="interview-main">

          <div className="question-card">

            <div className="question-card-top">
              <div className="ai-label">
                <div className="ai-avatar">
                  AI
                </div>

                <div>
                  <strong>AI Interviewer</strong>
                  <span>Personalized interview</span>
                </div>
              </div>

              <span className="session-label">
                VOICE SESSION
              </span>
            </div>

            <div className="question-content">

              <span className="question-eyebrow">
                CURRENT QUESTION
              </span>

              <h2>
                {question ||
                  "Preparing your interview question..."}
              </h2>

              <div className="audio-status">

                {isSpeaking && (
                  <>
                    <div className="status-circle speaking">
                      🔊
                    </div>

                    <div>
                      <strong>
                        AI is speaking
                      </strong>

                      <span>
                        Listen to the question...
                      </span>
                    </div>
                  </>
                )}

                {isRecording && (
                  <>
                    <div className="status-circle recording">
                      <span />
                    </div>

                    <div>
                      <strong>
                        Recording your answer
                      </strong>

                      <span>
                        Speak clearly and take your time.
                      </span>
                    </div>
                  </>
                )}

                {isProcessing && (
                  <>
                    <div className="status-circle processing">
                      <span className="spinner" />
                    </div>

                    <div>
                      <strong>
                        AI is evaluating your answer
                      </strong>

                      <span>
                        Generating your next question...
                      </span>
                    </div>
                  </>
                )}

                {!isSpeaking &&
                  !isRecording &&
                  !isProcessing &&
                  status !== "error" && (
                    <>
                      <div className="status-circle ready">
                        🎤
                      </div>

                      <div>
                        <strong>
                          Your turn
                        </strong>

                        <span>
                          Click the button below to answer.
                        </span>
                      </div>
                    </>
                  )}
              </div>

              <div className="interview-controls">

                {status === "ready_to_answer" && (
                  <button
                    className="voice-button"
                    onClick={startRecording}
                  >
                    <span className="mic-icon">
                      🎙
                    </span>

                    Start Answer
                  </button>
                )}

                {status === "recording" && (
                  <button
                    className="stop-recording-button"
                    onClick={stopRecording}
                  >
                    <span className="stop-icon" />
                    Stop Recording
                  </button>
                )}

                {status === "speaking" && (
                  <button
                    className="secondary-action"
                    onClick={() => {
                      if (
                        currentAudioRef.current
                      ) {
                        currentAudioRef.current.pause();
                        currentAudioRef.current.currentTime = 0;
                      }

                      setStatus("ready_to_answer");
                    }}
                  >
                    Skip Audio
                  </button>
                )}

                {status === "processing" && (
                  <button
                    className="voice-button disabled"
                    disabled
                  >
                    <span className="spinner" />
                    Processing...
                  </button>
                )}
              </div>

              {questionAudio &&
                status === "ready_to_answer" && (
                  <button
                    className="replay-button"
                    onClick={() =>
                      playQuestion(questionAudio)
                    }
                  >
                    ↻ Replay question
                  </button>
                )}
            </div>
          </div>

          {transcript && (
            <div className="feedback-card">

              <div className="feedback-header">
                <div>
                  <span>AI FEEDBACK</span>
                  <h3>
                    Your previous answer
                  </h3>
                </div>

                {evaluation?.score !== undefined &&
                  evaluation?.score !== null && (
                    <div className="score">
                      <strong>
                        {evaluation.score}
                      </strong>
                      <span>/10</span>
                    </div>
                  )}
              </div>

              <div className="feedback-grid">

                <div>
                  <span className="feedback-label">
                    TRANSCRIPT
                  </span>

                  <p>
                    {transcript}
                  </p>
                </div>

                {evaluation && (
                  <div>
                    <span className="feedback-label">
                      IMPROVEMENT
                    </span>

                    <p>
                      {evaluation.improvement ||
                        evaluation.weaknesses ||
                        "Keep your answer specific and structured."}
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {error && (
            <div className="error-box interview-error">
              <span>!</span>
              <div>
                <strong>
                  Something went wrong
                </strong>

                <p>{error}</p>
              </div>
            </div>
          )}

          <button
            className="new-interview-button"
            onClick={resetInterview}
          >
            ← Start a new interview
          </button>

        </section>
      </main>
    );
  }

  // =========================================================
  // SETUP SCREEN
  // =========================================================

  const ready =
    resumeUploaded &&
    jobDescriptionUploaded;

  const resumeReady =
    !!resumeFile &&
    !resumeUploaded;

  const addingJob =
    jobStatus === "Adding job description...";

  const uploadingResume =
    resumeStatus === "Uploading...";

  return (
    <main className="setup-page">

      <div className="setup-shell">

        {/* ===================================================
            TOP BAR
        =================================================== */}

        <header className="topbar">

          <div className="brand">
            <div className="brand-logo">
              ✦
            </div>

            <div>
              <strong>AI Interview Coach</strong>
              <span>AI-powered interview practice</span>
            </div>
          </div>

          <div className="topbar-status">
            <span className="online-dot" />
            System ready
          </div>
        </header>

        {/* ===================================================
            HERO
        =================================================== */}

        <section className="setup-hero">

          <div>

            <div className="hero-badge">
              <span>✦</span>
              AI-POWERED INTERVIEW PRACTICE
            </div>

            <h1>
              Prepare for your
              <span> next interview.</span>
            </h1>

            <p>
              Upload your resume and job description.
              Our AI will create a realistic,
              personalized interview based on your
              experience and target role.
            </p>

          </div>

          <div className="progress">

            <div className="progress-step active">
              <div>1</div>
              <span>Prepare</span>
            </div>

            <div className="progress-line" />

            <div
              className={`progress-step ${
                ready ? "active" : ""
              }`}
            >
              <div>2</div>
              <span>Interview</span>
            </div>

          </div>

        </section>

        {/* ===================================================
            SETUP CARDS
        =================================================== */}

        <section className="setup-grid">

          {/* =================================================
              RESUME CARD
          ================================================= */}

          <article className="setup-card">

            <div className="card-header">

              <div className="step-icon">
                1
              </div>

              <div>
                <h2>
                  Upload your resume
                </h2>

                <p>
                  We'll use it to personalize
                  your interview.
                </p>
              </div>

              {resumeUploaded && (
                <span className="complete-badge">
                  ✓ Added
                </span>
              )}

            </div>

            <label
              className={`dropzone ${
                resumeUploaded
                  ? "uploaded"
                  : ""
              }`}
            >

              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleResumeChange}
              />

              <div className="drop-icon">
                {resumeUploaded
                  ? "✓"
                  : "↑"}
              </div>

              {resumeFile ? (
                <>
                  <strong>
                    {resumeFile.name}
                  </strong>

                  <span>
                    {resumeUploaded
                      ? "Resume uploaded successfully"
                      : "Ready to upload"}
                  </span>
                </>
              ) : (
                <>
                  <strong>
                    Choose your resume
                  </strong>

                  <span>
                    PDF, DOCX or TXT · Max 10MB
                  </span>
                </>
              )}

              <small>
                Click anywhere to browse
              </small>

            </label>

            {resumeReady && (
              <button
                className="upload-button"
                onClick={uploadResume}
                disabled={uploadingResume}
              >
                {uploadingResume ? (
                  <>
                    <span className="spinner" />
                    Uploading...
                  </>
                ) : (
                  <>
                    Upload Resume
                    <span>→</span>
                  </>
                )}
              </button>
            )}

            {resumeStatus &&
              resumeUploaded && (
                <div className="success-message">
                  <span>✓</span>
                  Resume uploaded successfully.
                </div>
              )}

            <div className="privacy-box">
              <span>🔒</span>

              <div>
                <strong>
                  Your resume is private
                </strong>

                <p>
                  It is only used to personalize
                  this interview session.
                </p>
              </div>
            </div>

          </article>

          {/* =================================================
              JOB CARD
          ================================================= */}

          <article className="setup-card">

            <div className="card-header">

              <div className="step-icon">
                2
              </div>

              <div>
                <h2>
                  Add job description
                </h2>

                <p>
                  Tell the AI what role you're targeting.
                </p>
              </div>

              {jobDescriptionUploaded && (
                <span className="complete-badge">
                  ✓ Added
                </span>
              )}

            </div>

            <textarea
              className="job-input"
              value={jobDescription}
              onChange={handleJobDescriptionChange}
              placeholder={`Paste the complete job description here...

Example:
AI/ML Engineer

Requirements:
• Python
• Machine Learning
• LLMs
• RAG
• FastAPI
• Docker
• Git/GitHub`}
            />

            <div className="textarea-meta">
              <span>
                {jobDescription.length.toLocaleString()} characters
              </span>

              {jobDescriptionUploaded && (
                <span className="added-text">
                  ✓ Added
                </span>
              )}
            </div>

            <button
              className="job-button"
              onClick={uploadJobDescription}
              disabled={
                !jobDescription.trim() ||
                addingJob
              }
            >
              {addingJob ? (
                <>
                  <span className="spinner" />
                  Adding...
                </>
              ) : jobDescriptionUploaded ? (
                <>
                  ✓ Job Description Added
                </>
              ) : (
                <>
                  Add Job Description
                  <span>→</span>
                </>
              )}
            </button>

            {jobDescriptionUploaded && (
              <div className="success-message">
                <span>✓</span>
                Job description added successfully.
              </div>
            )}

            <div className="tip-box">
              <span>✦</span>

              <div>
                <strong>
                  Better input, better interview
                </strong>

                <p>
                  Include the complete job description
                  so questions match the actual role.
                </p>
              </div>
            </div>

          </article>

        </section>

        {/* ===================================================
            READY PANEL
        =================================================== */}

        <section
          className={`ready-panel ${
            ready ? "ready" : ""
          }`}
        >

          <div className="ready-main">

            <div className="ready-icon">
              {ready ? "✓" : "✦"}
            </div>

            <div>
              <span className="ready-label">
                {ready
                  ? "READY TO START"
                  : "ALMOST THERE"}
              </span>

              <h2>
                {ready
                  ? "Your interview is ready."
                  : "Complete your preparation."}
              </h2>

              <p>
                {ready
                  ? "Your resume and job description are ready. Start the AI interview whenever you're ready."
                  : "Upload your resume and add the job description to unlock the interview."}
              </p>
            </div>

          </div>

          <div className="features">

            <div>
              <span>✦</span>
              <strong>Personalized</strong>
              <small>
                Resume-based questions
              </small>
            </div>

            <div>
              <span>◉</span>
              <strong>Realistic</strong>
              <small>
                Adaptive AI interviewer
              </small>
            </div>

            <div>
              <span>🎙</span>
              <strong>Voice-based</strong>
              <small>
                Speak your answers
              </small>
            </div>

          </div>

        </section>

        {/* ===================================================
            ERROR
        =================================================== */}

        {error && (
          <div className="error-box">
            <span>!</span>

            <div>
              <strong>
                Action required
              </strong>

              <p>{error}</p>
            </div>
          </div>
        )}

        {/* ===================================================
            START
        =================================================== */}

        <section className="start-section">

          <button
            className={`start-button ${
              ready ? "enabled" : ""
            }`}
            onClick={startInterview}
            disabled={
              !ready ||
              status === "starting"
            }
          >
            {status === "starting" ? (
              <>
                <span className="spinner" />
                Starting your interview...
              </>
            ) : (
              <>
                Start AI Interview
                <span className="start-arrow">
                  →
                </span>
              </>
            )}
          </button>

          <p>
            🔒 Your interview session is private
            and personalized to your resume.
          </p>

        </section>

      </div>
    </main>
  );
}

export default App;